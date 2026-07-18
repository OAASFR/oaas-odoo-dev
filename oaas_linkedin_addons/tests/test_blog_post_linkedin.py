# -*- coding: utf-8 -*-
from unittest.mock import patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestBlogPostLinkedInCommentary(TransactionCase):

    def setUp(self):
        super().setUp()
        blog = self.env['blog.blog'].create({'name': 'Test Blog'})
        self.post = self.env['blog.post'].create({
            'name': 'Titre article',
            'subtitle': 'Sous-titre',
            'blog_id': blog.id,
            'content': '<p>Contenu de test</p>',
        })

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.'
           'LinkedInAiSummarizer.generate_commentary')
    def test_commentary_appends_article_link_after_ai_text(self, mock_generate):
        mock_generate.return_value = "Texte généré par l'IA #test"

        commentary = self.post._linkedin_commentary()

        self.assertTrue(commentary.startswith("Texte généré par l'IA #test"))
        self.assertIn(self.post.website_url, commentary)
        mock_generate.assert_called_once()
        _args, kwargs = mock_generate.call_args
        self.assertEqual(kwargs['title'], 'Titre article')
        self.assertEqual(kwargs['subtitle'], 'Sous-titre')
        self.assertIn('Contenu de test', kwargs['plain_text'])
