from odoo import fields, models

class ExcelWizard(models.TransientModel):
    _name = 'excel.wizard'
    _description = 'Excel Report Wizard'
    report_type = fields.Selection([('brand', 'Brand')], string="Report Type", default="brand")
    data = {}
    
    def generate_report(self):
        products = self.env['students.profile'].search([])
        lines = []
        for product in products.mapped('id'):
        lines.append([
            # product.image_128 if product.image_128 else "",
            product.name,
            product.standard,
            product.division,
            product.teacher
        ])
        self.data['lines'] = lines
        return self.env.ref('price_list_report.price_list_report').report_action(self,data={})