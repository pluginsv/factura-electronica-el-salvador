import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ShopifyProduct(models.Model):
    _name = 'shopify.product'
    _description = 'Mapeo de Producto Shopify'
    _rec_name = 'shopify_title'

    instance_id = fields.Many2one('shopify.instance', string='Instancia',
                                  required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Producto Odoo')
    shopify_id = fields.Char(string='Shopify Product ID', index=True)
    shopify_variant_id = fields.Char(string='Shopify Variant ID', index=True)
    shopify_title = fields.Char(string='Titulo en Shopify')
    shopify_sku = fields.Char(string='SKU')
    shopify_price = fields.Float(string='Precio Shopify')
    shopify_inventory_qty = fields.Float(string='Qty Shopify')
    shopify_image_url = fields.Char(string='URL Imagen')
    synced = fields.Boolean(string='Sincronizado', default=False)
    last_sync = fields.Datetime(string='Ultima sincronizacion')

    _sql_constraints = [
        ('unique_variant_instance', 'unique(instance_id, shopify_variant_id)',
         'El variante de Shopify ya esta mapeado en esta instancia.'),
    ]

    @api.model
    def sync_products_from_shopify(self, instance):
        page_info = None
        total = 0
        while True:
            params = {'limit': 250}
            if page_info:
                params['page_info'] = page_info
            result = instance._shopify_request('GET', 'products.json', params=params)
            products = result.get('products', [])
            if not products:
                break
            for prod_data in products:
                total += self._process_shopify_product(instance, prod_data)
            # Paginacion Shopify (simplificada)
            if len(products) < 250:
                break
            page_info = None  # Shopify usa Link headers para paginacion
            break  # Salir por ahora, se puede mejorar con Link header parsing

        instance.last_product_sync = fields.Datetime.now()
        instance._create_log('info', 'sync_products',
                             f'{total} productos sincronizados')

    def _process_shopify_product(self, instance, prod_data):
        count = 0
        for variant in prod_data.get('variants', [{}]):
            shopify_variant_id = str(variant.get('id', ''))
            existing = self.search([
                ('instance_id', '=', instance.id),
                ('shopify_variant_id', '=', shopify_variant_id),
            ], limit=1)

            sku = variant.get('sku', '')
            title = prod_data.get('title', '')
            variant_title = variant.get('title', '')
            if variant_title and variant_title != 'Default Title':
                title = f"{title} - {variant_title}"

            vals = {
                'instance_id': instance.id,
                'shopify_id': str(prod_data.get('id', '')),
                'shopify_variant_id': shopify_variant_id,
                'shopify_title': title,
                'shopify_sku': sku,
                'shopify_price': float(variant.get('price', 0)),
                'shopify_inventory_qty': float(variant.get('inventory_quantity', 0)),
                'last_sync': fields.Datetime.now(),
                'synced': True,
            }

            # Imagen
            images = prod_data.get('images', [])
            if images:
                vals['shopify_image_url'] = images[0].get('src', '')

            if existing:
                existing.write(vals)
            else:
                # Buscar producto Odoo por SKU
                product = None
                if sku:
                    product = self.env['product.product'].search(
                        [('default_code', '=', sku)], limit=1)
                if not product:
                    # Crear producto
                    product = self.env['product.product'].create({
                        'name': title,
                        'default_code': sku,
                        'list_price': float(variant.get('price', 0)),
                        'type': 'product',
                    })
                vals['product_id'] = product.id
                self.create(vals)
            count += 1
        return count

    def _get_odoo_product(self, instance, shopify_variant_id, variant_data=None):
        mapping = self.search([
            ('instance_id', '=', instance.id),
            ('shopify_variant_id', '=', str(shopify_variant_id)),
        ], limit=1)
        if mapping and mapping.product_id:
            return mapping.product_id

        # Si no existe, buscar por SKU o crear
        if variant_data:
            sku = variant_data.get('sku', '')
            title = variant_data.get('title', variant_data.get('name', 'Producto Shopify'))
            price = float(variant_data.get('price', 0))

            product = None
            if sku:
                product = self.env['product.product'].search(
                    [('default_code', '=', sku)], limit=1)
            if not product:
                product = self.env['product.product'].create({
                    'name': title,
                    'default_code': sku,
                    'list_price': price,
                    'type': 'product',
                })

            self.create({
                'instance_id': instance.id,
                'product_id': product.id,
                'shopify_id': str(variant_data.get('product_id', '')),
                'shopify_variant_id': str(shopify_variant_id),
                'shopify_title': title,
                'shopify_sku': sku,
                'shopify_price': price,
                'synced': True,
                'last_sync': fields.Datetime.now(),
            })
            return product

        return None
