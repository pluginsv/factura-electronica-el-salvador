{
    'name': 'Despachos',
    'summary': 'Gestión de despachos',
    'description': """
    Módulo para la gestión de despachos.
    """,
    'author': 'Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores',
    'website': 'https://contaspro.net',
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 20,
    'currency': 'USD',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'version': '17.0.1.0.0',
    'depends': [
        'web',
        'dpto_sv_dte',
        'hacienda_sv_dte',
        'stock',
        'stock_barcode',
        'sale',
        'fleet',
        'hr',
        'account',
        'mail',
    ],
    'assets': {
        'web.assets_backend': [
            'despacho_sv_dte/static/src/js/map_field.js',
            'despacho_sv_dte/static/src/xml/map_template.xml',
            'https://maps.googleapis.com/maps/api/js?key=AIzaSyCrGkTd0pXFZ1lZbj4DJrmsnmmXvT_DKjg',
            # 'despacho_sv_dte/static/src/js/barcode_header_button.js',
            'despacho_sv_dte/static/src/js/barcode_header_button.js',
            'despacho_sv_dte/static/src/xml/barcode_header_button.xml',
        ],
    },
    'data': [
        'data/res.configuration.csv',
        'data/res.municipality.csv',
        'data/dispatch_sequences.xml',
        'data/dispatch_route_sequence.xml',

        'security/ir.model.access.csv',

        # 1) PRIMERO vistas que serán referenciadas por actions/menus
        'views/dispatch_delivery_analysis_views.xml',

        'views/dispatch_route_view.xml',
        'views/sale_order_partner_picker_inherit.xml',
        'views/dispatch_route_sale_order_picker_view.xml',
        'views/sale_order_dispatch_route_view.xml',
        'views/sale_order_route_picker_views.xml',
        'views/dispatch_route_list_view.xml',

        'views/dispatch_action.xml',
        'views/dispatch_route_reception_view.xml',

        'views/dispatch_zones_view.xml',
        'views/dispatch_route_invoice_return_views.xml',
        'views/vehicule_dispatch_route_view.xml',

        # 2) DESPUÉS actions y menus
        'views/dispatch_menu.xml',

        # 3) Reportes
        'report/dispatch_report.xml',
        'report/report_recepcion_ruta_template.xml',
        'report/report_carga_ruta_template.xml',
        'report/dispatch_delivery_analysis_template.xml',
        'report/report_montacarguistas_template.xml',

        'data/res.previous.municipality.csv',
        'views/partner_company_view.xml',

        # (si necesitas que el reporte exista antes del action que lo llama, también va arriba)
    ],

    'application': True,
    'installable': True,
}
