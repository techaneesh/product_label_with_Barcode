import base64
from io import BytesIO
from odoo import models, fields, api
from datetime import datetime
from barcode.writer import ImageWriter
from odoo.tools import barcode
import barcode
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
            product._compute_barcode_image()
        return products
    barcode_image = fields.Binary("Barcode Image", compute="_compute_barcode_image")

    @api.depends('barcode')
    def _compute_barcode_image(self):
        for product in self:
            if product.barcode:
                barcode_str = self._generate_barcode_image(product.barcode)
                product.barcode_image = base64.b64encode(barcode_str).decode('utf-8')
            else:
                product.barcode_image = False

    def _generate_barcode_image(self, barcode_value):
        barcode_class = barcode.get_barcode_class('code128')
        barcode_instance = barcode_class(barcode_value, writer=ImageWriter())
        buffer = BytesIO()
        barcode_instance.write(buffer)
        return buffer.getvalue()
    
    def action_generate_barcode_for_selected(self):
        """Generate barcodes for selected products"""
        for product in self:
            if not product.barcode:
                today_str = datetime.today().strftime('%Y%m%d')
                barcode_sequence = f'PR-{today_str}/{product.id}'
                product.barcode = barcode_sequence
            # Generate the barcode image
            product._compute_barcode_image()
            
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
        company = self.env.company
        return {
            'docs': products,
            'product_quantities': product_quantities,
            'company': company,
        }