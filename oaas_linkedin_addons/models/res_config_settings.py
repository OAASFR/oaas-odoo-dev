# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Identifiants de l'app LinkedIn (saisis à la main, comme les champs
    # llms.txt du module website). Tokens d'accès/refresh NON exposés ici :
    # ils sont obtenus par le flux OAuth et stockés en ir.config_parameter
    # (clés oaas_linkedin.access_token / refresh_token / token_expiry).
    oaas_linkedin_client_id = fields.Char(
        string=_('Client ID LinkedIn'),
        config_parameter='oaas_linkedin.client_id')
    oaas_linkedin_client_secret = fields.Char(
        string=_('Client Secret LinkedIn'),
        config_parameter='oaas_linkedin.client_secret')
    oaas_linkedin_org_urn = fields.Char(
        string=_('Organization URN'),
        config_parameter='oaas_linkedin.org_urn')

    # Champ calculé d'affichage de l'état de connexion (non stocké).
    oaas_linkedin_connected = fields.Boolean(
        string=_('LinkedIn connecté'),
        compute='_compute_oaas_linkedin_connected')

    def _compute_oaas_linkedin_connected(self):
        client = self.env['oaas.linkedin.client']
        for rec in self:
            rec.oaas_linkedin_connected = client.is_connected()

    def action_oaas_linkedin_connect(self):
        """Lance le flux OAuth : redirige le navigateur vers /linkedin/oauth/connect.

        On enregistre d'abord les paramètres en cours (Client ID/Secret) pour
        qu'ils soient disponibles côté contrôleur.
        """
        self.ensure_one()
        self.set_values()
        return {
            'type': 'ir.actions.act_url',
            'url': '/linkedin/oauth/connect',
            'target': 'self',
        }
