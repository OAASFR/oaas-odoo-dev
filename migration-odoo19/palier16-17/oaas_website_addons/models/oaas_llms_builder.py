# -*- coding: utf-8 -*-
import json
import re

from markupsafe import Markup

from odoo import models, api


def _safe_jsonld(data):
    """Sérialise data en JSON-LD sûr pour insertion dans <script>.

    json.dumps produit du JSON valide ; on neutralise ensuite < > & en
    échappements unicode (toujours valides en JSON, mais inertes en HTML, ce
    qui évite toute fermeture prématurée du <script> ou injection). Le résultat
    est marqué Markup pour que QWeb (t-out) ne le ré-échappe pas en &#34;.
    """
    raw = json.dumps(data, ensure_ascii=False)
    raw = raw.replace('<', '\\u003c').replace('>', '\\u003e') \
             .replace('&', '\\u0026')
    return Markup(raw)


def _cover_image_url(cover_properties, base_url):
    """Extrait l'URL absolue de l'image de couverture depuis cover_properties."""
    if not cover_properties:
        return None
    match = re.search(r'url\(([^)]+)\)', cover_properties)
    if not match:
        return None
    url = match.group(1).strip('\'" ')
    if url.startswith('/'):
        url = base_url.rstrip('/') + url
    return url


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

        # Section "Pages clés" : pages statiques publiées du site (accueil,
        # services, contact…). Aide les LLM à situer le site au-delà du blog.
        pages = self._key_pages(website)
        if pages:
            lines.append('## Pages clés')
            lines.append('')
            for name, page_url in pages:
                lines.append('- [%s](%s)' % (name, page_url))
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
                if post.author_id.name:
                    lines.append('Auteur: %s' % post.author_id.name)
                lines.append('')
                body = _strip_html(post.content or '')
                lines.append(body)
                lines.append('')

        return '\n'.join(lines).strip() + '\n'

    @api.model
    def _key_pages(self, website):
        """Retourne [(nom, url_absolue)] des pages statiques publiées du site.

        Limité aux pages indexables (menu visible), hors pages techniques.
        """
        base_url = (website.get_base_url() if website
                    else self.env['ir.config_parameter'].sudo().get_param(
                        'web.base.url')) or ''
        base_url = base_url.rstrip('/')
        domain = [('is_published', '=', True), ('url', '!=', False)]
        if website:
            domain += ['|', ('website_id', '=', website.id),
                       ('website_id', '=', False)]
        pages = self.env['website.page'].sudo().search(domain)
        result = []
        for page in pages:
            # On ignore les URL paramétrées ou de service
            if not page.url.startswith('/') or '/' in page.url[1:].rstrip('/'):
                continue
            name = page.name or page.url
            result.append((name, base_url + page.url))
        return result


class BlogPost(models.Model):
    _inherit = 'blog.post'

    def _oaas_blogposting_jsonld(self):
        """Renvoie le JSON-LD Schema.org BlogPosting de l'article (string).

        Exploité par les moteurs IA (Claude, ChatGPT, Gemini) et Google SGE
        pour comprendre auteur / date / sujet de la page. Injecté dans le
        <head> via le template website_blog.blog_post_complete.
        """
        self.ensure_one()
        # Le rendu a lieu en contexte public (visiteur non connecté). L'accès
        # à author_id (res.partner) et website_id est interdit au public, ce
        # qui ferait planter le QWeb -> 403. On lit donc ces relations en sudo.
        post = self.sudo()
        base_url = (post.get_base_url() or '').rstrip('/')
        url = '%s/blog/%s/%s' % (base_url, post.blog_id.id, post.id)

        description = _strip_html(
            post.subtitle or post.website_meta_description or '')
        if len(description) > 300:
            description = description[:297] + '...'

        data = {
            '@context': 'https://schema.org',
            '@type': 'BlogPosting',
            'headline': post.name or '',
            'description': description,
            'url': url,
            'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
            'inLanguage': (self.env.lang or 'fr_FR').split('_')[0],
            'publisher': {
                '@type': 'Organization',
                'name': post.blog_id.website_id.name or 'OAAS',
                'url': base_url,
            },
        }
        if post.author_id.name:
            data['author'] = {'@type': 'Person', 'name': post.author_id.name}
        if post.post_date:
            data['datePublished'] = post.post_date.isoformat()
        if post.write_date:
            data['dateModified'] = post.write_date.isoformat()
        if post.website_meta_keywords:
            data['keywords'] = post.website_meta_keywords
        image = _cover_image_url(post.cover_properties, base_url)
        if image:
            data['image'] = image

        return _safe_jsonld(data)
