# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.common_utils.utils import config_utils
    _logger.info("SIT Modulo config_utils [hacienda -sale_order_line]")
except ImportError as e:
    _logger.error(f"Error al importar 'config_utils': {e}")
    config_utils = None
    s
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Impuestos permitidos según el diario de la cotización
    allowed_tax_ids = fields.Many2many(
        'account.tax',
        string='Impuestos permitidos (diario)',
        compute='_compute_allowed_tax_ids',
        store=False,
    )

    @api.depends('order_id.journal_id', 'order_id.journal_id.sit_tax_ids', 'product_id')
    def _compute_allowed_tax_ids(self):
        for line in self:
            _logger.info("=== [SOL COMPUTE ALLOWED TAX IDS] line=%s ===", line.id)

            company = line.order_id.company_id if line.order_id else None
            journal = line.order_id.journal_id
            tax_ids_journal = True if journal and journal.sit_tax_ids else False
            _logger.info("[SOL] Journal=%s | Impuesto del diario= %s", journal.id if journal else None, tax_ids_journal)

            # ----------------------------------------------------------------------
            # 1) Empresa NO usa facturación → usar impuestos estándar de Odoo
            # ----------------------------------------------------------------------
            if not company or not company.sit_facturacion or not tax_ids_journal:
                _logger.info("[SOL] Empresa NO usa facturación → usar comportamiento estándar de impuestos")

                # ✔️ Comportamiento estándar: permitir TODOS los impuestos
                if not company:
                    line.allowed_tax_ids = False
                    continue

                all_taxes = self.env['account.tax'].search([
                    ('company_id', '=', company.id),
                    ('type_tax_use', 'in', ['sale', 'none']),
                    ('active', '=', True)
                ])
                _logger.info("[SOL] Impuestos disponibles (estándar): %s", all_taxes.ids)

                line.allowed_tax_ids = all_taxes
                continue

            # ----------------------------------------------------------------------
            # 2) Empresa con facturación → usar impuestos definidos en el diario
            # ----------------------------------------------------------------------
            if journal and journal.sit_tax_ids:
                _logger.info("[SOL] Impuestos permitidos por diario: %s", journal.sit_tax_ids.ids)
                line.allowed_tax_ids = journal.sit_tax_ids
            else:
                _logger.info("[SOL] Diario sin impuestos configurados → sin taxes permitidos")
                line.allowed_tax_ids = False

    @api.onchange('order_id.journal_id', 'product_id')
    def _onchange_auto_set_taxes(self):
        for line in self:
            company = line.order_id.company_id
            journal = line.order_id.journal_id

            if not company or not company.sit_facturacion:
                return

            if journal and journal.sit_tax_ids:
                if not line.tax_id:
                    line.tax_id = journal.sit_tax_ids
