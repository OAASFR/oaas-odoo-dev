# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class OaasLlmsController(http.Controller):
    """Sert les fichiers llms.txt et llms-full.txt à la racine du site.

    Convention https://llmstxt.org/ : ces fichiers décrivent le site de façon
    exploitable par un LLM. Contenu auto-généré depuis les articles de blog
    publiés, ou contenu manuel selon le paramètre oaas_website_addons.llms_mode.
    """

    def _render_txt(self, full):
        get_param = request.env['ir.config_parameter'].sudo().get_param
        mode = get_param('oaas_website_addons.llms_mode') or 'auto'

        content = None
        if mode == 'manual':
            key = 'oaas_website_addons.llms_full_txt' if full \
                else 'oaas_website_addons.llms_txt'
            content = get_param(key)

        if not content:
            website = request.env['website'].get_current_website()
            content = request.env['oaas.llms.builder'].sudo().build_llms_txt(
                website, full=full)

        return request.make_response(content, headers=[
            ('Content-Type', 'text/plain; charset=utf-8'),
        ])

    @http.route('/llms.txt', type='http', auth='public', website=True,
                sitemap=False)
    def llms_txt(self, **kw):
        return self._render_txt(full=False)

    @http.route('/llms-full.txt', type='http', auth='public', website=True,
                sitemap=False)
    def llms_full_txt(self, **kw):
        return self._render_txt(full=True)
