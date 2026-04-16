# -*- coding: utf-8 -*-
{
    'name': "Departamentos y Municipios de El Salvador",
    'summary': """Permite generar el reporte de Departamentos y Municipios de El Salvador""",
    'description': """
        Permite generar el reporte de  Departamentos y Municipios de El Salvador
        """,
    'author': "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    'website': "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 10,
    'currency': 'USD',
    'license': 'OPL-1',
    'category': 'General',
    'version': '18.0.1.0.0',
    'depends': [],
    # 'depends': ['base',
    #             'base_sv_dte'],
    'data': [
        'data/res.country.state.csv',
        'data/res.municipality.csv',
        'views/res_municipality.xml',
        'views/res_partner.xml',
        'views/res_bank.xml',
        'views/res_company.xml',
        'security/ir.model.access.csv',
    ],
}
