{
    'name': "joo_partner_glyphtag",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'joo_tofurengo', 'joo_glyph_fonts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_glyphtag_editor_views.xml',
        'views/res_partner_views.xml',
        # 'wizard/partner_glyphtag_editor_wizard_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'license': 'LGPL-3',
}

