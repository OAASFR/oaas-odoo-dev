# -*- coding: utf-8 -*-
{
    'name': "oaas_website_addons",

    'summary': """
        Small widgets for website""",

    'description': """
        Long description of module's purpose
    """,

    'author': "O.A.A.S.",
    'website': "https://oaas.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'website',
    'version': '0.2',
    'installable': True,
    'application': True,
    'auto_install': False,
    'active': True,
    'images': ['static/description/icon.png'],
    'document': ['static/documents/why.png', 'static/documents/how.png', 'static/documents/what.png'],
    # any module necessary for this one to work correctly
    'depends': ['web', 'web_editor', 'http_routing', 'portal', 'website_blog'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'external_dependencies': {
        'python': ['openpyxl']
    },
    # 'pre_init_hook': '_oaas_website_addons_pre_init',
    # 'post_init_hook': '_oaas_website_addons_post_init',
    # 'uninstall_hook': '_oaas_website_addons_uninstall_hook',
    # 'post_init_hook':
}
