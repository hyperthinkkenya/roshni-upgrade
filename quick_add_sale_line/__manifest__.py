# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name' : 'Add Sale Line In Batch',
    'version': '12.0.0.1',
    'summary': 'Add multiple sale line one time',
    'category': 'Sale',
    'description': """User can add multiple sale line at a time""",
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'depends': ['base', 'product', 'sale_management'],
    'data': [
             'wizard/select_products_wizard_view.xml',
             'views/sale_views.xml',
             'security/ir.model.access.csv'
            ],
    'installable': True,
}
