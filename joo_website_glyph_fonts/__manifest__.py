{
    "name": "joo_website_glyph_fonts",
    "summary": "Website integration for joo_glyph_fonts",
    "description": """
Provide MJ/GJ web fonts (IPAmjMincho, DWPIMincho, DWPIexMincho)
to Odoo Website pages, with dynamic font switching via joo_glyph_fonts.
""",

    'author': "jp-one",
    'website': "https://github.com/jp-one",

    'category': 'Website',
    'version': '19.0.1.0.0',


    "depends": [
        "website",
        "joo_glyph_fonts",
    ],

    "assets": {
        "web.assets_frontend": [
            "joo_glyph_fonts/static/src/css/fonts.css",
            "joo_glyph_fonts/static/src/js/font_loader.js",
        ],
    },

    "license": "LGPL-3",
    "installable": True,
}
