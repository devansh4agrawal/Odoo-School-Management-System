from odoo import models, fields

class Standard(models.Model):
    _name = "standard.profile"
    _description = "Test Model"
    _rec_name = "standards"
     
    standards = fields.Char(string="Standard")