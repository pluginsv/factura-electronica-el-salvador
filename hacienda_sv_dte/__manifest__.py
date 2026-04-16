{
    "name": "Modulo Base para los Web Services de Hacienda",
    "version": "17.0.1.0.0",
    "category": "Localization/ElSalvador",
    "sequence": 14,
    "author": "Ing. Brenda Chacon, Ing. Karen Burgos, Ing. Francisco Flores",
    "website": "https://contaspro.net",
    "images": ['static/description/banner.png',
               'static/description/icon.png',
               'static/description/thumbnail.png'],
    "price": 20,
    "currency": "USD",
    "license": "LGPL-3",
    "summary": "",
    "depends": [
        "base_sv_dte",
        "sv_dte",  # needed for CUIT and also demo data
        # "dpto_sv_dte",  # needed for CUIT and also demo data
        "contacts",
        #"web"
        # TODO this module should be merged with l10n_ar_afipws_fe as the dependencies are the same
        "account",
    ],
    # "external_dependencies": {"python": ["pyafipws", "OpenSSL", "pysimplesoap"]},
    "data": [
        "wizard/upload_certificate_view.xml",
        "wizard/res_partner_update_from_padron_wizard_view.xml",
        "views/afipws_menuitem.xml",
        "views/ir_cron.xml",
        "views/afipws_certificate_view.xml",
        "views/afipws_certificate_alias_view.xml",
        "views/afipws_connection_view.xml",
        "views/res_config_settings.xml",
        "views/res_partner.xml",
        "views/res_company.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/ir.actions.url_data.xml",
        "data/res.configuration.csv",
        "views/res_company_config.xml",
    ],
    # "demo": [
    #     "demo/certificate_demo.xml",
    #     "demo/parameter_demo.xml",
    # ],
    'installable': True,
    "auto_install": False,
    "application": False,
}
