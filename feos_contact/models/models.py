# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    
    contact_ids = fields.One2many('feos.contact', 'partner_id', string="Contacts")

class ContactType(models.Model):
    _name = 'feos.contact.type'
    
    name = fields.Char(required=True)

class Contact(models.Model):
    _name = 'feos.contact'
    
    value = fields.Char(required=True)    
    partner_id = fields.Many2one('res.partner', ondelete='cascade', string="Partner", required=True, default=lambda self: self.env.user.partner_id)
    type_contact_id = fields.Many2one('feos.contact.type', string="Type", required=True)
    
    
    
    
    
    
    
    
    
    