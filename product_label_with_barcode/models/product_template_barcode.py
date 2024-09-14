from odoo import models, fields, api
from datetime import datetime
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    @api.model
    def create(self, vals):
        # Call super to create the product
        vals['barcode'] = vals.get('barcode', '')
        products = super(ProductTemplate, self).create(vals)
        for product in products:
            # Generate barcode sequence
            today_str = datetime.today().strftime('%Y%m%d')
            barcode_sequence = f'PR-{today_str}/{product.id}'
            product.barcode = barcode_sequence

        return products
    def action_generate_barcode_pdf(self):
        return {
            'name': 'Generate Barcodes',
            'type': 'ir.actions.act_window',
            'res_model': 'barcode.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('product_label_with_barcode.view_barcode_wizard_form').id,
            'target': 'new',
            'context': {'active_ids': self.ids}
        }
class BarcodeReport(models.AbstractModel):
    _name = 'report.product_label_with_barcode.barcode_report_template'
    @api.model
    def _get_report_values(self, docids, data=None):
        product_quantities = data.get('product_quantities', {})
        # products = self.env['product.template'].browse(product_quantities.keys())
        products = self.env['product.template'].browse(list(map(int, product_quantities.keys())))
        return {
            'docs': products,
            'product_quantities': product_quantities,
        }