from odoo import models, fields, api
import qrcode
import io
import base64

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qr_code = fields.Binary("QR Code", attachment=True, readonly=True)

    def generate_qr_code(self):
        for record in self:
            # Generate QR Code
            qr_data = f"ID: {record.id}\nName: {record.name}\nPrice: {record.list_price}\nVariants: {len(record.product_variant_ids)}\nQuantity: {sum(record.product_variant_ids.mapped('qty_available'))}"
            qr = qrcode.make(qr_data)
            qr_image = io.BytesIO()
            qr.save(qr_image, format='PNG')
            qr_image_base64 = base64.b64encode(qr_image.getvalue()).decode('utf-8')
            record.qr_code = qr_image_base64
