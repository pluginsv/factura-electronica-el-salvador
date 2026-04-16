import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ShopifyCustomer(models.Model):
    _name = 'shopify.customer'
    _description = 'Mapeo de Cliente Shopify'
    _rec_name = 'shopify_name'

    instance_id = fields.Many2one('shopify.instance', string='Instancia',
                                  required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Contacto Odoo')
    shopify_id = fields.Char(string='Shopify Customer ID', index=True)
    shopify_name = fields.Char(string='Nombre')
    shopify_email = fields.Char(string='Email')
    shopify_phone = fields.Char(string='Telefono')
    synced = fields.Boolean(string='Sincronizado', default=False)
    last_sync = fields.Datetime(string='Ultima sincronizacion')

    _sql_constraints = [
        ('unique_customer_instance', 'unique(instance_id, shopify_id)',
         'El cliente de Shopify ya esta mapeado en esta instancia.'),
    ]

    @api.model
    def sync_customers_from_shopify(self, instance):
        params = {'limit': 250}
        result = instance._shopify_request('GET', 'customers.json', params=params)
        customers = result.get('customers', [])
        count = 0
        for cust_data in customers:
            self._process_shopify_customer(instance, cust_data)
            count += 1

        instance.last_customer_sync = fields.Datetime.now()
        instance._create_log('info', 'sync_customers',
                             f'{count} clientes sincronizados')

    def _process_shopify_customer(self, instance, cust_data):
        shopify_id = str(cust_data.get('id', ''))
        existing = self.search([
            ('instance_id', '=', instance.id),
            ('shopify_id', '=', shopify_id),
        ], limit=1)

        name = f"{cust_data.get('first_name', '')} {cust_data.get('last_name', '')}".strip()
        email = cust_data.get('email', '')
        phone = cust_data.get('phone', '')

        vals = {
            'instance_id': instance.id,
            'shopify_id': shopify_id,
            'shopify_name': name or email,
            'shopify_email': email,
            'shopify_phone': phone,
            'synced': True,
            'last_sync': fields.Datetime.now(),
        }

        if existing:
            existing.write(vals)
            # Actualizar partner
            if existing.partner_id:
                partner_vals = {}
                if name:
                    partner_vals['name'] = name
                if email:
                    partner_vals['email'] = email
                if phone:
                    partner_vals['phone'] = phone
                if partner_vals:
                    existing.partner_id.write(partner_vals)
        else:
            # Buscar partner por email o crear
            partner = None
            if email:
                partner = self.env['res.partner'].search(
                    [('email', '=ilike', email)], limit=1)
            if not partner:
                partner_vals = {
                    'name': name or email or 'Cliente Shopify',
                    'email': email,
                    'phone': phone,
                    'customer_rank': 1,
                }
                # Direccion
                addresses = cust_data.get('addresses', [])
                if addresses:
                    addr = addresses[0]
                    country = None
                    if addr.get('country_code'):
                        country = self.env['res.country'].search(
                            [('code', '=', addr['country_code'].upper())], limit=1)
                    state = None
                    if addr.get('province_code') and country:
                        state = self.env['res.country.state'].search([
                            ('code', '=', addr['province_code']),
                            ('country_id', '=', country.id),
                        ], limit=1)
                    partner_vals.update({
                        'street': addr.get('address1', ''),
                        'street2': addr.get('address2', ''),
                        'city': addr.get('city', ''),
                        'zip': addr.get('zip', ''),
                        'country_id': country.id if country else False,
                        'state_id': state.id if state else False,
                    })
                partner = self.env['res.partner'].create(partner_vals)

            vals['partner_id'] = partner.id
            self.create(vals)

    def _get_or_create_partner(self, instance, customer_data):
        if not customer_data:
            return self.env['res.partner']

        shopify_id = str(customer_data.get('id', ''))
        if shopify_id:
            mapping = self.search([
                ('instance_id', '=', instance.id),
                ('shopify_id', '=', shopify_id),
            ], limit=1)
            if mapping and mapping.partner_id:
                return mapping.partner_id

        # Procesar y retornar
        self._process_shopify_customer(instance, customer_data)
        mapping = self.search([
            ('instance_id', '=', instance.id),
            ('shopify_id', '=', shopify_id),
        ], limit=1)
        return mapping.partner_id if mapping else self.env['res.partner']
