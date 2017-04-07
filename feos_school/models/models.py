# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Grade(models.Model):
    _name = "school.grade"
    
    name = fields.Char(string="Class name", required=True)
    description = fields.Text()
    class_ids = fields.One2many(
        'school.class', 'grade_id', string="Class")

class Class(models.Model):
    _name = "school.class"
    
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    grade_id = fields.Many2one('school.grade',ondelete='cascade', string="Grade", required=True)
    student_ids = fields.One2many('res.partner', 'class_id', string="Students")
    quantity = fields.Integer(string="Quantity", compute='_onchange_quantity', store=True)
    #male_student_ids = fields.One2many('res.partner', 'class_id', string="Male Students",domain=[('sex','=','male')])
    #female_student_ids = fields.One2many('res.partner', 'class_id', string="FeMale Students",domain=[('sex','=','female')])
    
    taken_seats = fields.Float(string="Taken seats")
    
    @api.multi
    @api.depends('student_ids')
    def _onchange_quantity(self):
        for r in self:
            print '_onchange_quantity: ', len(r.student_ids),r.student_ids
            r.quantity = len(r.student_ids)
        
        
        
        
        
        