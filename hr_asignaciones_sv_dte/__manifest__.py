{
    'name': 'Asignaciones Dinámicas de Salario',
    'version': '18.0.1.0.0',
    'author': 'Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores',
    'website': 'https://contaspro.net',
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 20,
    'currency': 'USD',
    'license': 'OPL-1',
    'summary': 'Permite gestionar horas extra, comisiones y otros ingresos por empleado',
    'category': 'Human Resources',
    'depends': ['web', 'base', 'hr', 'hr_payroll', 'hr_retenciones_sv_dte', 'hr_work_entry_contract', 'resource'],
    'data': [
        'data/hr_overtime_data.xml',
        'data/hr_salary_assignment_data.xml',
        'data/legacy_salary_rules.xml',
        'data/res.configuration.csv',

        'views/hr_salary_assignment_views.xml',
        'views/hr_salary_assignment_menu.xml',
        'views/res_company_contribution_view.xml',

        'security/hr_asignacion_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'post_init_hook': 'ejecutar_hooks_post_init',  # se ejecuta solo al instalar el módulo.
    # 'post_load': 'crear_asistencias_faltantes', #se ejecuta solo al actualizar el módulo.
}
