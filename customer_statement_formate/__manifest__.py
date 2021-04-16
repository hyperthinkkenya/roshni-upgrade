# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           # 
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name' : 'Customer Statement Reports',
    'version': '13.0.0.0',
    'summary': 'Customer Statement Report from customers due payment',
    'category': 'Account',
    'description': """Customer Statement Report from customers due payment""",
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'website': 'http://www.caretit.com',
    'depends': ['account_reports', 'account_accountant', 'account_followup'],
    'data': [
        'views/report_followup.xml',
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/followup.xml',
    ],
    'installable': True,
}
