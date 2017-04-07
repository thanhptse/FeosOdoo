from odoo import fields, models

class People(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean("Instructor", default=False)
    type_people = fields.Selection([('student', "Student"),('teacher',"Teacher")],string="People Type", default='student')
    class_id = fields.Many2one("school.class", string="Attended Classes")