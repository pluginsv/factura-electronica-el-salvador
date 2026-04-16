from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ShopifySetupWizard(models.TransientModel):
    _name = 'shopify.setup.wizard'
    _description = 'Asistente de Configuracion Shopify'

    instance_id = fields.Many2one('shopify.instance', string='Instancia')
    step = fields.Selection([
        ('1', 'Paso 1: Conexion'),
        ('2', 'Paso 2: Sincronizar Productos'),
        ('3', 'Paso 3: Sincronizar Clientes'),
        ('4', 'Paso 4: Configuracion Final'),
    ], default='1', string='Paso')

    # Paso 1
    shopify_url = fields.Char(string='URL Tienda Shopify')
    access_token = fields.Char(string='Access Token')
    api_key = fields.Char(string='API Key')

    # Paso 4
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen')
    payment_journal_id = fields.Many2one('account.journal', string='Diario de Pagos',
                                         domain=[('type', 'in', ['bank', 'cash'])])
    auto_confirm = fields.Boolean(string='Confirmar ordenes automaticamente', default=True)
    auto_invoice = fields.Boolean(string='Crear facturas automaticamente', default=True)
    auto_payment = fields.Boolean(string='Registrar pagos automaticamente', default=True)

    def action_next(self):
        self.ensure_one()
        if self.step == '1':
            # Crear o actualizar instancia y probar conexion
            if not self.instance_id:
                self.instance_id = self.env['shopify.instance'].create({
                    'name': self.shopify_url or 'Mi Tienda',
                    'shopify_url': self.shopify_url,
                    'access_token': self.access_token,
                    'api_key': self.api_key or '',
                })
            else:
                self.instance_id.write({
                    'shopify_url': self.shopify_url,
                    'access_token': self.access_token,
                    'api_key': self.api_key or '',
                })
            self.instance_id.action_test_connection()
            self.step = '2'

        elif self.step == '2':
            self.instance_id.action_sync_products()
            self.step = '3'

        elif self.step == '3':
            self.instance_id.action_sync_customers()
            self.step = '4'

        elif self.step == '4':
            self.instance_id.write({
                'warehouse_id': self.warehouse_id.id if self.warehouse_id else False,
                'payment_journal_id': self.payment_journal_id.id if self.payment_journal_id else False,
                'auto_confirm_order': self.auto_confirm,
                'auto_create_invoice': self.auto_invoice,
                'auto_register_payment': self.auto_payment,
            })
            self.instance_id.action_activate()
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'shopify.instance',
                'res_id': self.instance_id.id,
                'view_mode': 'form',
                'target': 'current',
            }

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'shopify.setup.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
