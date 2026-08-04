# -*- coding: utf-8 -*-
from unittest.mock import patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestResConfigSettingsAiActions(TransactionCase):

    def setUp(self):
        super().setUp()
        self.settings = self.env['res.config.settings'].create({
            'oaas_linkedin_ai_base_url': 'https://ollama.example.test/v1',
            'oaas_linkedin_ai_model': 'qwen3:4b',
        })

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.'
           'LinkedInAiSummarizer.list_models')
    def test_list_ai_models_uses_form_values_and_shows_count(self, mock_list):
        mock_list.return_value = ['llama3.1', 'qwen3:4b']

        result = self.settings.action_oaas_linkedin_list_ai_models()

        mock_list.assert_called_once_with(
            base_url='https://ollama.example.test/v1', api_key=None)
        self.assertIn('2', result['params']['message'])
        self.assertEqual(result['params']['type'], 'success')

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.'
           'LinkedInAiSummarizer.list_models')
    def test_test_ai_connection_success_when_model_available(self, mock_list):
        mock_list.return_value = ['llama3.1', 'qwen3:4b']

        result = self.settings.action_oaas_linkedin_test_ai_connection()

        self.assertEqual(result['params']['type'], 'success')
        self.assertIn('qwen3:4b', result['params']['message'])

    @patch('odoo.addons.oaas_linkedin_addons.models.ai_summarizer.'
           'LinkedInAiSummarizer.list_models')
    def test_test_ai_connection_warns_when_model_missing(self, mock_list):
        mock_list.return_value = ['llama3.1']

        result = self.settings.action_oaas_linkedin_test_ai_connection()

        self.assertEqual(result['params']['type'], 'warning')
        self.assertIn('introuvable', result['params']['message'])
