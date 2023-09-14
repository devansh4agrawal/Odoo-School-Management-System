from odoo import models, fields, api
from odoo import _

class StudentWizard(models.TransientModel):
    _name = "students.wizard"
    _description = "Fee Status"

    def _get_default_students(self):
        return self.env['students.profile']

    enrollment_number = fields.Many2one(
        'students.profile', "Enrollment Number")
    payment_mode = fields.Selection(
        [("Cash", "Cash"), ("Cheque", "Cheque"), ("Online", "Online (UPI)")], string="Payment Mode")
    payment_mode_cheque = fields.Char(string="Cheque Number")
    payment_mode_online = fields.Char(string="UTR Number")
    student_fee = fields.Selection([('Unpaid','UnPaid'),('Paid','Paid')], string ='Fee Status', default="Paid")
    receipt = fields.Char(string="Reciept", readonly=True, default='New')

    def set_student_level(self):
        if self.enrollment_number:
            a = self.env['students.profile'].search(
                [('id', '=', self.enrollment_number.id)])
            a.student_fee = self.student_fee
            if self.student_fee == "Paid":
                if self.receipt == "New":
                    self.receipt = self.env['ir.sequence'].next_by_code('receipt_sequence') or _('New')

            a.fee_mode = self.payment_mode 
            a.receipt_number =  self.receipt