{
    "name": "JOO Contacts Japan",
    "summary": "Japanese support for Odoo Contacts (Furigana, GlyphTag, IVS)",
    "description": """
Japanese enhancement bundle for Odoo Contacts:
- Furigana input & search
- GlyphTag input & IVS rendering
- MJ/GJ font integration
- Tofurengo normalization engine
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Contacts",
    "version": "19.0.10.2.0",

    "depends": [
        "contacts",
        "joo_partner_furigana",
        "joo_partner_glyphtag",
    ],

    "external_dependencies": {},

    "data": [],

    "assets": {},

    "demo": [
        "demo/demo.xml",
    ],

    "application": True,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
