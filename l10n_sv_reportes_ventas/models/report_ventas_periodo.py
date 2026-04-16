# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ReportVentasPeriodo(models.Model):
    _name = "report.ventas.periodo"
    _description = "Reporte de Ventas por Periodo"
    _auto = False
    _order = "invoice_date desc"

    invoice_date = fields.Date(string="Fecha de emisión", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", readonly=True)
    invoice_user_id = fields.Many2one("res.users", string="Vendedor", readonly=True)
    team_id = fields.Many2one("crm.team", string="Equipo de ventas", readonly=True)
    name = fields.Char(string="Número de factura", readonly=True)
    codigo_tipo_documento = fields.Char(string="Tipo de documento", readonly=True)
    amount_untaxed = fields.Monetary(string="Subtotal", readonly=True)
    amount_tax = fields.Monetary(string="IVA", readonly=True)
    amount_total = fields.Monetary(string="Total facturado", readonly=True)
    amount_residual = fields.Monetary(string="Saldo pendiente", readonly=True)
    amount_paid = fields.Monetary(string="Monto cobrado", readonly=True)
    payment_state = fields.Selection(
        selection=[
            ("not_paid", "No pagado"),
            ("in_payment", "En proceso"),
            ("paid", "Pagado"),
            ("partial", "Parcial"),
            ("reversed", "Revertido"),
            ("invoicing_legacy", "Legacy"),
        ],
        string="Estado de pago",
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("posted", "Publicado"),
            ("cancel", "Cancelado"),
        ],
        string="Estado",
        readonly=True,
    )
    currency_id = fields.Many2one("res.currency", string="Moneda", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)
    invoice_year = fields.Char(string="Año", readonly=True)
    invoice_month = fields.Char(string="Mes", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    am.id AS id,
                    am.invoice_date,
                    am.partner_id,
                    am.invoice_user_id,
                    am.team_id,
                    am.name,
                    am.codigo_tipo_documento,
                    am.amount_untaxed,
                    am.amount_tax,
                    am.amount_total,
                    am.amount_residual,
                    (am.amount_total - am.amount_residual) AS amount_paid,
                    am.payment_state,
                    am.state,
                    am.currency_id,
                    am.company_id,
                    TO_CHAR(am.invoice_date, 'YYYY') AS invoice_year,
                    TO_CHAR(am.invoice_date, 'MM') AS invoice_month
                FROM account_move am
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                  AND am.state = 'posted'
            )
            """ % self._table
        )
