from odoo import models, fields, api

class StudentResult(models.TransientModel):
    _name = "students.result"
    _description = "Student Result"

    def _get_default_students(self):
        return self.env['students.profile']

    enrollment_number = fields.Many2one(
        'students.profile', "Enrollment Number")
    student_result = fields.Selection([("Pass","Pass"),("Fail","Fail")], string="Result")
       
    
    def set_student_result(self):
        if self.enrollment_number:
            a = self.env['students.profile'].search(
                [('id', '=', self.enrollment_number.id)])
            a.student_result = self.student_result
            if(self.student_result == "Pass"):
                if int(a.standard)<=11:
                    b = int(a.standard)
                    a.standard = str((int(a.standard)+1))
                    a.teacher = self.env['teacher.profile'].search([('class_name', '=', a.standard)], limit=1).id