{
    'name': "Partner GlyphTag Extension",

    'summary': "Enable custom character and variant glyph management for contacts",

    'description': """
Partner GlyphTag Extension
==========================
Adds custom character (GlyphTag) support to contact names and addresses.

Key Features:
-------------
* Integrated GlyphTag editor for main partner and child contact forms
* Automatic read-only control for standard fields when GlyphTag is enabled
* Seamless integration with custom glyph fonts and Tofurengo modules
    """,

    'author': "jp-one",
    'website': "https://github.com/jp-one",

    'category': 'Services/Contacts',
    'version': '19.0.1.0.0',

    'depends': [
        'base',
        'mail',
        'joo_tofurengo',
        'joo_glyph_fonts',
    ],

    'data': [
        'views/res_partner_glyphtag_editor_views.xml',
        'views/res_partner_views.xml',
    ],
    
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
