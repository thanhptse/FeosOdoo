# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.addons import decimal_precision as dp
from odoo.fields import Date as fDate
from datetime import timedelta as td
import logging

__logger = logging.getLogger(__name__)
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_action(self):
        for record in self:
            record.active = not record.active

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = 'base.archive'
    _description = 'Library Book'  # membuat deskripsi di database
    _order = 'date_release desc, name'  # membuat urutan berdasarkan date_release kemudian name
    _rec_name = 'id'
    
    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    date_release = fields.Date('Release Date')
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('borrowed', 'Borrowec'),
         ('lost', 'Lost')],
         'State'
         )
    cover = fields.Binary(
        "Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    cover_medium = fields.Binary(
        "Medium-sized image", attachment=True,
        help="Medium-sized image of the product. It is automatically "
             "resized as a 128x128px image, with aspect ratio preserved, "
             "only when the image exceeds one of those sizes. Use this field in form views or some kanban views.")
    cover_small = fields.Binary(
        "Small-sized image", attachment=True,
        help="Small-sized image of the product. It is automatically "
             "resized as a 64x64px image, with aspect ratio preserved. "
             "Use this field anywhere a small image is required.")
    
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Updated')
    description = fields.Html(
            string='Description',
            sanitize=True,
            strip_style=False,
            translate=False,
            )
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
        )
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),  # Optional precision (total, decimals)
        )
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # (Optional) currency_field='currency_id',
        )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # Optional:
        ondelete='set null',
        context={},
        domain=[],
        )
    publisher_city = fields.Char(
        'Publisher City', related='publisher_id.city'
        )
    author_ids = fields.Many2many('res.partner', string='Authors')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
        )
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be uniqe..')
    ]  #  database constrains


    # python file constrains
    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past.')

    # add the method with the value computation logic
    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release) - today)
            book.age_days = delta.days

    # add the method implementing the logic to write on the computed field
    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)
            print book.date_release

    # To implement the logic allowing you to search on the computed field
    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]


    # add a helper method to dynamically build the list of selectable target models
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]

    # add the Reference field and use the previous function to provide the list of selectable models
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document'
        )

    # Add a helper method to check whether a state transition is allowed:
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        template = super(LibraryBook, self).create(vals)
        related_vals = {}
        if related_vals:
            template.write(related_vals)
        return template
    
    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        res = super(LibraryBook, self).write(vals)
        return res

    # Add a method to change the state of some books to a new one passed as an argument:
    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue


    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])
    
class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'
    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published Books'
        )
    book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'  # optional
        )
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books'
        )
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books'
        )

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade'
        )

class SomeModel(models.Model):
    _name = 'some.model'
    # name = fields.Char('Name', required=True)
    # email = fields.Char('Email')
    # date = fields.Date('Date')
    # is_company = fields.Boolean('Is a company')
    # parent_id = fields.Many2one('res.partner', 'Related Company')
    # child_ids = fields.One2many('res.partner', 'parent_id', 'Contacts')

    @api.multi
    def create_partner(self):
        today_str = fields.Date.context_today()
        val1 = {'name': u'Eric Idle',
                'email': u'eric.idle@example.com',
                'date': today_str}
        val2 = {'name': u'Jhon Cleese',
                'email': u'jhon.cleese@example.com',
                'date': today_str}
        partner_val = {
            'name': u'Flying Circus',
            'email': u'm.python@example.com',
            'date': today_str,
            'is_company': True,
            'child_ids': [(0, 0, val1),
                          (0, 0, val2),
                          ]
            }
        record = self.env['res.partner'].create(partner_val)

        return record


    # To update a partner, you can write a new method
    # method 1 using Combining recordsets
    @api.model
    def update_contacts(self, partner, contacts):
        partner.ensure_one()  # memastikan argument contains one record except will raise error
        if contacts:
            partner.date = fields.Date.context_today()
            partner.child_ids |= contacts


    # method 2 using update()
    # update() can use just only 1 recordsets
    @api.model
    def update_contacts_option2(self, partner, contacts):
        partner.ensure_one()
        if contacts:
            today = fields.Date.context_today()
            partner.update(
                {'date': today,
                 'child_ids': partner.child_ids | contacts}
            )


    # Searching for records
    # 1. Get an empty recordset for res.partner
    @api.model
    def find_partners_and_contacts(self, name):
        partner = self.env['res.partner']

        # search domain for your criteria
        domain = ['|',
                  '&',
                  ('is_company', '=', True),
                  ('name', 'like', name),
                  '&',
                  ('is_company', '=', False),
                  ('parent_id.name', 'like', name)
                  ]

        # 3. Call the search() method with the domain and return the recordset
        return partner.search(
                                domain,
                                # #option
                                # offset=0, #This is used to skip the N first records that match the query
                                # limit=0, #return at most N records. By default, there is no limit
                                # order=sort_specification, # his is used to force the order on the returned recordset
                                # count=boolean, # if True this returns the number of records instead of the recordset.
                                                # It defaults to False . or can use `search_count(domain)`
                            )

    # # Filtering recordsets
    # using manual function
    @api.model
    def partners_with_email(self, partners):
        def predicate(partner):
            if partner.email:
                return True
            return False
        return partners.filter(predicate)

    # using lambda function
    @api.model
    def partners_with_email_variant(self, partners):
        return partners.filter(lambda p: p.email)

    # simple filtering
    @api.model
    def partners_with_email_variant2(self, partners):
        return partners.filter('email')


    # # Traversing recordset relations
    @api.model
    def get_email_addresses(self, partner):
        partner.ensure_one()
        # Call mapped() to get the e-mail addresses of the contacts of the partner
        return partner.mapped('child_ids.email')

    def get_companies(self, partners):
        # Call mapped() to get the different companies of the partners
        return partners.mapped('parent_id')

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
