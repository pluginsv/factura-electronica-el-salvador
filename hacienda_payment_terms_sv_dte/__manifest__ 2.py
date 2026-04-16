# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Añade configuracion para terminos de pagos hacienda sv",
    "version": "18.0.1.0.0",
    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 20,
    "currency": "USD",
    "license": "LGPL-3",
    "category": "Point of Sale",
    "depends": [
        "haciendaws_fe_sv_dte",
        "sv_dte",
        "base",
    ],
    "data": [
        'views/account_payment_term.xml',
        'views/account_move.xml'
    ],
    "installable": True,
    "auto_install": False,
}
