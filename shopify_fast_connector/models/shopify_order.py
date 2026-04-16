import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ShopifyOrder(models.Model):
    _name = 'shopify.order'
    _description = 'Pedido Shopify'
    _rec_name = 'shopify_order_name'
    _order = 'create_date desc'

    instance_id = fields.Many2one('shopify.instance', string='Instancia',
                                  required=True, ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', string='Orden de Venta')
    invoice_id = fields.Many2one('account.move', string='Factura')

    shopify_id = fields.Char(string='Shopify Order ID', index=True)
    shopify_order_name = fields.Char(string='Numero de Orden')
    shopify_order_number = fields.Integer(string='Order Number')
    shopify_financial_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('authorized', 'Autorizado'),
        ('partially_paid', 'Parcialmente Pagado'),
        ('paid', 'Pagado'),
        ('partially_refunded', 'Parcialmente Reembolsado'),
        ('refunded', 'Reembolsado'),
        ('voided', 'Anulado'),
    ], string='Estado Financiero')
    shopify_fulfillment_status = fields.Selection([
        ('unfulfilled', 'Sin Cumplir'),
        ('partial', 'Parcial'),
        ('fulfilled', 'Cumplido'),
    ], string='Estado Cumplimiento', default='unfulfilled')

    shopify_total = fields.Float(string='Total Shopify')
    shopify_subtotal = fields.Float(string='Subtotal')
    shopify_tax = fields.Float(string='Impuestos')
    shopify_shipping = fields.Float(string='Envio')
    shopify_discount = fields.Float(string='Descuento')
    shopify_currency = fields.Char(string='Moneda')
    shopify_created_at = fields.Datetime(string='Creado en Shopify')

    state = fields.Selection([
        ('draft', 'Borrador'),
        ('order_created', 'Orden Creada'),
        ('order_confirmed', 'Orden Confirmada'),
        ('invoiced', 'Facturado'),
        ('paid', 'Pagado'),
        ('fulfilled', 'Cumplido'),
        ('done', 'Completado'),
        ('error', 'Error'),
    ], default='draft', string='Estado')
    error_message = fields.Text(string='Mensaje de Error')

    _sql_constraints = [
        ('unique_order_instance', 'unique(instance_id, shopify_id)',
         'El pedido de Shopify ya existe en esta instancia.'),
    ]

    # ──────────────────────────────────────────────────
    # Sincronizacion de ordenes
    # ──────────────────────────────────────────────────

    @api.model
    def sync_orders_from_shopify(self, instance):
        params = {
            'status': 'any',
            'limit': 250,
        }
        if instance.last_order_sync:
            params['updated_at_min'] = instance.last_order_sync.isoformat()

        result = instance._shopify_request('GET', 'orders.json', params=params)
        orders = result.get('orders', [])
        count = 0
        errors = 0
        for order_data in orders:
            try:
                self._process_shopify_order(instance, order_data)
                count += 1
            except Exception as e:
                errors += 1
                _logger.error("Error procesando orden Shopify %s: %s",
                              order_data.get('name', ''), str(e))
                instance._create_log('error', 'sync_order',
                                     f"Error en orden {order_data.get('name', '')}: {str(e)}",
                                     str(order_data.get('id', '')))

        instance.last_order_sync = fields.Datetime.now()
        instance._create_log('info', 'sync_orders',
                             f'{count} ordenes sincronizadas, {errors} errores')

    def _process_shopify_order(self, instance, order_data):
        shopify_id = str(order_data.get('id', ''))
        existing = self.search([
            ('instance_id', '=', instance.id),
            ('shopify_id', '=', shopify_id),
        ], limit=1)

        if existing and existing.state in ('done', 'fulfilled', 'paid'):
            return existing

        vals = self._prepare_order_vals(instance, order_data)

        if existing:
            existing.write(vals)
            order_rec = existing
        else:
            order_rec = self.create(vals)

        # Ejecutar flujo automatico
        if not existing or existing.state == 'draft':
            order_rec._execute_auto_flow(instance, order_data)

        return order_rec

    def _prepare_order_vals(self, instance, order_data):
        fulfillment_status = order_data.get('fulfillment_status') or 'unfulfilled'
        return {
            'instance_id': instance.id,
            'shopify_id': str(order_data.get('id', '')),
            'shopify_order_name': order_data.get('name', ''),
            'shopify_order_number': order_data.get('order_number', 0),
            'shopify_financial_status': order_data.get('financial_status', 'pending'),
            'shopify_fulfillment_status': fulfillment_status,
            'shopify_total': float(order_data.get('total_price', 0)),
            'shopify_subtotal': float(order_data.get('subtotal_price', 0)),
            'shopify_tax': float(order_data.get('total_tax', 0)),
            'shopify_shipping': sum(
                float(s.get('price', 0))
                for s in order_data.get('shipping_lines', [])
            ),
            'shopify_discount': abs(float(order_data.get('total_discounts', 0))),
            'shopify_currency': order_data.get('currency', ''),
            'shopify_created_at': order_data.get('created_at', '').replace('T', ' ')[:19]
            if order_data.get('created_at') else False,
        }

    # ──────────────────────────────────────────────────
    # Flujo automatico completo
    # ──────────────────────────────────────────────────

    def _execute_auto_flow(self, instance, order_data):
        self.ensure_one()
        try:
            # 1. Crear orden de venta
            sale_order = self._create_sale_order(instance, order_data)
            self.sale_order_id = sale_order.id
            self.state = 'order_created'

            # 2. Confirmar orden
            if instance.auto_confirm_order:
                sale_order.action_confirm()
                self.state = 'order_confirmed'

                # 3. Crear factura
                if instance.auto_create_invoice:
                    invoice = self._create_invoice(sale_order)
                    self.invoice_id = invoice.id
                    self.state = 'invoiced'

                    # 4. Registrar pago
                    if (instance.auto_register_payment and
                            self.shopify_financial_status == 'paid'):
                        self._register_payment(instance, invoice)
                        self.state = 'paid'

                # 5. Procesar inventario (las transferencias se crean al confirmar)
                if instance.auto_process_inventory:
                    self._process_inventory(sale_order)

                # 6. Notificar cumplimiento a Shopify
                if instance.notify_shopify_fulfillment:
                    self._notify_fulfillment(instance)
                    self.state = 'done'

            instance._create_log('info', 'order_flow',
                                 f"Orden {self.shopify_order_name} procesada completamente",
                                 self.shopify_id)

        except Exception as e:
            self.state = 'error'
            self.error_message = str(e)
            instance._create_log('error', 'order_flow',
                                 f"Error en orden {self.shopify_order_name}: {str(e)}",
                                 self.shopify_id)
            raise

    def _create_sale_order(self, instance, order_data):
        self.ensure_one()
        # Obtener o crear partner
        customer_data = order_data.get('customer', {})
        partner = self.env['shopify.customer']._get_or_create_partner(
            instance, customer_data)

        if not partner:
            # Crear partner desde datos de la orden
            billing = order_data.get('billing_address', {})
            partner = self.env['res.partner'].create({
                'name': f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip()
                        or order_data.get('email', 'Cliente Shopify'),
                'email': order_data.get('email', ''),
                'phone': order_data.get('phone', ''),
                'customer_rank': 1,
            })

        # Preparar lineas
        order_lines = []
        for line in order_data.get('line_items', []):
            product = self.env['shopify.product']._get_odoo_product(
                instance,
                line.get('variant_id', ''),
                variant_data={
                    'id': line.get('variant_id', ''),
                    'product_id': line.get('product_id', ''),
                    'title': line.get('title', 'Producto'),
                    'name': line.get('name', line.get('title', 'Producto')),
                    'sku': line.get('sku', ''),
                    'price': line.get('price', 0),
                },
            )
            if product:
                discount_pct = 0.0
                if line.get('discount_allocations'):
                    total_discount = sum(
                        float(d.get('amount', 0))
                        for d in line['discount_allocations']
                    )
                    line_total = float(line.get('price', 0)) * int(line.get('quantity', 1))
                    if line_total > 0:
                        discount_pct = (total_discount / line_total) * 100

                order_lines.append((0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': int(line.get('quantity', 1)),
                    'price_unit': float(line.get('price', 0)),
                    'discount': discount_pct,
                    'name': line.get('name', product.name),
                }))

        # Linea de envio
        for shipping in order_data.get('shipping_lines', []):
            shipping_price = float(shipping.get('price', 0))
            if shipping_price > 0:
                shipping_product = self._get_shipping_product()
                order_lines.append((0, 0, {
                    'product_id': shipping_product.id,
                    'product_uom_qty': 1,
                    'price_unit': shipping_price,
                    'name': shipping.get('title', 'Envio'),
                }))

        so_vals = {
            'partner_id': partner.id,
            'order_line': order_lines,
            'client_order_ref': self.shopify_order_name,
            'company_id': instance.company_id.id,
        }

        if instance.warehouse_id:
            so_vals['warehouse_id'] = instance.warehouse_id.id
        if instance.pricelist_id:
            so_vals['pricelist_id'] = instance.pricelist_id.id
        if instance.fiscal_position_id:
            so_vals['fiscal_position_id'] = instance.fiscal_position_id.id
        if instance.sales_team_id:
            so_vals['team_id'] = instance.sales_team_id.id

        return self.env['sale.order'].create(so_vals)

    def _get_shipping_product(self):
        product = self.env.ref(
            'shopify_fast_connector.product_shopify_shipping', raise_if_not_found=False)
        if not product:
            product = self.env['product.product'].search(
                [('default_code', '=', 'SHOPIFY-SHIPPING')], limit=1)
        if not product:
            product = self.env['product.product'].create({
                'name': 'Costo de Envio Shopify',
                'default_code': 'SHOPIFY-SHIPPING',
                'type': 'service',
                'list_price': 0,
                'invoice_policy': 'order',
            })
        return product

    def _create_invoice(self, sale_order):
        invoice = sale_order._create_invoices()
        invoice.action_post()
        return invoice

    def _register_payment(self, instance, invoice):
        if not instance.payment_journal_id:
            return

        payment_register = self.env['account.payment.register'].with_context(
            active_model='account.move',
            active_ids=invoice.ids,
        ).create({
            'journal_id': instance.payment_journal_id.id,
        })
        payment_register.action_create_payments()

    def _process_inventory(self, sale_order):
        for picking in sale_order.picking_ids.filtered(
                lambda p: p.state not in ('done', 'cancel')):
            for move in picking.move_ids:
                move.quantity = move.product_uom_qty
            picking.button_validate()

    def _notify_fulfillment(self, instance):
        self.ensure_one()
        if not self.shopify_id:
            return

        # Obtener tracking si existe
        tracking_numbers = []
        tracking_urls = []
        if self.sale_order_id:
            for picking in self.sale_order_id.picking_ids.filtered(
                    lambda p: p.state == 'done'):
                if picking.carrier_tracking_ref:
                    tracking_numbers.append(picking.carrier_tracking_ref)

        line_items = []
        try:
            result = instance._shopify_request(
                'GET', f'orders/{self.shopify_id}.json')
            order_data = result.get('order', {})
            for line in order_data.get('line_items', []):
                line_items.append({'id': line['id'], 'quantity': line['quantity']})
        except Exception:
            pass

        if not line_items:
            return

        fulfillment_data = {
            'fulfillment': {
                'line_items_by_fulfillment_order': [{
                    'fulfillment_order_id': self.shopify_id,
                }],
                'notify_customer': True,
            }
        }
        if tracking_numbers:
            fulfillment_data['fulfillment']['tracking_info'] = {
                'number': tracking_numbers[0],
            }

        try:
            instance._shopify_request(
                'POST', 'fulfillments.json', data=fulfillment_data)
            self.shopify_fulfillment_status = 'fulfilled'
            instance._create_log('info', 'fulfillment',
                                 f"Cumplimiento enviado para {self.shopify_order_name}",
                                 self.shopify_id)
        except Exception as e:
            _logger.warning("No se pudo enviar cumplimiento a Shopify: %s", str(e))
