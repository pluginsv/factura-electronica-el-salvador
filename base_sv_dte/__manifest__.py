# -*- coding: utf-8 -*-
{
    'name': "Localizacion Base de El Salvador",
    'summary': """Localizacion Base de El Salvador""",
    'description': """
    Localizacion de El Salvador :
        - Documento de Identificacion Unico
        """,
    'author': "Francisco Antonio Flores Villalta",
    'website': "https://contaspro.net/",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 15,
    'currency': 'USD',
    'license': 'LGPL-3',
    'category': 'Localization',
    'version': '19.0.1.0.0',
    'depends': ['base'],
    'data': [
        'data/res_lang.xml',
        'views/view_res_partner.xml',
        'views/view_res_company.xml',
        "views/res_company_form_mail_senders.xml",
    ],
    'demo': [
        'demo/res_company_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
