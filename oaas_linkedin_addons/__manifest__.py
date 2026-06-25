# -*- coding: utf-8 -*-
{
    'name': "oaas_linkedin_addons",

    'summary': """
        Publier les articles de blog sur la page entreprise LinkedIn""",

    'description': """
        Ajoute une action (et un bouton) aux articles de blog pour les publier
        sur la page entreprise LinkedIn via l'API Community Management.
        Configuration (Client ID/Secret, Organization URN) dans
        Paramètres -> Site Web. Authentification OAuth 2.0.
    """,

    'author': "O.A.A.S.",
    'website': "https://oaas.fr/",

    'category': 'website',
    'version': '0.1',
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],

    'depends': ['website_blog'],

    'data': [
        'data/ir_actions_server.xml',
        'views/res_config_settings_views.xml',
        'views/blog_post_views.xml',
    ],
    'external_dependencies': {
        'python': ['requests'],
    },
}
