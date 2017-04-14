# -*- coding: utf-8 -*-

from odoo import models, fields, api

class skype_button(models.Model):
    _inherit = 'res.partner'
    
    skype = fields.Char(string='Skype name', size=128)

# class skype_button(models.Model):
#     _name = 'skype_button.skype_button'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100