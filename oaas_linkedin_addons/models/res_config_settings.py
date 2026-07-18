# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

from .ai_summarizer import DEFAULT_AI_MODEL


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

    # Mode de test : appel API réel mais lifecycleState=DRAFT (post créé sur
    # la page mais non diffusé dans le feed).
    oaas_linkedin_draft = fields.Boolean(
        string=_('Publier en brouillon (non diffusé)'),
        config_parameter='oaas_linkedin.draft')

    # Version de l'API LinkedIn (header LinkedIn-Version, format AAAAMM).
    # LinkedIn ne garde chaque version active qu'~12 mois : si les
    # publications échouent avec NONEXISTENT_VERSION, relever la version
    # courante sur https://learn.microsoft.com/en-us/linkedin/marketing/versioning
    # et la saisir ici (vide = valeur de repli codée dans le module).
    oaas_linkedin_api_version = fields.Char(
        string=_('Version API'),
        config_parameter='oaas_linkedin.api_version')

    # Génération IA du texte de post (résumé + accroche), endpoint compatible
    # API OpenAI (ex. Ollama exposant /v1/chat/completions). Champs vides =
    # repli sur DEFAULT_AI_BASE_URL / DEFAULT_AI_MODEL (models/ai_summarizer.py).
    oaas_linkedin_ai_base_url = fields.Char(
        string=_('URL de base IA'),
        config_parameter='oaas_linkedin.ai_base_url')
    oaas_linkedin_ai_model = fields.Char(
        string=_('Modèle IA'),
        config_parameter='oaas_linkedin.ai_model')
    oaas_linkedin_ai_api_key = fields.Char(
        string=_('Bearer token IA'),
        config_parameter='oaas_linkedin.ai_api_key')
    # Valeur 0/0.0 (champ jamais touché) => res.config.settings n'écrit rien
    # dans ir.config_parameter (le paramètre est absent, pas stocké à "0") :
    # le repli sur DEFAULT_AI_* dans ai_summarizer.py fonctionne normalement.
    oaas_linkedin_ai_temperature = fields.Float(
        string=_('Température IA'),
        config_parameter='oaas_linkedin.ai_temperature')
    oaas_linkedin_ai_max_tokens = fields.Integer(
        string=_('Tokens maximum IA'),
        config_parameter='oaas_linkedin.ai_max_tokens')
    oaas_linkedin_ai_timeout = fields.Integer(
        string=_("Délai d'attente IA (s)"),
        config_parameter='oaas_linkedin.ai_timeout')

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

    def _notify(self, title, message, warning=False, sticky=True):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'type': 'warning' if warning else 'success',
                'sticky': sticky,
            },
        }

    def action_oaas_linkedin_list_ai_models(self):
        """Sonde l'endpoint IA (avec les valeurs actuellement dans le
        formulaire, même non enregistrées) et affiche les modèles
        disponibles, pour aider à saisir le bon nom de modèle."""
        self.ensure_one()
        summarizer = self.env['oaas.linkedin.ai_summarizer']
        models_available = summarizer.list_models(
            base_url=self.oaas_linkedin_ai_base_url or None,
            api_key=self.oaas_linkedin_ai_api_key or None)
        message = _("%(count)s modèle(s) disponible(s) : %(models)s") % {
            'count': len(models_available),
            'models': ', '.join(models_available) or '—',
        }
        return self._notify(_('Modèles IA LinkedIn'), message)

    def action_oaas_linkedin_test_ai_connection(self):
        """Vérifie que l'endpoint IA répond et que le modèle configuré en
        fait partie (idem action_oaas_linkedin_list_ai_models + contrôle du
        modèle sélectionné)."""
        self.ensure_one()
        summarizer = self.env['oaas.linkedin.ai_summarizer']
        models_available = summarizer.list_models(
            base_url=self.oaas_linkedin_ai_base_url or None,
            api_key=self.oaas_linkedin_ai_api_key or None)
        configured_model = self.oaas_linkedin_ai_model or DEFAULT_AI_MODEL
        if configured_model in models_available:
            message = _("Connexion OK. Modèle « %(model)s » disponible "
                        "parmi %(count)s modèle(s).") % {
                'model': configured_model, 'count': len(models_available)}
            return self._notify(_('Test IA LinkedIn'), message)
        message = _("Connexion OK, mais le modèle « %(model)s » est "
                    "introuvable parmi : %(models)s") % {
            'model': configured_model,
            'models': ', '.join(models_available) or '—',
        }
        return self._notify(_('Test IA LinkedIn'), message, warning=True)
