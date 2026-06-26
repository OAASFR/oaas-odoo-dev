# -*- coding: utf-8 -*-
import base64
import json
import logging
import re

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class BlogPost(models.Model):
    _inherit = 'blog.post'

    linkedin_post_urn = fields.Char(
        string='URN du post LinkedIn', readonly=True, copy=False,
        help="Identifiant du post créé sur LinkedIn. Sa présence empêche "
             "toute republication (idempotence).")
    linkedin_state = fields.Selection(
        selection=[
            ('not_published', 'Non publié'),
            ('published', 'Publié'),
            ('error', 'Erreur'),
        ],
        string='Statut LinkedIn', default='not_published', readonly=True,
        copy=False)
    linkedin_error = fields.Text(
        string='Dernière erreur LinkedIn', readonly=True, copy=False)

    def _linkedin_commentary(self):
        """Construit le texte du post : titre + sous-titre + lien."""
        self.ensure_one()
        parts = [self.name or '']
        if self.subtitle:
            parts.append(self.subtitle)
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        url = '%s%s' % (base_url, self.website_url) if self.website_url else ''
        if url:
            parts.append(url)
        return '\n\n'.join(p for p in parts if p)

    def _linkedin_cover_bytes(self):
        """Retourne le binaire de l'image de couverture, ou None.

        Sur blog.post (Odoo 16), la couverture est stockée dans
        cover_properties : un JSON CSS contenant
        background-image: url(/web/image/<attachment_id>...). On en extrait
        l'id de l'ir.attachment puis on lit son binaire (datas).
        """
        self.ensure_one()
        if not self.cover_properties:
            return None
        try:
            props = json.loads(self.cover_properties)
        except (TypeError, ValueError):
            return None
        bg = props.get('background-image') or ''
        # ex: url(/web/image/123-abc/cover.png) ou url("/web/image/123")
        m = re.search(r'/web/image/(\d+)', bg)
        if not m:
            return None
        attachment = self.env['ir.attachment'].sudo().browse(int(m.group(1)))
        if not attachment.exists() or not attachment.datas:
            return None
        try:
            return base64.b64decode(attachment.datas)
        except (TypeError, ValueError):
            return None

    def _publish_one_to_linkedin(self):
        """Publie un article. Lève UserError en cas d'échec."""
        self.ensure_one()
        client = self.env['oaas.linkedin.client']

        commentary = self._linkedin_commentary()
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        link_url = '%s%s' % (base_url, self.website_url) \
            if self.website_url else None

        image_urn = None
        cover = self._linkedin_cover_bytes()
        if cover:
            token = client.get_valid_token()
            image_urn = client.upload_image(token, cover)

        urn = client.create_post(
            commentary=commentary,
            link_url=link_url,
            image_urn=image_urn,
            link_title=self.name)

        self.write({
            'linkedin_post_urn': urn,
            'linkedin_state': 'published',
            'linkedin_error': False,
        })
        return urn

    def action_publish_to_linkedin(self):
        """Action appelée par le bouton du formulaire et l'action serveur.

        Idempotent : un article déjà porteur d'un URN n'est pas republié.
        Agrège les résultats et renvoie une notification.
        """
        published, skipped, errors = 0, 0, 0
        for post in self:
            if post.linkedin_post_urn:
                skipped += 1
                continue
            try:
                post._publish_one_to_linkedin()
                published += 1
            except UserError as e:
                errors += 1
                post.write({
                    'linkedin_state': 'error',
                    'linkedin_error': str(e),
                })
                _logger.warning("LinkedIn publish failed for blog.post %s: %s",
                                post.id, e)

        client = self.env['oaas.linkedin.client']
        mode = _(" [BROUILLON — posts non diffusés sur le feed]") \
            if client._draft_enabled() else ''

        msg = _("%(pub)s publié(s), %(skip)s ignoré(s) (déjà publié), "
                "%(err)s en erreur.%(mode)s") % {
            'pub': published, 'skip': skipped, 'err': errors, 'mode': mode}
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Publication LinkedIn'),
                'message': msg,
                'type': 'danger' if errors else 'success',
                'sticky': bool(errors),
            },
        }
