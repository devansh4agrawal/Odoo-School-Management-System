from odoo import models, fields

class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"
   
    custom_field = fields.Boolean(string="Global Field", store=True, config_parameter='school.custom_field')