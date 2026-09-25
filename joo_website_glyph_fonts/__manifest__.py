{
    "name": "JOO Website Glyph Fonts",
    "summary": "MJ/GJ font integration for Odoo Website",
    "description": """
Provides MJ/GJ web fonts (IPAmjMincho, DWPIMincho, DWPIexMincho)
to Odoo Website pages, with dynamic font switching via joo_glyph_fonts.
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Website",
    "version": "19.0.10.2.0",

    "depends": [
        "website",
        "joo_glyph_fonts",
    ],

    "external_dependencies": {},

    "data": [],

    "assets": {
        "web.assets_frontend": [
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
