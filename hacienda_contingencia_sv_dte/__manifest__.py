# -*- coding: utf-8 -*-
{
    'name': "Contingencia DTE El Salvador",

    'summary': """
        Proceso de gestión de contingencias y generación de DTE por lotes

        """,

    'description': """
        Proceso de gestión de contingencias y generación de DTE por lotes
    """,

    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 20,
    "currency": "USD",
    "license": "LGPL-3",
    'category': 'Accounting',
    "version": "18.0.1.0.0",


    # any module necessary for this one to work correctly
    'depends': ['base', 'sv_dte',
        'account',

        "hacienda_sv_dte",   # webservice de Hacienda
        "base_sv_dte",
        "haciendaws_fe_sv_dte",

    ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/account_contingencia.xml',
        'views/menuitem.xml',
        'views/account_move_views.xml',
        'views/cron_contingencia.xml',
        'data/res.configuration.csv',
        'views/account_incoterms_views.xml',
        'views/res_company_view_lote.xml',
        'data/account_journal_data.xml',
    ],
    # only loaded in demonstration mode
    "demo": [],
    'installable': True,
    "auto_install": False,
    "application": False,
}
