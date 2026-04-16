# -*- coding: utf-8 -*-
{
    'name': "sv_dte Factura Sujeto Excluido",
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
    "price": 35,
    "currency": "USD",
    "license": "LGPL-3",
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
