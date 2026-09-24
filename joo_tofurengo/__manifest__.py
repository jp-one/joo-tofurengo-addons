{
    'name': "joo_tofurengo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "jp-one",
    'website': "https://github.com/jp-one",

    'version': '19.0.1.0.0',



    # any module necessary for this one to work correctly
    'depends': ['base', 'base_setup'],

    'external_dependencies': {
        'python': [
            'tofurengo',
        ],
    },
    
    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
    ],

    'license': 'LGPL-3',
}

