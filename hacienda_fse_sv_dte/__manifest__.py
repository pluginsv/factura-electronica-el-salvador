# -*- coding: utf-8 -*-
{
    'name': "Factura Sujeto Excluido DTE El Salvador",
    'summary': """
        Factura Sujeto Excluido
        """,
    'description': """
        Factura Sujeto Excluido
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
    "version": "18.0.1.0.0",
    'depends': ['base',
        "hacienda_sv_dte",   # webservice de Hacienda
        "base_sv_dte",
        # "invoice_sv_dte",
        # "account_debit_note",
        "haciendaws_fe_sv_dte",                ],
    # always loaded
    'data': [
    #     "views/account_move_views.xml",
    ],
    "demo": [],
    'installable': True,
    "auto_install": False,
    "application": False,
}
