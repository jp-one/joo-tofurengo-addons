{
    "name": "JOO Partner (Contact) GlyphTag",
    "summary": "GlyphTag support for partner names and addresses",
    "description": """
Adds GlyphTag input fields and IVS rendering to partner names and addresses.
Includes integrated GlyphTag editor and synchronization with standard fields.
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Contacts",
    "version": "19.0.10.2.0",

    "depends": [
        "base",
        "mail",
        "joo_tofurengo",
        "joo_glyph_fonts",
    ],

    "external_dependencies": {},

    "data": [
        "views/res_partner_glyphtag_editor_views.xml",
        "views/res_partner_views.xml",
    ],

    "assets": {},

    "demo": [],

    "application": False,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
