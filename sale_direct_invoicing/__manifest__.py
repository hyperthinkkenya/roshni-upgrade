# -*- coding: utf-8 -*-
# © 2017 Jérome Guerriat
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': 'Sale - Direct invoicing of confirmed Sales',
    'summary': 'Automatically create an invoice from a confirmed sale',
    'version': '13.0.0.0.0',
    'author': 'Niboo',
    'category': 'Document Management',
    'description': '''
When confirming a SO, this module will automatically create and validate the invoice

    ''',
    'license': 'AGPL-3',
    'website': 'https://www.niboo.be/',

    'depends': [
        'sale'
    ],
    'data': [
    ],
    'installable': True,
    'auto_install': False,
}
