import json
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ShopifyWebhookController(http.Controller):

    @http.route('/shopify/webhook/order/create', type='json', auth='none',
                methods=['POST'], csrf=False)
    def webhook_order_create(self):
        return self._handle_order_webhook('order_create')

    @http.route('/shopify/webhook/order/updated', type='json', auth='none',
                methods=['POST'], csrf=False)
    def webhook_order_updated(self):
        return self._handle_order_webhook('order_updated')

    @http.route('/shopify/webhook/product/update', type='json', auth='none',
                methods=['POST'], csrf=False)
    def webhook_product_update(self):
        data = request.jsonrequest
        hmac_header = request.httprequest.headers.get('X-Shopify-Hmac-Sha256', '')
        shop_domain = request.httprequest.headers.get('X-Shopify-Shop-Domain', '')

        instance = self._find_instance(shop_domain)
        if not instance:
            _logger.warning("Webhook producto: instancia no encontrada para %s", shop_domain)
            return {'status': 'ignored'}

        if not instance.verify_webhook(request.httprequest.get_data(), hmac_header):
            _logger.warning("Webhook producto: HMAC invalido")
            return {'status': 'unauthorized'}

        try:
            env = request.env(su=True)
            env['shopify.product']._process_shopify_product(instance, data)
            instance._create_log('info', 'webhook_product',
                                 f"Producto actualizado via webhook: {data.get('title', '')}",
                                 str(data.get('id', '')))
        except Exception as e:
            _logger.error("Error webhook producto: %s", str(e))
            instance._create_log('error', 'webhook_product', str(e),
                                 str(data.get('id', '')))

        return {'status': 'ok'}

    def _handle_order_webhook(self, operation):
        data = request.jsonrequest
        hmac_header = request.httprequest.headers.get('X-Shopify-Hmac-Sha256', '')
        shop_domain = request.httprequest.headers.get('X-Shopify-Shop-Domain', '')

        instance = self._find_instance(shop_domain)
        if not instance:
            _logger.warning("Webhook %s: instancia no encontrada para %s",
                            operation, shop_domain)
            return {'status': 'ignored'}

        if not instance.verify_webhook(request.httprequest.get_data(), hmac_header):
            _logger.warning("Webhook %s: HMAC invalido", operation)
            return {'status': 'unauthorized'}

        try:
            env = request.env(su=True)
            env['shopify.order']._process_shopify_order(instance, data)
            instance._create_log('info', f'webhook_{operation}',
                                 f"Orden procesada via webhook: {data.get('name', '')}",
                                 str(data.get('id', '')))
        except Exception as e:
            _logger.error("Error webhook %s: %s", operation, str(e))
            instance._create_log('error', f'webhook_{operation}', str(e),
                                 str(data.get('id', '')))

        return {'status': 'ok'}

    def _find_instance(self, shop_domain):
        if not shop_domain:
            return None
        env = request.env(su=True)
        return env['shopify.instance'].search([
            ('shopify_url', 'ilike', shop_domain),
            ('state', '=', 'connected'),
        ], limit=1)
