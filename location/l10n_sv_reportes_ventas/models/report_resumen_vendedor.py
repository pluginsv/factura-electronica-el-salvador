# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ReportResumenVendedor(models.Model):
    _name = "report.resumen.vendedor"
    _description = "Reporte Resumen por Vendedor"
    _auto = False
    _order = "period desc, total_invoiced desc"

    invoice_user_id = fields.Many2one("res.users", string="Vendedor", readonly=True)
    team_id = fields.Many2one("crm.team", string="Equipo de ventas", readonly=True)
    period = fields.Char(string="Periodo (YYYY-MM)", readonly=True)
    invoice_year = fields.Char(string="Año", readonly=True)
    invoice_month = fields.Char(string="Mes", readonly=True)
    total_invoiced = fields.Monetary(string="Total facturado", readonly=True)
    total_collected = fields.Monetary(string="Total cobrado", readonly=True)
    total_pending = fields.Monetary(string="Total pendiente", readonly=True)
    invoice_count = fields.Integer(string="Cantidad de facturas", readonly=True)
    collection_rate = fields.Float(string="% de cobro", readonly=True, digits=(5, 2))
    currency_id = fields.Many2one("res.currency", string="Moneda", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    ROW_NUMBER() OVER (
                        ORDER BY am.invoice_user_id, TO_CHAR(am.invoice_date, 'YYYY-MM')
                    ) AS id,
                    am.invoice_user_id,
                    MAX(am.team_id) AS team_id,
                    TO_CHAR(am.invoice_date, 'YYYY-MM') AS period,
                    TO_CHAR(am.invoice_date, 'YYYY') AS invoice_year,
                    TO_CHAR(am.invoice_date, 'MM') AS invoice_month,
                    SUM(am.amount_total) AS total_invoiced,
                    SUM(am.amount_total - am.amount_residual) AS total_collected,
                    SUM(am.amount_residual) AS total_pending,
                    COUNT(am.id) AS invoice_count,
                    CASE
                        WHEN SUM(am.amount_total) > 0
                        THEN (SUM(am.amount_total - am.amount_residual) / SUM(am.amount_total)) * 100
                        ELSE 0
                    END AS collection_rate,
                    MAX(am.currency_id) AS currency_id,
                    am.company_id
                FROM account_move am
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                  AND am.state = 'posted'
                  AND am.invoice_date IS NOT NULL
                GROUP BY
                    am.invoice_user_id,
                    TO_CHAR(am.invoice_date, 'YYYY-MM'),
                    TO_CHAR(am.invoice_date, 'YYYY'),
                    TO_CHAR(am.invoice_date, 'MM'),
                    am.company_id
            )
            """ % self._table
        )
