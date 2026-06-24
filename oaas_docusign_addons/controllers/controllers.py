# -*- coding: utf-8 -*-
# from odoo import http


# class OaasDocusignAddons(http.Controller):
#     @http.route('/oaas_docusign_addons/oaas_docusign_addons', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oaas_docusign_addons/oaas_docusign_addons/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('oaas_docusign_addons.listing', {
#             'root': '/oaas_docusign_addons/oaas_docusign_addons',
#             'objects': http.request.env['oaas_docusign_addons.oaas_docusign_addons'].search([]),
#         })

#     @http.route('/oaas_docusign_addons/oaas_docusign_addons/objects/<model("oaas_docusign_addons.oaas_docusign_addons"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oaas_docusign_addons.object', {
#             'object': obj
#         })
