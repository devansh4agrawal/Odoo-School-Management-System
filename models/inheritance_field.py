from odoo import models, fields

class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='Custom Phone Field')