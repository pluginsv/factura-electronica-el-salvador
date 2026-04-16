# -*- coding: utf-8 -*-
from odoo import fields, models, tools


class ReportProductosVendidos(models.Model):
    _name = "report.productos.vendidos"
    _description = "Reporte de Productos más Vendidos"
    _auto = False
    _order = "total_revenue desc"

    product_id = fields.Many2one("product.product", string="Producto", readonly=True)
    product_categ_id = fields.Many2one("product.category", string="Categoría", readonly=True)
    quantity_sold = fields.Float(string="Cantidad vendida", readonly=True)
    total_revenue = fields.Monetary(string="Ingreso total", readonly=True)
    avg_unit_price = fields.Monetary(string="Precio promedio", readonly=True)
    invoice_count = fields.Integer(string="Cantidad de facturas", readonly=True)
    partner_count = fields.Integer(string="Clientes distintos", readonly=True)
    period = fields.Char(string="Periodo (YYYY-MM)", readonly=True)
    invoice_year = fields.Char(string="Año", readonly=True)
    invoice_month = fields.Char(string="Mes", readonly=True)
    currency_id = fields.Many2one("res.currency", string="Moneda", readonly=True)
    company_id = fields.Many2one("res.company", string="Compañía", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    ROW_NUMBER() OVER (
                        ORDER BY aml.product_id, TO_CHAR(am.invoice_date, 'YYYY-MM')
                    ) AS id,
                    aml.product_id,
                    pt.categ_id AS product_categ_id,
                    SUM(aml.quantity) AS quantity_sold,
                    SUM(aml.price_subtotal) AS total_revenue,
                    CASE
                        WHEN SUM(aml.quantity) > 0
                        THEN SUM(aml.price_subtotal) / SUM(aml.quantity)
                        ELSE 0
                    END AS avg_unit_price,
                    COUNT(DISTINCT am.id) AS invoice_count,
                    COUNT(DISTINCT am.partner_id) AS partner_count,
                    TO_CHAR(am.invoice_date, 'YYYY-MM') AS period,
                    TO_CHAR(am.invoice_date, 'YYYY') AS invoice_year,
                    TO_CHAR(am.invoice_date, 'MM') AS invoice_month,
                    MAX(am.currency_id) AS currency_id,
                    am.company_id
                FROM account_move_line aml
                JOIN account_move am ON am.id = aml.move_id
                JOIN product_product pp ON pp.id = aml.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE am.move_type IN ('out_invoice', 'out_refund')
                  AND am.state = 'posted'
                  AND aml.product_id IS NOT NULL
                  AND aml.display_type = 'product'
                GROUP BY
                    aml.product_id,
                    pt.categ_id,
                    TO_CHAR(am.invoice_date, 'YYYY-MM'),
                    TO_CHAR(am.invoice_date, 'YYYY'),
                    TO_CHAR(am.invoice_date, 'MM'),
                    am.company_id
            )
            """ % self._table
        )
