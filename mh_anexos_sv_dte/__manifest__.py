# -*- coding: utf-8 -*-
{
    'name': "Anexos MH",
    'summary': """Anexos MH""",
    'author': "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    'website': "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 15,
    'currency': 'USD',
    'license': 'LGPL-3',
    'category': 'Localization',
    'version': '17.0.1.0.0',
    'depends': ['base',
                # "hacienda_sv_dte",  # webservice de Hacienda
                # "base_sv_dte",
                "invoice_sv_dte",
                'account',
                'phone_validation',
                'l10n_latam_base',
                'haciendaws_fe_sv_dte',
                'hacienda_invalidadion_sv_dte'
                ],
    'data': [
        "security/ir.model.access.csv",

        # VISTAS
        "views/view_anexo_search_filters.xml",
        "views/view_report_account_move_consumidor_final_daily_list.xml",
        "views/view_account_new_fields.xml",
        "views/view_anexo_casilla162.xml",
        "views/view_anexo_cliente_mayores.xml",
        "views/view_anexo_clientes.xml",
        "views/view_anexo_compras.xml",
        "views/view_anexo_contribuyentes.xml",
        "views/view_anexo_documentos_anulados_y_extraviados.xml",
        "views/view_anexo_sujeto_excluido.xml",
        "views/hide_new_button_in_anexos.xml",

        # ACCIONES / MENÚS
        "views/report_anexos_action.xml",

        # DATA CSV
        "data/account.tipo.costo.gasto.csv",
        "data/account.tipo.ingreso.csv",
        "data/account.tipo.operacion.csv",
        "data/account.clasificacion.facturacion.csv",
        "data/account.clase.documento.csv",
        "data/account.tipo.documento.identificacion.csv",
        "data/account.sector.csv",
    ],

    'demo': [
        # 'demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'country_code': 'SV',
    # 'post_init_hook': 'drop_data',
}
