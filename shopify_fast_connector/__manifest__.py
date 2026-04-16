{
    'name': 'Shopify Fast Connector',
    'version': '18.0.1.0.0',
    'summary': 'Sincroniza pedidos, productos, clientes e inventario entre Shopify y Odoo',
    'description': """
    Shopify Fast Connector para Odoo

    Sincronizacion bidireccional entre Shopify y Odoo:
        - Importa pedidos de Shopify como ordenes de venta
        - Crea facturas y registra pagos automaticamente
        - Genera movimientos de inventario
        - Envia detalles de cumplimiento de vuelta a Shopify
        - Sincroniza productos y clientes
        - Configuracion en 4 sencillos pasos
        - Sincronizacion en tiempo real via webhooks
        - Resumen por correo electronico con KPIs personalizados
    """,
    'author': 'Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores',
    'website': 'https://contaspro.net',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/thumbnail.png',
    ],
    'price': 99,
    'currency': 'USD',
    'license': 'OPL-1',
    'category': 'Sales/Connector',
    'depends': [
        'sale_management',
        'account',
        'stock',
        'product',
        'contacts',
        'mail',
    ],
    'data': [
        'security/shopify_security.xml',
        'security/ir.model.access.csv',
        'data/shopify_cron.xml',
        'data/mail_template.xml',
        'wizard/shopify_setup_wizard_views.xml',
        'views/shopify_instance_views.xml',
        'views/shopify_product_views.xml',
        'views/shopify_order_views.xml',
        'views/shopify_customer_views.xml',
        'views/shopify_log_views.xml',
        'views/shopify_menu.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
