from odoo import models,fields

class Labs(models.Model):
    _name = "labs.profile"
    _description = "Student Labs"
    _rec_name = "labs"
    
    labs = fields.Selection([('Computer',"Computer Lab"),('Science',"Science Lab"),('Physics',"Physics Lab"),('Chemistry',"Chemistry Lab")], string = "Labs")
    # labs = fields.Char(string="Labs")
    lab_id = fields.Many2one(comodel_name='students.profile', string="Lab Id")