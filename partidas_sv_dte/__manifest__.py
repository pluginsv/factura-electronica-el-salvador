{
    'name': 'Reporte Partidas Contables SV',
    'version': '18.0.1.0.0',
    'summary': 'Reporte PDF de partidas contables agrupadas por cuenta padre',
    'description': """
    Genera reportes PDF de partidas contables agrupadas por cuenta padre,
    facilitando la revision y auditoria de los asientos contables.
    """,
    'author': 'Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores',
    'website': 'https://contaspro.net',
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/thumbnail.png',
    ],
    'price': 10,
    'currency': 'USD',
    'license': 'OPL-1',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'wizard/account_move_line_report_wizard.xml',
        'report/account_move_line_report_template.xml',
        'views/account_move_line_views.xml',
    ],
    'installable': True,
    'application': False,
}
