{
    "name": "RRHH - Planilla Única",
    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 40,
    "currency": "USD",
    "license": "GPL-3",
    "depends": [
        "base",
        "hr",
        "hr_payroll",
        "rrhh_base",
        "l10n_sv_hr_asignaciones",
        "l10n_sv_hr_retenciones",
    ],
    'assets': {
        'web.assets_pdf': [
            'rrhh_base/static/src/css/inter_font.css',
            'rrhh_base/static/src/css/bootstrap.min.css',
        ],
    },
    'category': 'Human Resources',
    'data': [
        'security/ir.model.access.csv',
        "views/hr_payslip_menu.xml",
        "views/hr_employees_planilla_unica_data.xml",
        "views/hr_payslip_planilla_unica_reporte.xml",
    ],
    'installable': True,
}
