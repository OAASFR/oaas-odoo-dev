# -*- coding: utf-8 -*-
# from odoo import http


# class Oaas-website-addons(http.Controller):
#     @http.route('/oaas_website_addons/oaas_website_addons', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oaas_website_addons/oaas_website_addons/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('oaas_website_addons.listing', {
#             'root': '/oaas_website_addons/oaas_website_addons',
#             'objects': http.request.env['oaas_website_addons.oaas_website_addons'].search([]),
#         })

#     @http.route('/oaas_website_addons/oaas_website_addons/objects/<model("oaas_website_addons.oaas_website_addons"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oaas_website_addons.object', {
#             'object': obj
#         })
