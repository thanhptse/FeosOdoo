# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate
from datetime import timedelta as td

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    
    name = fields.Char('Title', required=True)
    short_name = fields.Char(
                        string='Short Title',
                        size=100,
                        translate=False)
#     notes = fields.Text('Internal Notes')
#     state = fields.Selection([('draft', 'Not available'), ('available', 'Available'), ('lost', 'Lost')], 'State')
#     description = fields.Html(string='Description')
#     cover = fields.Binary('Book Cover')
#     out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
#     date_updated = fields.Datetime('Last Updated')
#     pages = fields.Integer(
#                     string='Number of Pages',
#                     default=0,
#                     help='Total book page count',
#                     groups='base.group_user',
#                     states={'cancel':[('readonly', True)]},
#                     copy=True,
#                     index=False,
#                     readonly=False,
#                     company_dependent=False,)
#     reader_rating = fields.Float('Reader Average Rating', (14, 4),)
    author_ids = fields.Many2many('res.partner', string='Authors')
#     cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
#     currency_id = fields.Many2one('res.currency', string='Currency')
#     retail_price = fields.Monetary('Retail Price', currency_field='currency_id')
#     publisher_city = fields.Char('Publisher City',related='publisher_id.city')
#     age_days = fields.Float(
#         string='Days Since Release',
#         compute='_compute_age',
#         inverse='_inverse_age',
#         search='_search_age',
#         store=False,
#         compute_sudo=False,
#         )
#     
#     _sql_constraints = [
#         ('name_uniq',
#         'UNIQUE (name)',
#         'Book title must be unique.')
#         ]
#     @api.constrains('date_release')
#     def _check_release_date(self):
#         for r in self:
#             if r.date_release > fields.Date.today():
#                 raise models.ValidationError('Release date must be in the past')
#     
#     @api.depends('date_release')
#     def _compute_age(self):
#         today = fDate.from_string(fDate.today())
#         for book in self.filtered('date_release'):
#             delta = (fDate.from_string(book.date_release - today)
#             book.age_days = delta.days
#     
#     def _inverse_age(self):
#         today =fDate.from_string(fDate.today())
#         for book in self.filtered('date_release'):
#             d = td(days=book.age_days) - today
#             book.date_release = fDate.to_string(d)
#             
#     def _search_age(self, operator, value):
#         today = fDate.from_string(fDate.today())
#         value_days = td(days=value)
#         value_date = fDate.to_string(today - value_days)
#         return [('date_release', operator, value_date)]
#     
#     @api.model
#     def _referencable_models(self):
#         models = self.env['res.request.link'].search([])
#         return [(x.object, x.name) for x in models]f
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    book_ids = fields.Many2many('library.book', string='Published Books')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
