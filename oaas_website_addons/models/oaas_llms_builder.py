# -*- coding: utf-8 -*-
import re

from odoo import models, api


def _strip_html(html):
    """Retourne le texte brut d'un fragment HTML (sans balises)."""
    if not html:
        return ''
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', html,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Décode les entités HTML les plus courantes
    replacements = {
        '&nbsp;': ' ', '&amp;': '&', '&lt;': '<', '&gt;': '>',
        '&quot;': '"', '&#39;': "'", '&rsquo;': "'", '&eacute;': 'é',
    }
    for needle, value in replacements.items():
        text = text.replace(needle, value)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


class OaasLlmsBuilder(models.AbstractModel):
    """Génère le contenu des fichiers llms.txt / llms-full.txt.

    Suit la convention https://llmstxt.org/ : un fichier Markdown listant les
    ressources du site exploitables par un LLM. llms.txt = index (titres +
    URL + résumé), llms-full.txt = même index mais avec le contenu complet de
    chaque article.
    """
    _name = 'oaas.llms.builder'
    _description = 'Générateur llms.txt / llms-full.txt'

    @api.model
    def _published_posts(self, website):
        """Articles de blog publiés et visibles pour le site donné."""
        domain = [('is_published', '=', True), ('active', '=', True)]
        if website:
            domain += ['|', ('website_id', '=', website.id),
                       ('website_id', '=', False)]
        return self.env['blog.post'].sudo().search(
            domain, order='post_date desc')

    @api.model
    def build_llms_txt(self, website, full=False):
        """Construit le contenu textuel du fichier llms.txt ou llms-full.txt."""
        get_param = self.env['ir.config_parameter'].sudo().get_param
        # get_base_url() renvoie l'URL complète (scheme + domaine) du site si
        # configuré, sinon retombe sur web.base.url. Plus robuste que
        # website.domain qui peut être vide ou sans scheme.
        base_url = (website.get_base_url() if website
                    else get_param('web.base.url')) or ''
        base_url = base_url.rstrip('/')
        site_name = (website and website.name) or 'Site'

        lines = []
        # Titre H1 (requis par la spec llms.txt)
        lines.append('# %s' % site_name)
        lines.append('')

        header = get_param('oaas_website_addons.llms_header')
        if header:
            lines.append(header.strip())
            lines.append('')

        lines.append('## Articles de blog')
        lines.append('')

        for post in self._published_posts(website):
            url = '%s/blog/%s/%s' % (base_url, post.blog_id.id, post.id)

            summary = _strip_html(post.subtitle or post.content or '')
            if not full:
                if len(summary) > 200:
                    summary = summary[:197] + '...'
                lines.append('- [%s](%s): %s' % (post.name or '', url, summary))
            else:
                lines.append('### %s' % (post.name or ''))
                lines.append('')
                lines.append('URL: %s' % url)
                if post.post_date:
                    lines.append('Date: %s' % post.post_date)
                lines.append('')
                body = _strip_html(post.content or '')
                lines.append(body)
                lines.append('')

        return '\n'.join(lines).strip() + '\n'
