import json
import os
import re
import pip
from odoo import api, SUPERUSER_ID
from csv import DictReader
from odoo.modules.module import get_module_path


@api.model
def oaas_website_addons_installation_code(env):
    print("Installation et configuration du module oaas_website_addons")


@api.model
def oaas_website_addons_update_code(env):
    print("Update et configuration du module oaas_website_addons")


@api.model
def oaas_website_addons_desinstallation_code(env):
    print("Désintallation et configuration du module oaas_website_addons")
