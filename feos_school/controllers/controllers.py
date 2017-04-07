# -*- coding: utf-8 -*-
from odoo import http

# class FeosSchool(http.Controller):
#     @http.route('/feos_school/feos_school/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/feos_school/feos_school/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('feos_school.listing', {
#             'root': '/feos_school/feos_school',
#             'objects': http.request.env['feos_school.feos_school'].search([]),
#         })

#     @http.route('/feos_school/feos_school/objects/<model("feos_school.feos_school"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('feos_school.object', {
#             'object': obj
#         })