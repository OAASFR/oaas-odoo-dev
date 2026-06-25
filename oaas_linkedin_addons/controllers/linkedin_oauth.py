# -*- coding: utf-8 -*-
"""Flux OAuth 2.0 LinkedIn.

Deux routes réservées à un utilisateur authentifié (auth='user') :
  - /linkedin/oauth/connect  : redirige vers l'écran d'autorisation LinkedIn.
  - /linkedin/oauth/callback : reçoit le code, vérifie le state anti-CSRF,
    échange le code contre un token et le stocke.

Le redirect_uri doit correspondre EXACTEMENT à celui déclaré dans l'app
LinkedIn (Paramètres de l'app → Auth → Authorized redirect URLs).
"""
import logging
import secrets

import werkzeug

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

CALLBACK_PATH = '/linkedin/oauth/callback'


class LinkedInOAuth(http.Controller):

    def _redirect_uri(self):
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        return '%s%s' % (base_url, CALLBACK_PATH)

    @http.route('/linkedin/oauth/connect', type='http', auth='user',
                website=False)
    def connect(self, **kw):
        client = request.env['oaas.linkedin.client']
        # State anti-CSRF stocké en session, vérifié au retour.
        state = secrets.token_urlsafe(24)
        request.session['linkedin_oauth_state'] = state
        try:
            url = client.get_authorization_url(self._redirect_uri(), state)
        except UserError as e:
            return self._result_page(str(e))
        return werkzeug.utils.redirect(url)

    @http.route(CALLBACK_PATH, type='http', auth='user', website=False)
    def callback(self, code=None, state=None, error=None,
                 error_description=None, **kw):
        if error:
            _logger.warning("LinkedIn OAuth error: %s - %s", error,
                            error_description)
            return self._result_page(
                _("Connexion LinkedIn refusée : %s") % (
                    error_description or error))

        expected = request.session.pop('linkedin_oauth_state', None)
        if not state or state != expected:
            return self._result_page(
                _("Échec de la vérification anti-CSRF (state invalide). "
                  "Recommencez la connexion."))
        if not code:
            return self._result_page(_("Aucun code d'autorisation reçu."))

        client = request.env['oaas.linkedin.client']
        try:
            client.exchange_code(code, self._redirect_uri())
        except UserError as e:
            return self._result_page(str(e))

        return self._result_page(
            _("Compte LinkedIn connecté avec succès. Vous pouvez fermer cet "
              "onglet."), success=True)

    def _result_page(self, message, success=False):
        """Page HTML minimale de retour, avec lien vers les paramètres."""
        color = '#0a66c2' if success else '#b00020'
        html = """
        <html><head><meta charset="utf-8"/>
        <title>LinkedIn — O.A.A.S.</title></head>
        <body style="font-family:sans-serif;max-width:560px;margin:80px auto;
                     text-align:center;">
          <h2 style="color:%s;">%s</h2>
          <p><a href="/web#action=base_setup.action_general_configuration">
             Retour aux paramètres</a></p>
        </body></html>
        """ % (color, werkzeug.utils.escape(message))
        return request.make_response(html, headers=[
            ('Content-Type', 'text/html; charset=utf-8')])
