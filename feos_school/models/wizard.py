from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'school.wizard'
    
    def _default_student(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))
        
    student_id = fields.Many2one('res.partner', string="Student", required=True, default=_default_student)
    grade_ids = fields.Many2many('school.grade', string="Grade", required=True)
    
    @api.multi
    def subscribe(self):
        for grade in self.grade_ids:
            grade.class_ids |= self.grade_ids.class_ids
        return {}