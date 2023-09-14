from odoo import models, fields

class ConfSetting(models.TransientModel):
    _inherit = "res.config.settings"
   
    school_name = fields.Char(string="School Name", store=True)
    form_type = fields.Char(string="Form Type", store=True)
    hidden_charge = fields.Integer(string="Hidden Charge")  
    
    
    def set_values(self):
        super(ConfSetting, self).set_values()
        config_param = self.env['ir.config_parameter'].sudo()
        self.env['students.profile'].sudo().search([]).write({'school_abc': self.school_name, 'form':self.form_type, 'extra_charges':self.hidden_charge})
        config_param.set_param('school.school_name', self.school_name)
        config_param.set_param('school.form_type', self.form_type)
        config_param.set_param('school.hidden_charge', self.hidden_charge)


    def get_values(self):
        res = super(ConfSetting, self).get_values()
        config_param = self.env['ir.config_parameter'].sudo()
        res.update(
            hidden_charge = config_param.get_param('school.hidden_charge', default=1000)
        )

        return res