
# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import fields, models, api


import datetime


class DispathWizard(models.TransientModel):
    _name = "dispatch.wizard"
    _description = 'Dispatch Wizard'

    def _get_default_dispatch_reg(self):
        return self.env['dispatch.register'].browse(self.env.context.get('active_ids'))

    invoice_ids = fields.Many2many('account.move', domain="[('dispatch_reg_num', '=', False), ('state', '!=', 'draft'), ('type','in',('out_invoice', 'out_refund'))]")


    def button_save(self):
        for record in self:
            if record.invoice_ids:
                for invoice in record.invoice_ids:
                    rec = self._get_default_dispatch_reg()
                    rec.dispathched_line_ids.create({
                        'invoice_id': invoice.id,
                        'order_id': rec.id,
                        'inv_date': invoice.invoice_date,
                        # 'account_id': invoice..id,
                        'partner_id': invoice.partner_id.id,
                        'period': invoice.invoice_date.month
                    })
        return True
