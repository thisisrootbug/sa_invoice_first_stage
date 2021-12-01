# -*- coding: utf-8 -*-
{
    'name': 'ZATCA Tax Invoice First Stage',
    'version': '1.0',
    'installed_version': '1.0',
    'category': 'Accounting',
    'author': 'Alhaidab-ITIS',
    'summary': 'Meet the first staget requirement for the Saudi Arabia Tax Invoice and Simple Invoice',
    'website': 'https://www.alhaidab.dolibarr.sd',
    'description': """
    -Add an automaticly generated QRCode in invoice form views and reports with the required information.
    -Disable invoice delete after the posted State
    -Disable invoice modification after the posted State
    -Change the views and reports design to meet the fist stage requirements.
    """,
    'depends': [ 'account' ],
    'data': [
        'report/report_invoice_document.xml',
        'report/simple_invoice.xml',
        'views/account_move_inherit.xml',
    ],
    'images': [ 'static/description/banner.png', ],
    'installable': True,
    'application': True,
    'price': 49,
    'currency': 'USD',
    'license': "LGPL-3",
}
