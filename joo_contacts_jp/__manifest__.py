{
    'name': "joo_contacts_jp",
    'summary': "Japanese support for Odoo Contacts (Furigana, GlyphTag, IVS)",
    'description': """
Japanese enhancement bundle for Odoo Contacts:
- Furigana input & search
- GlyphTag input & IVS rendering
- MJ/GJ font integration
- Tofurengo normalization engine

Search keywords:
Japanese, JP, Nihongo, Furigana, GlyphTag, IVS, Contacts
    """,

    'author': "jp-one",
    'website': "https://github.com/jp-one",
    'category': 'Contacts',
    'version': '19.0.1.0.0',


    'application': True,
    'installable': True,
    'auto_install': False,

    'depends': [
        'contacts',
        'joo_partner_furigana',
        'joo_partner_glyphtag',
        'joo_tofurengo',
        'joo_glyph_fonts',
    ],

    'data': [
        'demo/demo.xml',
    ],

    'license': 'LGPL-3',
}
