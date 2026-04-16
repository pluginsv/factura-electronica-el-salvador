# -*- coding: utf-8 -*-
{
    'name': "l10n_sv_hacienda_invalidadion",

    'summary': """
        Proceso de invalidadion
        m""",

    'description': """
        Proceso de invalidadion
    """,

    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 30,
    "currency": "USD",
    "license": "GPL-3",

    'category': 'Accounting',
    "version": "17.0.1",

    # any module necessary for this one to work correctly
    'depends': ['base',
        "l10n_sv_hacienda",   # webservice de Hacienda
        "base_sv",
        # "l10n_invoice_sv",
        # "account_debit_note",
        "l10n_sv_haciendaws_fe",
        #'common_utils',
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
