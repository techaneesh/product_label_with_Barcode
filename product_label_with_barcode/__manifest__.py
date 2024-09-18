{
    'name': 'Product Label with Barcode',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Automatically generate barcode sequence for new products',
    # 'description': """
    # This module generates a barcode sequence in the format PR-YearMonthDay/Product_id 
    # for each new product and stores it and You can generate product label also in PDF format by this and manage inventory through Scanner.
    # """,
    'description': """
    This module streamlines your inventory management by:
    - Generating multiple barcodes with a single click.
    - Creating barcodes and QR codes for both existing and new products.
    - Producing customizable PDF product labels with barcodes and QR codes.
    Optimize your product labeling and tracking with ease.
    """,
    'author': 'PyCraze',
    'depends': ['base', 'account', 'product', 'web'],
    'data': [
        'views/product_template_barcode_views.xml',
        'views/barcode_wizard_view.xml',
        'views/product_qrcode_view.xml',
        'views/setting_view.xml',
        'report/barcode_report_template.xml',
        'report/barcode_report_action.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png', 'static/description/main_screenshot.png'],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'price': 5.00,  # Added price in USD
    'currency': 'USD',
}