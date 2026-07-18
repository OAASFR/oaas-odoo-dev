# -*- coding: utf-8 -*-
from unittest.mock import Mock, patch

import requests

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


def _mock_response(content):
    resp = Mock()
    resp.raise_for_status = Mock()
    resp.json.return_value = {'choices': [{'message': {'content': content}}]}
    return resp


@tagged('post_install', '-at_install')
class TestLinkedInAiSummarizer(TransactionCase):

    def setUp(self):
        super().setUp()
        self.summarizer = self.env['oaas.linkedin.ai_summarizer']
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('oaas_linkedin.ai_base_url', 'https://ollama.example.test/v1')
        icp.set_param('oaas_linkedin.ai_model', 'qwen3:4b')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_calls_configured_endpoint(self, mock_post):
        mock_post.return_value = _mock_response('Accroche.\n\n- point 1\n\nCTA #tag')

        result = self.summarizer.generate_commentary(
            title='Titre', subtitle='Sous-titre', plain_text='Contenu',
            lang='fr_FR')

        self.assertIn('Accroche.', result)
        called_url = mock_post.call_args.args[0]
        self.assertEqual(called_url, 'https://ollama.example.test/v1/chat/completions')
        payload = mock_post.call_args.kwargs['json']
        self.assertEqual(payload['model'], 'qwen3:4b')
        self.assertIn('Titre', payload['messages'][1]['content'])

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_uses_default_endpoint_when_unset(self, mock_post):
        self.env['ir.config_parameter'].sudo().set_param('oaas_linkedin.ai_base_url', '')
        mock_post.return_value = _mock_response('Texte')

        self.summarizer.generate_commentary(
            title='T', subtitle='S', plain_text='C', lang='fr_FR')

        called_url = mock_post.call_args.args[0]
        self.assertEqual(
            called_url, 'https://ollama.validation.oaas.fr/v1/chat/completions')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_strips_think_blocks(self, mock_post):
        mock_post.return_value = _mock_response(
            '<think>raisonnement interne</think>Texte final du post')

        result = self.summarizer.generate_commentary(
            title='T', subtitle='S', plain_text='C', lang='fr_FR')

        self.assertEqual(result, 'Texte final du post')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_raises_user_error_on_http_failure(self, mock_post):
        mock_post.side_effect = requests.RequestException('boom')

        with self.assertRaises(UserError):
            self.summarizer.generate_commentary(
                title='T', subtitle='S', plain_text='C', lang='fr_FR')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_raises_user_error_on_empty_result(self, mock_post):
        mock_post.return_value = _mock_response('   ')

        with self.assertRaises(UserError):
            self.summarizer.generate_commentary(
                title='T', subtitle='S', plain_text='C', lang='fr_FR')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.post')
    def test_generate_commentary_sends_temperature_and_max_tokens(self, mock_post):
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('oaas_linkedin.ai_temperature', '0.4')
        icp.set_param('oaas_linkedin.ai_max_tokens', '500')
        mock_post.return_value = _mock_response('Texte')

        self.summarizer.generate_commentary(
            title='T', subtitle='S', plain_text='C', lang='fr_FR')

        payload = mock_post.call_args.kwargs['json']
        self.assertEqual(payload['temperature'], 0.4)
        self.assertEqual(payload['max_tokens'], 500)

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.get')
    def test_list_models_returns_sorted_ids(self, mock_get):
        resp = Mock()
        resp.raise_for_status = Mock()
        resp.json.return_value = {'data': [{'id': 'llama3.1'}, {'id': 'qwen3:4b'}]}
        mock_get.return_value = resp

        result = self.summarizer.list_models()

        self.assertEqual(result, ['llama3.1', 'qwen3:4b'])
        called_url = mock_get.call_args.args[0]
        self.assertEqual(called_url, 'https://ollama.example.test/v1/models')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.get')
    def test_list_models_uses_override_base_url_and_api_key(self, mock_get):
        resp = Mock()
        resp.raise_for_status = Mock()
        resp.json.return_value = {'data': []}
        mock_get.return_value = resp

        self.summarizer.list_models(
            base_url='https://override.test/v1', api_key='secret-token')

        called_url = mock_get.call_args.args[0]
        self.assertEqual(called_url, 'https://override.test/v1/models')
        headers = mock_get.call_args.kwargs['headers']
        self.assertEqual(headers['Authorization'], 'Bearer secret-token')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.requests.get')
    def test_list_models_raises_user_error_on_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException('boom')

        with self.assertRaises(UserError):
            self.summarizer.list_models()
