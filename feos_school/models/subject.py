from odoo import fields, models

class Subject(models.Model):
    _name = "school.subject"
    
    name = fields.Char(required=True)
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    color = fields.Char(
    string="Color",
    help="Choose your color"
)
    
class Input(models.Model):
    _name = "school.input"
    
    subject_id = fields.Many2one("school.subject", ondelete="cascade", string="Subject", required=True)
    student_id = fields.Many2one("res.partner", ondelete="cascade", string="Student", required=True)
    value = fields.Float(digits=(6, 2))
    
