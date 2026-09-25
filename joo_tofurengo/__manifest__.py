{
    "name": "JOO Tofurengo (GlyphTag Engine)",
    "summary": "GlyphTag normalization engine",
    "description": """
Provides normalization, rendering, simplification, and inverse operations
for GlyphTag strings, with MJ/GJ dataset switching.
""",

    "author": "jp-one",
    "website": "https://github.com/jp-one",
    "category": "Tools",
    "version": "19.0.10.2.0",

    "depends": [
        "base",
        "base_setup",
    ],

    "external_dependencies": {
        "python": ["tofurengo"],
    },

    "data": [
        "views/res_config_settings_views.xml",
    ],

    "assets": {},

    "demo": [],

    "application": False,
    "auto_install": False,
    "installable": True,
    "license": "LGPL-3",
}
