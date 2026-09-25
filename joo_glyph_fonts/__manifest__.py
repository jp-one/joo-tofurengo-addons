{
    "name": "JOO Glyph Fonts",
    "summary": "MJ/GJ font integration for IVS rendering",
    "description": """
Provides MJ/GJ web fonts (IPAmjMincho, DWPIMincho, DWPIexMincho)
for IVS rendering in the Odoo Web client.
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Tools",
    "version": "19.0.10.2.0",

    "depends": ["web"],

    "external_dependencies": {},

    "data": [
        "views/res_config_settings_views.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "joo_glyph_fonts/static/src/css/fonts.css",
            "joo_glyph_fonts/static/src/js/font_loader.js",
        ],
    },

    "demo": [],

    "application": False,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
