from odoo import models, fields

class StudentWizard(models.TransientModel):
    _name = "students.admission.wizard"
    _description = "Admission Status"
    
    def _get_default_students(self):
        return self.env['students.profile']

    enrollment_number = fields.Many2one('students.profile', string = "Enrollment Number")
    admission_status = fields.Selection([('Cancelled','Cancelled'),('Confirmed','Confirmed')], string = 'Admission Status')

    def set_student_status(self):
        if self.enrollment_number:
            a = self.env['students.profile'].search(
                [('id', '=', self.enrollment_number.id)])
            a.admission_status = self.admission_status