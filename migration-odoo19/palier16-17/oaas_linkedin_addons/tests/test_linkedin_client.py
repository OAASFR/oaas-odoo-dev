# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from ..models.linkedin_client import DEFAULT_LINKEDIN_API_VERSION


@tagged('post_install', '-at_install')
class TestLinkedInClientApiVersion(TransactionCase):
    """Couvre la régression 426 NONEXISTENT_VERSION : la version d'API
    LinkedIn doit être pilotable via ir.config_parameter, avec repli sur
    DEFAULT_LINKEDIN_API_VERSION quand le paramètre est vide."""

    def setUp(self):
        super().setUp()
        self.client = self.env['oaas.linkedin.client']
        self.icp = self.env['ir.config_parameter'].sudo()

    def test_api_version_falls_back_to_default_when_unset(self):
        self.icp.set_param('oaas_linkedin.api_version', '')
        self.assertEqual(self.client._api_version(), DEFAULT_LINKEDIN_API_VERSION)

    def test_api_version_uses_configured_value(self):
        self.icp.set_param('oaas_linkedin.api_version', '202601')
        self.assertEqual(self.client._api_version(), '202601')

    def test_headers_carry_configured_api_version(self):
        self.icp.set_param('oaas_linkedin.api_version', '202601')
        headers = self.client._headers('fake-token')
        self.assertEqual(headers['LinkedIn-Version'], '202601')

    def test_headers_carry_default_api_version_when_unset(self):
        self.icp.set_param('oaas_linkedin.api_version', '')
        headers = self.client._headers('fake-token')
        self.assertEqual(headers['LinkedIn-Version'], DEFAULT_LINKEDIN_API_VERSION)
