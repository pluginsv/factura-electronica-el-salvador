# -*- coding: utf-8 -*-
{
    'name': "Invalidacion de DTE El Salvador",

    'summary': """
        Proceso de invalidacion
        m""",

    'description': """
        Proceso de invalidacion
    """,

    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 15,
    "currency": "USD",
    "license": "OPL-1",

    'category': 'Accounting',
    "version": "18.0.1.0.0",

    # any module necessary for this one to work correctly
    'depends': ['base',
        "hacienda_sv_dte",   # webservice de Hacienda
        "base_sv_dte",
        # "invoice_sv_dte",
        # "account_debit_note",
        "haciendaws_fe_sv_dte",
        #'common_utils_sv_dte',
    ],

    # always loaded
    'data': [
        "views/account_move_views.xml",
        "security/ir.model.access.csv",
        "data/invoice_sending_invalidacion.xml",
        "data/res.configuration.csv",
    ],
    # only loaded in demonstration mode
    "demo": [],
    'installable': True,
    "auto_install": False,
    "application": False,
}
