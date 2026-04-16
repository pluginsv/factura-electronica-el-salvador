{
    "name": "RRHH - Planilla Única",
    "version": "18.0.1.0.0",

    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 20,
    "currency": "USD",
    "license": "OPL-1",
    "depends": [
        "base",
        "hr",
        "hr_payroll",
        "rrhh_base_sv_dte",
        "hr_asignaciones_sv_dte",
        "hr_retenciones_sv_dte",
    ],
    'assets': {
        'web.assets_pdf': [
            'rrhh_base_sv_dte/static/src/css/inter_font.css',
            'rrhh_base_sv_dte/static/src/css/bootstrap.min.css',
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
