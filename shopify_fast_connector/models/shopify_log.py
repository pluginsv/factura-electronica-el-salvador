from odoo import models, fields


class ShopifyLog(models.Model):
    _name = 'shopify.log'
    _description = 'Log de Shopify'
    _order = 'create_date desc'

    instance_id = fields.Many2one('shopify.instance', string='Instancia',
                                  required=True, ondelete='cascade')
    log_type = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Advertencia'),
        ('error', 'Error'),
    ], string='Tipo', default='info')
    operation = fields.Char(string='Operacion')
    message = fields.Text(string='Mensaje')
    shopify_id = fields.Char(string='Shopify ID')
    create_date = fields.Datetime(string='Fecha', readonly=True)
