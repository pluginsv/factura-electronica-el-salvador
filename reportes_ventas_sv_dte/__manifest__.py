# -*- coding: utf-8 -*-
{
    'name': "Reportes de Ventas SV",
    'summary': "Reportes de ventas, facturación y cobros para El Salvador",
    'description': """
Reportes de Ventas
==================
Provee 5 reportes basados en SQL views (account.move + account.payment):

* Ventas por Periodo
* Cobros / Pagos recibidos
* Cuentas por Cobrar (antigüedad de saldos)
* Resumen por Vendedor
* Productos más vendidos
    """,
    'author': "ContaPro",
    'website': "https://contaspro.net",
    'license': 'OPL-1',
    'category': 'Sales/Reporting',
    'version': '18.0.1.0.0',
    'depends': [
        'base',
        'account',
        'sale',
        'invoice_sv_dte',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/report_ventas_periodo_views.xml',
        'views/report_cobros_views.xml',
        'views/report_cuentas_por_cobrar_views.xml',
        'views/report_resumen_vendedor_views.xml',
        'views/report_productos_vendidos_views.xml',
        'views/menu_reportes_ventas.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'country_code': 'SV',
}
