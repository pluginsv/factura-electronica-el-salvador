# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_round
import logging
_logger = logging.getLogger(__name__)

try:
    from odoo.addons.common_utils_sv_dte.utils import config_utils
    from odoo.addons.common_utils_sv_dte.utils import constants
    _logger.info("SIT Modulo config_utils [purchase_sv_dte -purchase_order]")
except ImportError as e:
    _logger.error(f"[purchase_sv_dte -purchase_order] Error al importar 'config_utils': {e}")
    config_utils = None
    constants = None

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    document_number = fields.Char("Número de documento de proveedor")

    journal_id = fields.Many2one(
        'account.journal',
        string='Diario contable',
        domain="[('type', '=', 'purchase')]",
        help="Seleccione el diario contable para la factura de proveedor.",
        required=True
    )

    # Aplicar retenciones
    apply_retencion_iva_po = fields.Boolean(string="Aplicar Retención IVA", default=False)
    retencion_iva_amount_po = fields.Monetary(string="Monto Retención IVA", currency_field='currency_id', tracking=True,
                                              compute='_compute_retencion_purchase', readonly=True, store=True, default=0.0)

    apply_retencion_renta_po = fields.Boolean(string="Aplicar Renta 10%", default=False)
    apply_renta_20_po = fields.Boolean(string="Aplicar Renta 20%", default=False)
    retencion_renta_amount_po = fields.Monetary(string="Monto Retención Renta", currency_field='currency_id',
                                                tracking=True,
                                                compute='_compute_retencion_purchase', readonly=True, store=True, default=0.0)

    apply_iva_percibido_po = fields.Boolean(string="Aplicar IVA percibido", default=False)
    iva_percibido_amount_po = fields.Monetary(string="Monto iva percibido", currency_field='currency_id', tracking=True,
                                              compute='_compute_retencion_purchase', readonly=True, store=True, default=0.0)

    amount_total_retenciones_purchase = fields.Monetary(
        string="Total a Pagar con Retención",
        currency_field="currency_id",
        compute="_compute_total_con_retenciones",
        store=True,
        tracking=True
    )

    # ── Banner de advertencia en el formulario ──────────────────────
    advertencia_gran_contribuyente_purchase = fields.Html(
        string='Advertencia Gran Contribuyente',
        compute='_compute_advertencia_gran_contribuyente_purchase',
    )

    tipo_dte_purchase = fields.Char(
        string='Tipo DTE',
        related='journal_id.sit_tipo_documento.codigo',
        store=False,
    )

    def _prepare_invoice(self):
        res = super()._prepare_invoice()
        if self.journal_id:
            res['journal_id'] = self.journal_id.id

        # Asignar fecha de documento al crear la factura
        if not res.get('invoice_date'):
            res['invoice_date'] = fields.Date.context_today(self)

        # Logs de estado de retenciones
        _logger.info("Estado retenciones -> renta:%s retencion iva:%s iva_percibido:%s", self.apply_retencion_renta_po, self.apply_retencion_iva_po, self.apply_iva_percibido_po)

        # Copiar configuración de retenciones desde la cotización
        if self.apply_retencion_renta_po:
            res.update({
                'apply_retencion_renta': self.apply_retencion_renta_po,
                'retencion_renta_amount': self.retencion_renta_amount_po,
            })
        elif self.apply_renta_20_po:
            res.update({
                'apply_renta_20': self.apply_renta_20_po,
                'retencion_renta_amount': self.retencion_renta_amount_po,
            })

        if self.apply_retencion_iva_po:
            res.update({
                'apply_retencion_iva': self.apply_retencion_iva_po,
                'retencion_iva_amount': self.retencion_iva_amount_po,
            })

        if self.apply_iva_percibido_po:
            res.update({
                'apply_iva_percibido': self.apply_iva_percibido_po,
                'iva_percibido_amount': self.iva_percibido_amount_po,
            })

        return res

    def action_create_invoice(self, **kwargs):
        ctx = dict(self.env.context)

        omitir = any(
            order.amount_untaxed >= 100 and order.partner_id and order.partner_id.gran_contribuyente and not order.apply_iva_percibido_po
            for order in self
        )

        ctx['omitir_ret_perc'] = omitir
        _logger.info("[Purchase Order] Omitir retencion/percepcion: %s", omitir)
        moves = super(PurchaseOrder, self.with_context(ctx)).action_create_invoice(**kwargs)
        return moves

    def button_confirm(self):
        for order in self:
            if not order.journal_id:
                raise UserError(_(
                    'Debe seleccionar un diario antes de confirmar la orden de compra "%s".'
                ) % order.name)
        return super().button_confirm()

    @api.onchange('partner_id', 'order_line')
    def _onchange_partner_id(self):
        _logger.info("[ONCHANGE SALE ORDER] partner_id cambiado en sale.order ID=%s", self.id)

        if self.partner_id and self.partner_id.journal_id and self.partner_id.journal_id.type == constants.TYPE_COMPRA:
            self.journal_id = self.partner_id.journal_id

        self.apply_iva_percibido_po = False
        _logger.info("Filtros DTE -> company:%s | sit_fact:%s", self.company_id, self.company_id.sit_facturacion)

        if self.company_id and self.company_id.sit_facturacion:
            if self.partner_id:
                _logger.info("[ONCHANGE] Cliente: %s (ID=%s) - gran_contribuyente=%s", self.partner_id.name, self.partner_id.id, self.partner_id.gran_contribuyente)

                if self.amount_untaxed >= 100 and self.partner_id.gran_contribuyente:
                    self.apply_iva_percibido_po = True
                    _logger.info("[ONCHANGE] apply_iva_percibido_po=True (gran contribuyente y monto >= 100).")
                else:
                    _logger.info("[ONCHANGE] Se estableció apply_iva_percibido_po=False porque NO es gran contribuyente.")
            else:
                _logger.info("[ONCHANGE] No hay partner seleccionado, apply_iva_percibido_po=False")

    @api.depends('apply_retencion_renta_po', 'apply_renta_20_po', 'apply_retencion_iva_po', 'apply_iva_percibido_po', 'amount_untaxed')
    def _compute_retencion_purchase(self):
        for order in self:
            """Reinicia los montos de retención e IVA percibido a cero."""
            order.retencion_renta_amount_po = 0.0
            order.retencion_iva_amount_po = 0.0
            order.iva_percibido_amount_po = 0.0
            # retencion_renta = 0.0
            retencion_iva = 0.0
            iva_percibido = 0.0

            # Ventas → solo si no hay facturación electrónica se resetea
            if not order.company_id.sit_facturacion:
                _logger.info("SIT _compute_retencion_purchase Cotizacion | Orden de Venta detectada sin facturación -> order_id: %s, se omiten cálculos", order.id)
                continue

            tipo_doc = order.journal_id.sit_tipo_documento if order.journal_id and order.journal_id.sit_tipo_documento else None

            base_total = order.amount_untaxed

            if order.apply_retencion_renta_po:
                order.retencion_renta_amount_po = base_total * 0.10
                order.apply_renta_20_po = False
            elif order.apply_renta_20_po:
                order.retencion_renta_amount_po = base_total * 0.20

            _logger.info("base total %s", base_total)
            _logger.info(" order.retencion_renta_amount_po %s | Retencion 10: %s | Retencion 20: %s", order.retencion_renta_amount_po, order.apply_retencion_renta_po, order.apply_renta_20_po)

            # Retencion 1%
            retencion_contribuyente = config_utils.get_config_value(self.env, constants.config_retencion_venta, order.company_id.id)
            try:
                retencion_contribuyente = float(retencion_contribuyente) / 100.0
            except (TypeError, ValueError):
                retencion_contribuyente = 0.0

            # Retencion IVA
            iva_retencion = config_utils.get_config_value(self.env, constants.config_iva_rete, order.company_id.id)
            try:
                iva_retencion = float(iva_retencion) / 100.0
            except (TypeError, ValueError):
                iva_retencion = 0.0

            # IVA Percibido
            iva_percibido = config_utils.get_config_value(self.env, constants.config_iva_percibido_venta, order.company_id.id)
            try:
                iva_percibido = float(iva_percibido) / 100.0
            except (TypeError, ValueError):
                iva_percibido = 0.0
            _logger.info("SIT Retencion= %s, Retencion IVA= %s, IVA Percibido= %s", retencion_contribuyente, iva_retencion, iva_percibido)

            if order.apply_retencion_iva_po:
                if tipo_doc and tipo_doc.codigo == constants.COD_DTE_FSE:
                    retencion_iva = base_total * iva_retencion
                    order.retencion_iva_amount_po = float_round(retencion_iva, precision_rounding=order.currency_id.rounding)
                else:
                    retencion_iva = base_total * retencion_contribuyente
                    order.retencion_iva_amount_po = float_round(retencion_iva, precision_rounding=order.currency_id.rounding)
            else:
                order.retencion_iva_amount_po = 0.00

            if order.apply_iva_percibido_po:
                iva_percibido_amount = base_total * iva_percibido
                order.iva_percibido_amount_po = float_round(iva_percibido_amount, precision_rounding=order.currency_id.rounding)
            # else:
            #     order.iva_percibido_amount_po = 0.00

    @api.onchange('apply_renta_20_po')
    def _onchange_renta_20_purchase(self):
        _logger.info("[ONCHANGE-PURCHASE ORDER] Retencion (20): %s Retencion (10): %s", self.apply_renta_20_po, self.apply_retencion_renta_po)
        if self.apply_renta_20_po:
            self.apply_retencion_renta_po = False
        elif self.apply_retencion_renta_po:
            self.apply_renta_20_po = False
        else:
            self.apply_retencion_renta_po = False
            self.apply_renta_20_po = False

    @api.depends('amount_total', 'retencion_renta_amount_po', 'retencion_iva_amount_po', 'iva_percibido_amount_po', 'apply_renta_20_po')
    def _compute_total_con_retenciones(self):
        _logger.info("==== COMPUTE TOTAL CON RETENCIONES ====")

        for order in self:
            total_ret = (order.retencion_renta_amount_po + order.retencion_iva_amount_po)
            order.amount_total_retenciones_purchase = (order.amount_total + order.iva_percibido_amount_po) - total_ret

            _logger.info("Orden %s | total original=%s | retenciones=%s | total final=%s",
                order.id, order.amount_total, total_ret, order.amount_total_retenciones_purchase)

    # ── Banner: depende de apply_iva_percibido_po (ya calculado) ──────
    @api.depends('apply_iva_percibido_po', 'partner_id', 'journal_id', 'amount_untaxed')
    def _compute_advertencia_gran_contribuyente_purchase(self):
        for order in self:
            _logger.info("Filtros DTE -> company:%s | sit_fact:%s", order.company_id, order.company_id.sit_facturacion)

            if order.partner_id and order.partner_id.gran_contribuyente and order.amount_untaxed >= 100:
                order.advertencia_gran_contribuyente_purchase = _(
                    '<p><strong>⚠️ </strong>'
                    'El Proveedor <strong>%s</strong> es Gran Contribuyente. '
                    'IVA percibido ha sido aplicado automáticamente '
                    'y puede ser modificado si es necesario.</p>'
                ) % order.partner_id.name
            else:
                order.advertencia_gran_contribuyente_purchase = False
