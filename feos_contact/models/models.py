# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    contact_ids = fields.One2many('feos.contact', 'partner_id', string="Contacts")

class Contact(models.Model):
    _name = 'feos.contact'
    
    value = fields.Char(required=True)    
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="Partner", required=True, default=lambda self: self.env.uid)
    
    type = fields.Many2one('foes.contacttype', string="Type", required=True)
    
class Type(models.Model):
    _name = 'feos.contacttype'
    
    name = fields.Char(required=True)
    
    contact_ids = fields.One2many('feos.contact', 'type', string="Types")
    
    
    
    
    
    
    
    
    