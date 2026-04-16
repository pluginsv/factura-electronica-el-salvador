# -*- coding: utf-8 -*-
{
    'name': "Localizacion de El Salvador",
    'summary': """Plan contable, catalogos del MH, impuestos y campos DTE para El Salvador""",
    'description': """
    Localizacion contable y fiscal de El Salvador para Odoo.

    Plan contable y configuracion fiscal:
        - Plan de cuentas oficial requerido en El Salvador
        - Impuestos de compra y venta (IVA, retenciones, percepciones)
        - Posiciones fiscales configuradas

    25 catalogos oficiales del Ministerio de Hacienda:
        - CAT02 Tipos de documento
        - CAT03 Modelos de facturacion
        - CAT05 Tipos de contingencia
        - CAT09 Tipos de establecimiento
        - CAT11 Tipos de item
        - CAT14 Unidades de medida
        - CAT15 Tributos
        - CAT17 Formas de pago
        - CAT18 Plazos
        - CAT19 Actividades economicas
        - CAT27 Recintos fiscales
        - CAT28 Regimenes de exportacion
        - CAT31 INCOTERMS
        - Y mas (CAT21, CAT23, CAT24, CAT25, CAT26, CAT29, CAT30, CAT32)

    Campos DTE en facturas:
        - Forma de pago, condicion de pago, plazo
        - Tipo de transmision (normal/contingencia)
        - QR de Hacienda, JSON de respuesta, estado DTE
        - Calculo automatico de retenciones IVA para grandes contribuyentes

    Campos DTE en diarios contables:
        - Tipo de documento, tipo de establecimiento
        - Codigo de establecimiento y punto de venta
        - Modelo de facturacion y tipo de operacion

    Campos DTE en productos:
        - Unidad de medida Hacienda, tipo de item
        - Tributos por producto, tipo de venta (gravado/exento/no sujeto)

    Campos extendidos en contactos y empresa:
        - NRC, giro, nombre comercial, domicilio fiscal
        - UUID de empresa para DTE
        - Secuencias por diario
    """,
    'author': "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    'website': "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    'price': 0,
    'currency': 'USD',
    'license': 'OPL-1',
    'category': 'Localization',
    'version': '17.0.1.0.0',
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
