# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ReportCobros(models.Model):
    _name = "report.cobros"
    _description = "Reporte de Cobros / Pagos Recibidos"
    _auto = False
    _order = "payment_date desc"

    payment_date = fields.Date(string="Fecha de pago", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Cliente", readonly=True)
    invoice_user_id = fields.Many2one("res.users", string="Vendedor", readonly=True)
    move_name = fields.Char(string="Número de factura", readonly=True)
    payment_name = fields.Char(string="Número de pago", readonly=True)
    journal_id = fields.Many2one("account.journal", string="Método de pago", readonly=True)
    amount_paid = fields.Monetary(string="Monto pagado", readonly=True)
    amount_invoice = fields.Monetary(string="Total factura", readonly=True)
    amount_residual = fields.Monetary(string="Saldo pendiente", readonly=True)
    days_to_pay = fields.Integer(string="Días de cobro", readonly=True)
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
    payment_year = fields.Char(string="Año", readonly=True)
    payment_month = fields.Char(string="Mes", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY ap.id, am.id) AS id,
                    ap.date AS payment_date,
                    am.partner_id,
                    am.invoice_user_id,
                    am.name AS move_name,
                    apm.name AS payment_name,
                    apm.journal_id,
                    apr.amount AS amount_paid,
                    am.amount_total AS amount_invoice,
                    am.amount_residual,
                    CASE
                        WHEN am.invoice_date IS NOT NULL AND ap.date IS NOT NULL
                        THEN (ap.date - am.invoice_date)
                        ELSE 0
                    END AS days_to_pay,
                    am.payment_state,
                    am.currency_id,
                    am.company_id,
                    TO_CHAR(ap.date, 'YYYY') AS payment_year,
                    TO_CHAR(ap.date, 'MM') AS payment_month
                FROM account_payment ap
                JOIN account_move apm ON apm.id = ap.move_id
                JOIN account_move_line apml ON apml.move_id = apm.id
                JOIN account_partial_reconcile apr
                  ON apr.credit_move_id = apml.id OR apr.debit_move_id = apml.id
                JOIN account_move_line aml
                  ON (aml.id = apr.debit_move_id OR aml.id = apr.credit_move_id)
                  AND aml.id != apml.id
                JOIN account_move am ON am.id = aml.move_id
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                  AND am.state = 'posted'
                  AND apm.state = 'posted'
            )
            """ % self._table
        )
