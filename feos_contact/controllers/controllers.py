# -*- coding: utf-8 -*-
from odoo import http

# class FeosContact(http.Controller):
#     @http.route('/feos_contact/feos_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/feos_contact/feos_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('feos_contact.listing', {
#             'root': '/feos_contact/feos_contact',
#             'objects': http.request.env['feos_contact.feos_contact'].search([]),
#         })

#     @http.route('/feos_contact/feos_contact/objects/<model("feos_contact.feos_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('feos_contact.object', {
#             'object': obj
#         })