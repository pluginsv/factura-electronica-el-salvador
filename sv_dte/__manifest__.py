# -*- coding: utf-8 -*-
{
    'name': "Localizacion de El Salvador",
    'summary': """Localizacion contable, fiscal y tributaria de El Salvador para Odoo""",
    'description': """
    Localizacion de El Salvador para Odoo:

    Plan contable y configuracion fiscal:
        - Plan de cuentas oficial requerido en El Salvador
        - Categorias e impuestos (IVA, retenciones, percepciones)
        - Posiciones fiscales para compras y ventas

    Catalogos tributarios del Ministerio de Hacienda:
        - Actividades economicas, formas de pago, plazos
        - Tipos de documento, tipos de operacion, tributos
        - Unidades de medida, recintos fiscales, INCOTERMS
        - Tipos de establecimiento, regimenes, contingencias

    Tipos de identificacion fiscal:
        - NIT (Numero de Identificacion Tributaria)
        - NRC (Numero de Registro de Contribuyente)
        - DUI (Documento Unico de Identidad)

    Soporte para documentos fiscales:
        - Consumidor Final (FCF)
        - Credito Fiscal (CCF)
        - Exportaciones
        - Notas de Credito y Debito
        - Anulaciones
    """,
    'author': "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    'website': "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 25,
    'currency': 'USD',
    'license': 'LGPL-3',
    'category': 'Localization',
    'version': '18.0.1.0.0',
    'depends': ['base',
                'base_sv_dte',
                'account',
                'phone_validation',
                # 'dpto_sv_dte',
                # 'l10n_latam_invoice_document',
                'l10n_latam_base',
                ],
    'data': [
        "security/ir.model.access.csv",
        "views/account_catalogos.xml",
        "data/catalogos.xml",
        'data/account.journal.tipo_modelo.field.csv',
        "views/menuitem.xml",
        "views/product_template.xml",
        'views/view_res_company.xml',
        'views/view_res_partner.xml',
        'views/account_type.xml',
        'views/view_ir_sequence.xml',
        'views/account_journal_view.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'views/account_tax.xml',

        'data/res_country_data.xml',
        'data/l10n_sv_coa.xml',
        # 'data/account.account.template.csv',
        'data/account_tax_data.xml',
        'data/account_fiscal_position.xml',
        'data/account_fiscal_position_tax.xml',
        'data/l10n_sv_coa_post.xml',
        'data/journal_data.xml',
        'data/l10n_latam.identification.type.csv',

        'data/account.move.tipo_contingencia.field.csv',
        'data/account.move.actividad_economica.field.csv',
        'data/account.move.forma_pago.field.csv',
        'data/account.move.incoterms.field.csv',
        'data/account.move.plazo.field.csv',
        'data/account.move.recinto_fiscal.field.csv',
        'data/account.move.tipo_documento_contingencia.field.csv',
        'data/account.move.tipo_establecimiento.field.csv',
        'data/account.move.titulo_rem_bienes.field.csv',
        'data/account.move.unidad_medida.field.csv',
        'data/account.move.tributos.field.csv',
        'data/account.move.tipo_item.field.csv',
        'data/account.journal.tipo_documento.field.csv',
        'data/account.move.tipo_operacion.field.csv',
        'data/account.move.regimen.field.csv',
        'data/account_tax_sv.xml',
        # 'views/anexos_report_views.xml',

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
