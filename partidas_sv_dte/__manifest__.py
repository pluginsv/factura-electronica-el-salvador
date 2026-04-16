{
    'name': 'Reporte Partidas Contables SV',
    'version': '18.0.1.0.0',
    'summary': 'Reporte PDF de partidas contables agrupadas por cuenta padre',
    'author': 'Custom',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'wizard/account_move_line_report_wizard.xml',
        'report/account_move_line_report_template.xml',
        'views/account_move_line_views.xml',

    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}
