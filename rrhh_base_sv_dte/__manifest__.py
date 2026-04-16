{
    'name': 'Base Recursos Humanos',
    'version': '18.0.1.0.0',

    'author': 'Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores',
    'website': 'https://contaspro.net',
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 15,
    'currency': 'USD',
    'license': 'LGPL-3',
    'depends': ['hr_contract', 'hr_retenciones_sv_dte', 'hr_payroll'],
    'assets': {
        'web.assets_pdf': [
            'rrhh_base_sv_dte/static/src/css/inter_font.css',
            'rrhh_base_sv_dte/static/src/css/bootstrap.min.css',
        ],
    },
    'category': 'Human Resources',
    'data': [
        'security/ir.model.access.csv',
        'views/hr_retencion_isss_views.xml',
        'views/hr_retencion_afp_views.xml',
        'views/hr_retencion_renta_views.xml',
        'views/hr_retencion_renta_tramos_views.xml',
        'views/hr_payroll_reports.xml',
        'views/menu_rrhh_base.xml',
        "report/report.xml",
        "report/override_payment_report.xml",
        "report/report_payslip_incoe.xml",
        "views/hr_payslip_views.xml",
        'data/mail_template_payslip.xml',
        "views/hr_payslips_send_lotes.xml"
    ],
    'installable': True,
}
