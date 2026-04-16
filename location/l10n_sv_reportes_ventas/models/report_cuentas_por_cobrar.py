# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ReportCuentasPorCobrar(models.Model):
    _name = "report.cuentas.por.cobrar"
    _description = "Reporte de Cuentas por Cobrar (Antigüedad de Saldos)"
    _auto = False
    _order = "days_overdue desc"

    partner_id = fields.Many2one("res.partner", string="Cliente", readonly=True)
    invoice_user_id = fields.Many2one("res.users", string="Vendedor", readonly=True)
    name = fields.Char(string="Número de factura", readonly=True)
    invoice_date = fields.Date(string="Fecha de emisión", readonly=True)
    invoice_date_due = fields.Date(string="Fecha de vencimiento", readonly=True)
    amount_total = fields.Monetary(string="Total facturado", readonly=True)
    amount_residual = fields.Monetary(string="Saldo pendiente", readonly=True)
    days_overdue = fields.Integer(string="Días vencido", readonly=True)
    range_due = fields.Selection(
        selection=[
            ("vigente", "Vigente"),
            ("1_30", "1-30 días"),
            ("31_60", "31-60 días"),
            ("61_90", "61-90 días"),
            ("90_plus", "90+ días"),
        ],
        string="Rango de antigüedad",
        readonly=True,
    )
    payment_state = fields.Selection(
        selection=[
            ("not_paid", "No pagado"),
            ("in_payment", "En proceso"),
            ("paid", "Pagado"),
            ("partial", "Parcial"),
            ("reversed", "Revertido"),
        ],
        string="Estado de pago",
        readonly=True,
    )
    currency_id = fields.Many2one("res.currency", string="Moneda", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    am.id AS id,
                    am.partner_id,
                    am.invoice_user_id,
                    am.name,
                    am.invoice_date,
                    am.invoice_date_due,
                    am.amount_total,
                    am.amount_residual,
                    CASE
                        WHEN am.invoice_date_due IS NULL THEN 0
                        WHEN am.invoice_date_due >= CURRENT_DATE THEN 0
                        ELSE (CURRENT_DATE - am.invoice_date_due)
                    END AS days_overdue,
                    CASE
                        WHEN am.invoice_date_due IS NULL OR am.invoice_date_due >= CURRENT_DATE THEN 'vigente'
                        WHEN (CURRENT_DATE - am.invoice_date_due) BETWEEN 1 AND 30 THEN '1_30'
                        WHEN (CURRENT_DATE - am.invoice_date_due) BETWEEN 31 AND 60 THEN '31_60'
                        WHEN (CURRENT_DATE - am.invoice_date_due) BETWEEN 61 AND 90 THEN '61_90'
                        ELSE '90_plus'
                    END AS range_due,
                    am.payment_state,
                    am.currency_id,
                    am.company_id
                FROM account_move am
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                  AND am.state = 'posted'
                  AND am.payment_state IN ('not_paid', 'partial')
                  AND am.amount_residual > 0
            )
            """ % self._table
        )
