# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Fields purchase sv",
    "version": "18.0.1.0.0",
    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 30,
    "currency": "USD",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": [
        "purchase",
        "account",
        "sv_dte",
        "hacienda_contingencia_sv_dte",
        "invoice_sv_dte",
        "mh_anexos_sv_dte"
    ],
    "demo": [
    ],
    "data": [
        "data/res_configuration_defaults.xml",
        "security/ir.model.access.csv",

        'views/purchase.xml',
        'views/account_move.xml',
        'views/account_move_reversal.xml',
        # 'views/account_move_line_view.xml',
        "views/exp_duca_views.xml",
        "views/account_move_views.xml",
        "views/sale_purchase_created_by_views.xml",
        "views/res_company_account.xml",

        "views/sv_tax_override_views.xml",
        "views/account_move_fechas_purchase.xml",
        "views/account_move_purchase_rete_perc.xml",
    ],
    "installable": True,
    "auto_install": False,
}
