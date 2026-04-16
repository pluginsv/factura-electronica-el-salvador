# -*- coding: utf-8 -*-
{
    'name': "Factura de Exportacion DTE El Salvador",
    'summary': """
        Factura de Exportacion
        """,
    'description': """
        Factura de Exportacion
    """,
    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 20,
    "currency": "USD",
    "license": "OPL-1",
    'category': 'Accounting',
    "version": "17.0.1.0.0",
    'depends': ['base',
        "hacienda_sv_dte",   # webservice de Hacienda
        "base_sv_dte",
        # "invoice_sv_dte",
        # "account_debit_note",
        "haciendaws_fe_sv_dte",                ],
    # always loaded
    'data': [
        "data/res.configuration.csv",
    #     "views/account_move_views.xml",
        "views/account_move_view_inherit.xml",
        "views/view_company_account.xml",
    ],
    "demo": [],
    'installable': True,
    "auto_install": False,
    "application": False,
}
