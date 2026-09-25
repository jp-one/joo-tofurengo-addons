{
    "name": "JOO Partner (Contact) Furigana",
    "summary": "Furigana input and search for partner names",
    "description": """
Adds a furigana field to res.partner and enables searching by reading.
Provides normalization options for hiragana, katakana, and spacing.
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Contacts",
    "version": "19.0.10.2.0",

    "depends": [
        "base",
        "base_setup",
    ],

    "external_dependencies": {
        "python": ["jaconv"],
    },

    "data": [
        "views/res_config_settings_views.xml",
        "views/res_partner_furigana_views.xml",
        "views/res_partner_furigana_contacts_views.xml",
    ],

    "assets": {},

    "demo": [],

    "application": False,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
