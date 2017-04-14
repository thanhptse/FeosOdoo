# -*- coding: utf-8 -*-
from odoo import http

# class SkypeButton(http.Controller):
#     @http.route('/skype_button/skype_button/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/skype_button/skype_button/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('skype_button.listing', {
#             'root': '/skype_button/skype_button',
#             'objects': http.request.env['skype_button.skype_button'].search([]),
#         })

#     @http.route('/skype_button/skype_button/objects/<model("skype_button.skype_button"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('skype_button.object', {
#             'object': obj
#         })