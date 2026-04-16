import requests
import hmac
import hashlib
import base64
import json
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

SHOPIFY_API_VERSION = '2024-01'


class ShopifyInstance(models.Model):
    _name = 'shopify.instance'
    _description = 'Instancia de Tienda Shopify'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nombre de Tienda', required=True, tracking=True)
    shopify_url = fields.Char(
        string='URL de Shopify',
        required=True,
        help='URL de tu tienda Shopify, ej: mi-tienda.myshopify.com',
        tracking=True,
    )
    api_key = fields.Char(string='API Key', required=True)
    api_secret = fields.Char(string='API Secret')
    access_token = fields.Char(string='Access Token', required=True)
    webhook_secret = fields.Char(string='Webhook Secret')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('step1', 'Paso 1: Conexion'),
        ('step2', 'Paso 2: Productos'),
        ('step3', 'Paso 3: Clientes'),
        ('connected', 'Conectado'),
    ], default='draft', string='Estado', tracking=True)

    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string='Compania',
                                 default=lambda self: self.env.company)

    # Configuracion de sincronizacion
    auto_confirm_order = fields.Boolean(
        string='Confirmar orden automaticamente', default=True,
        help='Confirma la orden de venta automaticamente al importar de Shopify')
    auto_create_invoice = fields.Boolean(
        string='Crear factura automaticamente', default=True,
        help='Crea y valida la factura automaticamente al confirmar la orden')
    auto_register_payment = fields.Boolean(
        string='Registrar pago automaticamente', default=True,
        help='Registra el pago de la factura automaticamente si el pedido esta pagado en Shopify')
    auto_process_inventory = fields.Boolean(
        string='Procesar inventario automaticamente', default=True,
        help='Valida la transferencia de inventario automaticamente')
    notify_shopify_fulfillment = fields.Boolean(
        string='Notificar cumplimiento a Shopify', default=True,
        help='Envia la informacion de cumplimiento de vuelta a Shopify')
    sync_products = fields.Boolean(string='Sincronizar productos', default=True)
    sync_customers = fields.Boolean(string='Sincronizar clientes', default=True)

    # Mapeo por defecto
    warehouse_id = fields.Many2one('stock.warehouse', string='Almacen',
                                   default=lambda self: self.env['stock.warehouse'].search(
                                       [('company_id', '=', self.env.company.id)], limit=1))
    pricelist_id = fields.Many2one('product.pricelist', string='Lista de Precios')
    payment_journal_id = fields.Many2one('account.journal', string='Diario de Pagos',
                                         domain=[('type', 'in', ['bank', 'cash'])])
    sales_team_id = fields.Many2one('crm.team', string='Equipo de Ventas')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Posicion Fiscal')

    # KPI Email
    kpi_email_enabled = fields.Boolean(string='Enviar resumen KPI por email', default=False)
    kpi_email_to = fields.Char(string='Email destino KPI')
    kpi_email_frequency = fields.Selection([
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
    ], string='Frecuencia', default='daily')

    # Contadores
    order_count = fields.Integer(compute='_compute_counts', string='Pedidos')
    product_count = fields.Integer(compute='_compute_counts', string='Productos')
    customer_count = fields.Integer(compute='_compute_counts', string='Clientes')

    # Ultima sincronizacion
    last_order_sync = fields.Datetime(string='Ultima sync pedidos')
    last_product_sync = fields.Datetime(string='Ultima sync productos')
    last_customer_sync = fields.Datetime(string='Ultima sync clientes')

    @api.depends()
    def _compute_counts(self):
        for rec in self:
            rec.order_count = self.env['shopify.order'].search_count(
                [('instance_id', '=', rec.id)])
            rec.product_count = self.env['shopify.product'].search_count(
                [('instance_id', '=', rec.id)])
            rec.customer_count = self.env['shopify.customer'].search_count(
                [('instance_id', '=', rec.id)])

    # ──────────────────────────────────────────────────
    # API Shopify
    # ──────────────────────────────────────────────────

    def _get_headers(self):
        self.ensure_one()
        return {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': self.access_token,
        }

    def _get_base_url(self):
        self.ensure_one()
        url = self.shopify_url.strip().rstrip('/')
        if not url.startswith('https://'):
            url = 'https://' + url
        return f"{url}/admin/api/{SHOPIFY_API_VERSION}"

    def _shopify_request(self, method, endpoint, data=None, params=None):
        self.ensure_one()
        url = f"{self._get_base_url()}/{endpoint}"
        headers = self._get_headers()
        try:
            response = requests.request(
                method, url, headers=headers,
                json=data, params=params, timeout=30,
            )
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
        except requests.exceptions.HTTPError as e:
            error_msg = str(e)
            try:
                error_data = e.response.json()
                error_msg = json.dumps(error_data.get('errors', error_data), indent=2)
            except Exception:
                pass
            self._create_log('error', endpoint, error_msg)
            raise UserError(_('Error de Shopify API: %s') % error_msg)
        except requests.exceptions.ConnectionError:
            raise UserError(_('No se pudo conectar a Shopify. Verifica la URL de la tienda.'))
        except requests.exceptions.Timeout:
            raise UserError(_('Tiempo de espera agotado al conectar con Shopify.'))

    def _create_log(self, log_type, operation, message, shopify_id=None):
        self.ensure_one()
        self.env['shopify.log'].create({
            'instance_id': self.id,
            'log_type': log_type,
            'operation': operation,
            'message': message,
            'shopify_id': shopify_id,
        })

    # ──────────────────────────────────────────────────
    # Acciones de conexion
    # ──────────────────────────────────────────────────

    def action_test_connection(self):
        self.ensure_one()
        try:
            result = self._shopify_request('GET', 'shop.json')
            shop = result.get('shop', {})
            self.name = shop.get('name', self.name)
            self.state = 'step1'
            self._create_log('info', 'test_connection',
                             f"Conexion exitosa: {shop.get('name')}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Conexion Exitosa'),
                    'message': _('Conectado a: %s') % shop.get('name'),
                    'type': 'success',
                    'sticky': False,
                }
            }
        except UserError:
            self.state = 'draft'
            raise

    def action_sync_products(self):
        self.ensure_one()
        self.env['shopify.product'].sync_products_from_shopify(self)
        if self.state == 'step1':
            self.state = 'step2'

    def action_sync_customers(self):
        self.ensure_one()
        self.env['shopify.customer'].sync_customers_from_shopify(self)
        if self.state == 'step2':
            self.state = 'step3'

    def action_activate(self):
        self.ensure_one()
        self.state = 'connected'
        self._create_log('info', 'activate', 'Instancia activada y lista para sincronizar')

    def action_sync_orders(self):
        self.ensure_one()
        self.env['shopify.order'].sync_orders_from_shopify(self)

    def action_full_sync(self):
        self.ensure_one()
        if self.sync_products:
            self.action_sync_products()
        if self.sync_customers:
            self.action_sync_customers()
        self.action_sync_orders()

    # ──────────────────────────────────────────────────
    # Botones smart buttons
    # ──────────────────────────────────────────────────

    def action_view_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Pedidos Shopify'),
            'res_model': 'shopify.order',
            'view_mode': 'tree,form',
            'domain': [('instance_id', '=', self.id)],
        }

    def action_view_products(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Productos Shopify'),
            'res_model': 'shopify.product',
            'view_mode': 'tree,form',
            'domain': [('instance_id', '=', self.id)],
        }

    def action_view_customers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Clientes Shopify'),
            'res_model': 'shopify.customer',
            'view_mode': 'tree,form',
            'domain': [('instance_id', '=', self.id)],
        }

    # ──────────────────────────────────────────────────
    # KPI Email
    # ──────────────────────────────────────────────────

    def _send_kpi_email(self):
        self.ensure_one()
        if not self.kpi_email_enabled or not self.kpi_email_to:
            return

        today = fields.Date.today()
        if self.kpi_email_frequency == 'daily':
            date_from = fields.Datetime.to_datetime(today)
            date_range = str(today)
        elif self.kpi_email_frequency == 'weekly':
            date_from = fields.Datetime.to_datetime(
                today - __import__('datetime').timedelta(days=7))
            date_range = f"Semana {today.isocalendar()[1]}"
        else:
            date_from = fields.Datetime.to_datetime(today.replace(day=1))
            date_range = today.strftime('%B %Y')

        orders = self.env['shopify.order'].search([
            ('instance_id', '=', self.id),
            ('create_date', '>=', date_from),
        ])
        error_orders = orders.filtered(lambda o: o.state == 'error')
        new_customers = self.env['shopify.customer'].search_count([
            ('instance_id', '=', self.id),
            ('create_date', '>=', date_from),
        ])

        ctx = {
            'total_orders': len(orders),
            'total_amount': sum(orders.mapped('shopify_total')),
            'error_orders': len(error_orders),
            'new_customers': new_customers,
            'total_products': self.product_count,
            'date_range': date_range,
        }

        template = self.env.ref('shopify_fast_connector.mail_template_shopify_kpi')
        template.with_context(**ctx).send_mail(self.id, force_send=True)

    # ──────────────────────────────────────────────────
    # Webhook verification
    # ──────────────────────────────────────────────────

    def verify_webhook(self, data, hmac_header):
        self.ensure_one()
        if not self.webhook_secret:
            return True
        digest = hmac.new(
            self.webhook_secret.encode('utf-8'),
            data,
            hashlib.sha256,
        ).digest()
        computed_hmac = base64.b64encode(digest).decode('utf-8')
        return hmac.compare_digest(computed_hmac, hmac_header)
