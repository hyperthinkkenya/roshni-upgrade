# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

{
    'name': 'Report Customization',
    'version': '13.0.1.0',
    'summary': 'Loading Sheet, Invoice & Delivery Report',
    'description': """
    """,
    'author': 'Caret IT Solutions Pvt. Ltd',
    'website': 'http://www.caretit.com',
    'category': 'Reports',
    'depends': ['sale_management', 'account', 'account_accountant', 'sale_stock', 'account_batch_payment'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/dispatch_view.xml',
        'views/sale_view.xml',
        'views/view_stock_return_picking.xml',
        'report/loading_sheet_report.xml',
        'report/report_invoice_custom.xml',
        'report/dispatch_reg_report.xml',
        'report/account_batch_deposit_report.xml',
        'wizard/vat_report_view.xml',
        'wizard/dispatch_reg_view.xml',
    ],
    'installable': True,
}
