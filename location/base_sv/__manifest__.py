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
    'price': 50.00,
    'currency': 'USD',
    'license': 'GPL-3',
    'category': 'Localization',
    'version': '17.1',
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
