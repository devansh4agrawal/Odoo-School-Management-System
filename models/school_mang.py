from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import datetime
from odoo import _

class Students(models.Model):
    _name = "students.profile"
    _description = "Student"
    _inherit = 'mail.thread'

    # Students Information
    school_abc = fields.Char(readonly=True)
    form = fields.Char(readonly=True)
    student_profile_image = fields.Image(string="Profile Image")
    name = fields.Char(string="Name")
    gender = fields.Selection([('M', 'Male'), ('F', 'Female')], string="Gender")
    # standard = fields.Integer(string="Standard", group_operator= False)
    student_email = fields.Char(string="Email")
    # standard = fields.Many2one('standard.profile',string="Standard")
    standard = fields.Selection([("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6), ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("11", 11), ("12", 12)], string="Standard", group_operator=False)
    student_stream = fields.Selection([("science", "Science"), ("commerce", "Commerce"), ("arts", "Arts")], string="Stream")
    division = fields.Selection([("A", "A"), ("B", "B"), ("C", "C")])
    roll_no = fields.Integer(string="Roll Number", help="Enter only Integer value.")
    teacher = fields.Many2one(comodel_name="teacher.profile", string="Class Teacher", help="It may differ.")
    enrollment_no = fields.Char(string="Enrollment Number", readonly=True, default=lambda self: _('New'))
    address_line1 = fields.Char(string="Address Line 1")
    address_line2 = fields.Char(string="Address Line 2")
    city = fields.Char(string="City")
    country = fields.Many2one('res.country', string="Country")
    state = fields.Many2one('res.country.state', string="State", store=True)
    phone = fields.Char(string="Phone Number", tracking=True)
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", readonly=True, group_operator=False)
    date = fields.Date(default=fields.Date.today,readonly=True, string="Registration Date")
    birthday_month = fields.Char(string="Birthday Month", compute='_compute_month', store=True, readonly=True)
    admission_status = fields.Char(string="Admission Status", readonly=True, default="In Process")
    student_fee = fields.Char(string='Fee Status', default="Unpaid", readonly=True)
    fee_mode = fields.Char(string='Fee Mode')
    receipt_number = fields.Char(string='Receipt Number')
    student_result = fields.Char(string='Result')

    # Parent Details Field

    father_name = fields.Char(string="Father's Name")
    mother_name = fields.Char(string="Mother's Name")
    guardian_name = fields.Char(string="Gurdian's Name")
    relation = fields.Many2one(comodel_name="relation.profile", string="Relation")
    parents_phone = fields.Char(string="Parent's Phone Number")
    parents_email = fields.Char(string="Email")
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", readonly=True, default=lambda self: self.env['res.currency'].search([('name', '=', 'INR')]).id)
    parents_yearly_income = fields.Monetary(string="Parent's Yearly Income", currency_field="currency_id")

    # Previous School Details Field

    previous_school_name = fields.Char(string="School Name")
    previous_school_enrollment_no = fields.Integer(string="Previous Enrollment Number")
    previous_school_admission_date = fields.Date(string="Admission Date")
    previous_school_leave_date = fields.Date(string="Leaving Date")

    # Fee Details Field
    extra_charges = fields.Integer(readonly=True)
    fee_per_month = fields.Integer(string="Monthly Fee", compute='_cal_monthly_fee', store=True)
    total_labs = fields.One2many(comodel_name='labs.profile', inverse_name='lab_id' ,string="Total Labs" , store = True )
    total_lab_fee = fields.Integer(string="Total Lab Fee", compute='_cal_total_lab_fee', store=True)
    transportation = fields.Selection([("Yes", "Yes"), ("No", "No")], string="Avail Transportation", default="No")
    distance = fields.Float(string="Distance")
    total_fee = fields.Integer(string="Total Fee", compute='_cal_total_fee', store=True)
    total_fee_quater = fields.Integer(string="Quaterly Fee", compute='_cal_quaterly_fee')  
    fee_outstanding = fields.Monetary(string="Left Fee", currency_field="currency_id")
    
    @api.onchange('standard')
    def _res_name(self):
        self.school_abc = self.env['ir.config_parameter'].get_param('school.school_name')
        self.form = self.env['ir.config_parameter'].get_param('school.form_type')
        self.extra_charges = self.env['ir.config_parameter'].get_param('school.hidden_charges')

    @api.depends('standard')
    def _cal_monthly_fee(self):
        for record in self:
            a = int(record.standard)
            if (1 <= a <= 5):
                # for rec in record:
                record.fee_per_month = 2500
            elif (5 <= a <= 10):
                # for rec in record:
                record.fee_per_month = 4500
            elif (11 <= a <= 12):
                # for rec in record:
                record.fee_per_month = 6000

    @api.depends('total_labs')
    def _cal_total_lab_fee(self):
        for record in self:
            if (len(record.total_labs) > 0):
                record.total_lab_fee = len(record.total_labs) * 1500
            else:
                record.total_lab_fee = 0

    @api.depends('fee_per_month', 'total_lab_fee', 'transportation', 'distance','extra_charges')
    def _cal_total_fee(self):
        for record in self:
            if (record.transportation == "Yes"):
                print(record.extra_charges,"if")
                record.total_fee = (record.fee_per_month * 11.5) + record.total_lab_fee + (record.distance * 8 * 24 * 12) + record.extra_charges
            else:
                print(record.extra_charges,"else")
                record.total_fee = (record.fee_per_month * 11.5) + record.total_lab_fee + record.extra_charges 

    @api.depends('total_fee')
    def _cal_quaterly_fee(self):
        for record in self:
            record.total_fee_quater = (record.total_fee/4)

    # Age Calculation

    @api.onchange('date_of_birth')
    def _cal_age(self):
        if self.date_of_birth:
            d1 = self.date
            d2 = self.date_of_birth
            d3 = relativedelta(d1, d2).years
            if (d3 < 4):
                raise ValidationError("Age can't be less than 4.")
            else:
                self.age = d3

    # Assigning teacher

    @api.onchange('standard')
    def _standard(self):
        b = int(self.standard)
        if b:
            self.teacher = self.env['teacher.profile'].search(
                [('class_name', '=', b)], limit=1).id

    @api.model
    def create(self, vals):
        if vals.get('enrollment_no', _('New')) == _('New'):
            vals['enrollment_no'] = self.env['ir.sequence'].next_by_code(
                'enrollment_sequence') or _('New')
        res = super(Students, self).create(vals)
        return res

    # DOB & Gender Validation

    @api.constrains('date_of_birth')
    def _check_dob(self):
        for record in self:
            if not (record.date_of_birth):
                raise ValidationError("Please enter Date of Birth")

    # Gender Validation

    @api.constrains('gender')
    def _check_gender(self):
        for record in self:
            if not (record.gender):
                raise ValidationError("Please select Gender")

    # Validating Phone Number

    @api.constrains('phone')
    def _check_phone_number(self):
        for record in self:
            if not (record.phone and ((len(record.phone) == 10) and record.phone.isdigit())):
                raise ValidationError("Incorrect Phone Number")

    # Parent's Phone Validation

    @api.constrains('parents_phone')
    def _check_parents_phone_number(self):
        for rec in self:
            if not (rec.parents_phone and ((len(rec.parents_phone) == 10) and rec.parents_phone.isdigit())):
                raise ValidationError("Incorrect Parent's Phone Number")

    # Name Validation

    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not (self.name or self.phone):
                raise ValidationError("Name or phone field is empty.")

    # standard Validation

    @api.constrains('standard')
    def _check_standard(self):
        for rec in self:
            if int(rec.standard) > 12:
                raise ValidationError(
                    "Standard should be less than or equal to 12.")

    # Birthday Month Grouping

    @api.depends('date_of_birth')
    def _compute_month(self):
        for record in self:
            if record.date_of_birth:
                record.birthday_month = record.date_of_birth.strftime('%B')

    # Phone Duplication Task

    @api.constrains('phone')
    def _phone_duplication(self):
        for rec in self:
            if rec.phone:
                phone_duplicate = self.search(
                    [('phone', '=', rec.phone), ('id', '!=', rec.id)])
                if phone_duplicate:
                    raise ValidationError('Phone number already exists')

    # Getting State based on Country

    @api.onchange('country')
    def set_state_on_country(self):
        if self.country:
            ids = self.env['res.country.state'].search(
                [('country_id', '=', self.country.id)])
            return {
                'domain': {'state': [('id', 'in', ids.ids)], }
            }

    # Opening pages in New Mode using URL Action

    def open_new(self):
        context = self._context.copy()
        return {
            "name": _("Class Teachers"),
            "type": 'ir.actions.act_window',
            'view_mode': 'form',
            "res_model": 'teacher.profile',
            'view_id': 'student_teacher_data',
            "views": [[False, "form"]],
            "target": 'new',
        }

    def open_self(self):
        context = self._context.copy()
        return {
            "name": _("Tree View"),
            "type": 'ir.actions.act_window',
            'view_mode': 'form',
            "res_model": 'students.profile',
            'view_id': 'students_register_view',
            "views": [[False, "form"]],
            "target": 'new',
        }

    # Searching sudent using name, enrollment_no, phone using name_get and name_search

    def name_get(self):
        result = []
        for x in self:
            name = x.name + ' - ' + x.enrollment_no
            result.append((x.id, name))
        # print(result,"KKKKKKKKKKKKKKKKKKK")
        return result

    @api.model
    def _name_search(self, name="", args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            args += ['|', ('enrollment_no', operator, name),
                     ('phone', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        # temp = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        # print(temp, "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV")
        # return temp

    # Labs Filtration

    @api.onchange('enrollment_no')
    def _student_labs(self):
        if self.enrollment_no:
            self.total_labs = self.env['labs.profile'].search([('lab_id', '=', self.enrollment_no)])

    # def write(self, values):
    #     res = super(Students, self).write(values)
    #     print(res,"ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    #     return res
    
    def action_send_email(self):
        record = self.env['students.profile'].search([('admission_status','=','Confirmed')])
        for rec in record:
            if (rec.admission_status == 'Confirmed'):
                mail_template = self.env.ref('school.email_template_student')
                mail_template.send_mail(self.id, force_send=True)
                
        
    def action_psql(self):
        # query = """SELECT name, standard FROM students_profile"""
        # query = """SELECT name, standard FROM students_profile WHERE standard = '6'"""       
        # query = """UPDATE students_profile SET name='QWERTY', division= 'A' WHERE id = 81; """
        # query = """DELETE FROM students_profile WHERE id=7"""
        
        # query = """SELECT name, standard, division FROM teacher_profile CROSS JOIN students_profile """
        # query = """SELECT name, standard, division FROM teacher_profile INNER JOIN students_profile ON teacher_profile.class_name = students_profile.standard """
        # query = """SELECT name, standard, division FROM teacher_profile LEFT OUTER JOIN students_profile ON teacher_profile.class_name = students_profile.standard """
        # query = """SELECT name, standard, division FROM teacher_profile RIGHT OUTER JOIN students_profile ON teacher_profile.class_name = students_profile.standard"""
        # query = """SELECT name, standard, division FROM teacher_profile FULL OUTER JOIN students_profile ON teacher_profile.class_name = students_profile.standard"""
        
        # self.env.cr.execute(query)
        # res = self.env.cr.fetchall()
        print("---------------------------------------")
        # print(res)
