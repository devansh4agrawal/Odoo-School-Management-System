from odoo import models,fields

class Relation(models.Model):
    _name = "relation.profile"
    _description = "Test Model"
    _rec_name = "rel"
    
    rel = fields.Char(string="Relation", required=True)