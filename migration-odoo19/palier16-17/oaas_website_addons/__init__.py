# -*- coding: utf-8 -*-
import odoo
import pip
from odoo import api, SUPERUSER_ID
from . import controllers
from . import models
from . import scripts

#try:
#    import openpyxl
#except ImportError:
#    print('\n There was no such module named -openpyxl- installed')
#    print('xxxxxxxxxxxxxxxx installing openpyxl xxxxxxxxxxxxxx')
#    pip.main(['install', 'openpyxl'])


def _oaas_website_addons_pre_init(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    scripts.oaas_website_addons_init.oaas_website_addons_init_installation_code(env)


def _oaas_website_addons_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    scripts.oaas_website_addons_init.oaas_website_addons_init_update_code(env)


def _oaas_website_addons_uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    scripts.oaas_website_addons_init.oaas_website_addons_init_desinstallation_code(env)
