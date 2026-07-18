# -*- coding: utf-8 -*-
from unittest.mock import patch

from odoo.exceptions import UserError
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

    @patch('odoo.addons.oaas_linkedin_addons.models.blog_post.BlogPost.'
           '_publish_one_to_linkedin')
    def test_republish_ignores_idempotence_and_creates_new_post(
            self, mock_publish):
        def fake_publish(post):
            post.write({
                'linkedin_post_urn': 'urn:li:share:999',
                'linkedin_state': 'published',
                'linkedin_error': False,
            })
            return 'urn:li:share:999'
        mock_publish.side_effect = fake_publish
        self.post.write({
            'linkedin_post_urn': 'urn:li:share:111',
            'linkedin_state': 'published',
        })

        result = self.post.action_republish_to_linkedin()

        mock_publish.assert_called_once()
        self.assertEqual(self.post.linkedin_post_urn, 'urn:li:share:999')
        self.assertEqual(result['params']['type'], 'success')

    @patch('odoo.addons.oaas_linkedin_addons.models.blog_post.BlogPost.'
           '_publish_one_to_linkedin')
    def test_republish_sets_error_state_on_failure(self, mock_publish):
        mock_publish.side_effect = UserError("boom")
        self.post.write({
            'linkedin_post_urn': 'urn:li:share:111',
            'linkedin_state': 'published',
        })

        result = self.post.action_republish_to_linkedin()

        self.assertEqual(self.post.linkedin_state, 'error')
        self.assertEqual(self.post.linkedin_error, 'boom')
        self.assertEqual(result['params']['type'], 'danger')

    def test_republish_requires_single_record(self):
        blog = self.env['blog.blog'].create({'name': 'Test Blog 2'})
        other_post = self.env['blog.post'].create({
            'name': 'Autre article', 'blog_id': blog.id,
        })
        posts = self.post + other_post

        with self.assertRaises(ValueError):
            posts.action_republish_to_linkedin()
