from odoo import models, fields

class Teachers(models.Model):
    _name = "teacher.profile"
    _description = "Test Model"
    _rec_name = "teacher"
     
    teacher = fields.Char(string="Teacher")
    class_name = fields.Char(string="Class Name")