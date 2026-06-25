# -*- coding: utf-8 -*-
"""Client API LinkedIn (Community Management / Posts API).

Centralise :
  - la lecture/écriture sécurisée des identifiants et tokens
    (ir.config_parameter, lus en sudo),
  - le rafraîchissement du token OAuth 2.0,
  - l'upload d'image en deux temps,
  - la création d'un post au nom de l'organisation.

Aucune route HTTP ici : le flux OAuth (échange du code) vit dans
controllers/linkedin_oauth.py. Ce modèle est un AbstractModel utilitaire,
appelé via self.env['oaas.linkedin.client'].
"""
import logging
from datetime import datetime, timedelta

import requests

from odoo import models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Version de l'API LinkedIn (header LinkedIn-Version, format AAAAMM).
# https://learn.microsoft.com/en-us/linkedin/marketing/versioning
LINKEDIN_API_VERSION = '202405'

AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
REST_BASE = 'https://api.linkedin.com/rest'

# Délai réseau (s) appliqué à tous les appels sortants.
HTTP_TIMEOUT = 20

# Marge de sécurité avant expiration du token pour déclencher un refresh.
TOKEN_REFRESH_MARGIN = timedelta(minutes=5)

# Scopes OAuth nécessaires pour publier au nom d'une organisation.
OAUTH_SCOPES = 'w_organization_social r_organization_social rw_organization_admin'


class LinkedInClient(models.AbstractModel):
    _name = 'oaas.linkedin.client'
    _description = 'Client API LinkedIn'

    # ------------------------------------------------------------------
    # Accès aux paramètres (sudo, jamais exposés à une route publique)
    # ------------------------------------------------------------------
    def _get_param(self, key):
        return self.env['ir.config_parameter'].sudo().get_param(
            'oaas_linkedin.%s' % key)

    def _set_param(self, key, value):
        self.env['ir.config_parameter'].sudo().set_param(
            'oaas_linkedin.%s' % key, value or '')

    def _get_credentials(self):
        client_id = self._get_param('client_id')
        client_secret = self._get_param('client_secret')
        if not client_id or not client_secret:
            raise UserError(_(
                "Identifiants LinkedIn manquants. Renseignez le Client ID et "
                "le Client Secret dans Paramètres → Site Web."))
        return client_id, client_secret

    # ------------------------------------------------------------------
    # Gestion du token OAuth
    # ------------------------------------------------------------------
    def store_tokens(self, token_data):
        """Persiste la réponse d'un échange/refresh de token.

        token_data : dict renvoyé par l'endpoint accessToken
        (access_token, expires_in, refresh_token, refresh_token_expires_in).
        """
        self._set_param('access_token', token_data.get('access_token'))
        expires_in = int(token_data.get('expires_in', 0))
        expiry = datetime.utcnow() + timedelta(seconds=expires_in)
        self._set_param('token_expiry', expiry.isoformat())
        # LinkedIn ne renvoie un refresh_token que si le produit le permet ;
        # on ne l'écrase pas s'il est absent de la réponse.
        if token_data.get('refresh_token'):
            self._set_param('refresh_token', token_data['refresh_token'])

    def _token_expired(self):
        expiry_str = self._get_param('token_expiry')
        if not expiry_str:
            return True
        try:
            expiry = datetime.fromisoformat(expiry_str)
        except ValueError:
            return True
        return datetime.utcnow() + TOKEN_REFRESH_MARGIN >= expiry

    def _refresh_token(self):
        refresh_token = self._get_param('refresh_token')
        if not refresh_token:
            raise UserError(_(
                "Le jeton d'accès LinkedIn a expiré et aucun jeton de "
                "rafraîchissement n'est disponible. Reconnectez le compte "
                "via « Connecter LinkedIn » dans les paramètres."))
        client_id, client_secret = self._get_credentials()
        try:
            resp = requests.post(TOKEN_URL, data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': client_id,
                'client_secret': client_secret,
            }, timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise UserError(_(
                "Échec du rafraîchissement du jeton LinkedIn : %s") % e)
        self.store_tokens(resp.json())

    def get_valid_token(self):
        """Retourne un access_token valide, en rafraîchissant si nécessaire."""
        if self._token_expired():
            self._refresh_token()
        token = self._get_param('access_token')
        if not token:
            raise UserError(_(
                "Aucun jeton d'accès LinkedIn. Connectez le compte via "
                "« Connecter LinkedIn » dans les paramètres."))
        return token

    def is_connected(self):
        return bool(self._get_param('access_token')) and not self._token_expired()

    # ------------------------------------------------------------------
    # Helpers OAuth (utilisés par le contrôleur)
    # ------------------------------------------------------------------
    def get_authorization_url(self, redirect_uri, state):
        client_id, _secret = self._get_credentials()
        params = {
            'response_type': 'code',
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': state,
            'scope': OAUTH_SCOPES,
        }
        req = requests.Request('GET', AUTH_URL, params=params).prepare()
        return req.url

    def exchange_code(self, code, redirect_uri):
        client_id, client_secret = self._get_credentials()
        try:
            resp = requests.post(TOKEN_URL, data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri,
                'client_id': client_id,
                'client_secret': client_secret,
            }, timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise UserError(_(
                "Échec de l'échange du code OAuth LinkedIn : %s") % e)
        self.store_tokens(resp.json())

    # ------------------------------------------------------------------
    # Appels API métier
    # ------------------------------------------------------------------
    def _headers(self, token):
        return {
            'Authorization': 'Bearer %s' % token,
            'LinkedIn-Version': LINKEDIN_API_VERSION,
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
        }

    def _get_org_urn(self):
        org_urn = self._get_param('org_urn')
        if not org_urn:
            raise UserError(_(
                "Organization URN LinkedIn manquant. Renseignez-le dans "
                "Paramètres → Site Web (format urn:li:organization:123456)."))
        return org_urn

    def upload_image(self, token, image_bytes):
        """Upload binaire en deux temps, retourne l'URN de l'image.

        1) initializeUpload -> URL d'upload + image URN
        2) PUT du binaire vers cette URL
        """
        org_urn = self._get_org_urn()
        try:
            init = requests.post(
                '%s/images?action=initializeUpload' % REST_BASE,
                headers=self._headers(token),
                json={'initializeUploadRequest': {'owner': org_urn}},
                timeout=HTTP_TIMEOUT)
            init.raise_for_status()
            value = init.json()['value']
            upload_url = value['uploadUrl']
            image_urn = value['image']

            put = requests.put(
                upload_url,
                data=image_bytes,
                headers={'Authorization': 'Bearer %s' % token},
                timeout=HTTP_TIMEOUT)
            put.raise_for_status()
        except (requests.RequestException, KeyError) as e:
            raise UserError(_("Échec de l'upload de l'image LinkedIn : %s") % e)
        return image_urn

    def create_post(self, commentary, link_url=None, image_urn=None,
                    link_title=None):
        """Crée un post sur la page entreprise. Retourne l'URN du post.

        - commentary : texte du post (titre + sous-titre).
        - link_url + link_title : carte article (génère un aperçu).
        - image_urn : image uploadée au préalable (prioritaire sur le lien
          pour le média mis en avant ; si les deux sont fournis, l'image
          porte le visuel et le lien reste dans le texte).
        """
        token = self.get_valid_token()
        org_urn = self._get_org_urn()

        payload = {
            'author': org_urn,
            'commentary': commentary,
            'visibility': 'PUBLIC',
            'distribution': {
                'feedDistribution': 'MAIN_FEED',
                'targetEntities': [],
                'thirdPartyDistributionChannels': [],
            },
            'lifecycleState': 'PUBLISHED',
            'isReshareDisabledByAuthor': False,
        }

        if image_urn:
            content = {'media': {'id': image_urn}}
            if link_title:
                content['media']['title'] = link_title
            payload['content'] = content
        elif link_url:
            payload['content'] = {
                'article': {
                    'source': link_url,
                    'title': link_title or link_url,
                }
            }

        try:
            resp = requests.post(
                '%s/posts' % REST_BASE,
                headers=self._headers(token),
                json=payload,
                timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
        except requests.RequestException as e:
            body = getattr(e.response, 'text', '') if getattr(
                e, 'response', None) is not None else ''
            _logger.warning("LinkedIn create_post failed: %s | %s", e, body)
            raise UserError(_("Échec de la publication LinkedIn : %s\n%s")
                            % (e, body))

        # L'URN du post est renvoyé dans l'en-tête x-restli-id.
        return resp.headers.get('x-restli-id') or resp.headers.get(
            'X-RestLi-Id', '')
