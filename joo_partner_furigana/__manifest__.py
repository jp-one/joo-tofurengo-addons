{
    'name': "joo_partner_furigana",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "jp-one",
    'website': "https://github.com/jp-one",

    'category': 'Tools',
    'version': '19.0.1.0.0',


    'depends': ['base', 'base_setup'],

    'external_dependencies': {
        'python': [
            'jaconv',
        ],
    },

    'data': [
        'views/res_config_settings_views.xml',
        'views/res_partner_furigana_views.xml',
        'views/res_partner_furigana_contacts_views.xml',
    ],
    
    'license': 'LGPL-3',
}
