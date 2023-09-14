from odoo import models,fields,api

class Fees(models.Model):
    _name = "fees.profile"
    _description = "Test Model"
        
    name = fields.Char('Student Name')
    fee_paid = fields.Selection([("yes", "Yes")], default='yes',required = True)