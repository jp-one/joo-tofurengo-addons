{
    'name': "joo_web_fonts",

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
    'depends': ['base', 'base_setup'],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
    ],
    
    # static files (css, fonts, js) are loaded through the assets system
    'assets': {
        'web.assets_backend': [
            # css
            'joo_web_fonts/static/src/css/fonts.css',
            # fonts
            'joo_web_fonts/static/src/fonts/ipamjm.ttf',
            'joo_web_fonts/static/src/fonts/DWPIMincho.ttf',
            'joo_web_fonts/static/src/fonts/DWPIexMincho.ttf',
            # js
            'joo_web_fonts/static/src/js/font_loader.js',
        ],
    },

}

