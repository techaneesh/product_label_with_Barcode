from odoo import api, models, fields

class ProductLabelConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_contact_details = fields.Boolean(string="Show Contact Details")
    show_product_category = fields.Boolean(string="Show Product Category")
    show_price = fields.Boolean(string="Show Price")
    
    # Storing the options in ir.config_parameter for persistence
    def set_values(self):
        super(ProductLabelConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('product_label_with_barcode.show_contact_details', self.show_contact_details)
        self.env['ir.config_parameter'].sudo().set_param('product_label_with_barcode.show_product_category', self.show_product_category)
        self.env['ir.config_parameter'].sudo().set_param('product_label_with_barcode.show_price', self.show_price)

    @api.model
    def get_values(self):
        res = super(ProductLabelConfigSettings, self).get_values()
        res.update(
            show_contact_details=self.env['ir.config_parameter'].sudo().get_param('product_label_with_barcode.show_contact_details'),
            show_product_category=self.env['ir.config_parameter'].sudo().get_param('product_label_with_barcode.show_product_category'),
            show_price=self.env['ir.config_parameter'].sudo().get_param('product_label_with_barcode.show_price'),
        )
        return res
