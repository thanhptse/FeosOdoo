from odoo import fields, models, api

class People(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean("Instructor", default=False)
    type_people = fields.Selection([('student', "Student"),('teacher',"Teacher")],string="People Type", default='student')
    class_id = fields.Many2one("school.class", string="Attended Classes")
    
    demo = fields.Char(string='People Reference',readonly=True)
    
    @api.model
    def create(self, vals):
        if vals:
            vals['demo'] = self.env['ir.sequence'].get('res.partner')
            return super(People, self).create(vals)
            