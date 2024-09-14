from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class BarcodeWizard(models.TransientModel):
    _name = 'barcode.wizard'
    _description = 'Barcode Wizard'
    product_barcode_qty_ids = fields.One2many('barcode.wizard.line', 'wizard_id', string='Product Barcode Quantities')

    @api.model
    def default_get(self, fields):
        res = super(BarcodeWizard, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', [])
        active_ids = [int(id) for id in active_ids] 
        _logger.info(f"Active IDs: {active_ids}")
        # if active_ids:
        products = self.env['product.template'].browse(list(map(int, active_ids)))
        barcode_qty_lines = [(0, 0, {'product_id': product.id, 'barcode_qty': 1}) for product in products]
        _logger.info(f"Barcode Lines being created: {barcode_qty_lines}")
        res.update({
            'product_barcode_qty_ids': barcode_qty_lines,
        })
        return res

    def action_generate_barcode_pdf(self):
        _logger.info(f"Active IDs: {self.env.context.get('active_ids', [])}")
        
        product_quantities = {}
        
        for line in self.product_barcode_qty_ids:
            if not line.product_id or line.barcode_qty <= 0:
                _logger.error(f"Invalid line data: Product ID = {line.product_id}, Quantity = {line.barcode_qty}")
                continue            
            _logger.info(f"Processing barcode wizard line: Product ID = {line.product_id.id}, Quantity = {line.barcode_qty}")
            product_quantities[int(line.product_id.id)] = line.barcode_qty
        
        _logger.info(f"Collected Barcode Quantities: {product_quantities}")       
        return self.env.ref('product_label_with_barcode.barcode_report').report_action(
            self, data={'product_quantities': product_quantities}
        )

class BarcodeWizardLine(models.TransientModel):
    _name = 'barcode.wizard.line'
    _description = 'Barcode Wizard Line'
    wizard_id = fields.Many2one('barcode.wizard', string='Wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.template', string='Product', required=True)
    barcode_qty = fields.Integer('Barcode Quantity', required=True, default=1)
    @api.model
    def create(self, vals):
        # Ensure the product_id is an integer
        if 'product_id' in vals:
            vals['product_id'] = int(vals['product_id'])
        _logger.info(f"Creating barcode wizard line with vals: {vals}")
        return super(BarcodeWizardLine, self).create(vals)