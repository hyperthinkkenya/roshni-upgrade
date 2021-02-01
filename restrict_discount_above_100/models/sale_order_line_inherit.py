# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import models, api, fields, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('discount')
    def _onchange_sale_order_line_discount(self):
        warning = {}
        if self.discount > 100:
            warning = {
                    'title': _("Warning"),
                    'message': _("You can not give discount more than 100%")
                    }
            return {'warning': warning}

    def write(self, values):
        res = super(SaleOrderLine,self).write(values)
        if self.discount > 100:
            raise UserError(_('You can not give discount more than 100%'))
        return res

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine,self).create(vals)
        if res.discount > 100.0:
            raise UserError(_('You can not give discount more than 100%'))
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('discount')
    def _onchange_move_line_discount(self):
        warning = {}
        if self.discount > 100:
            warning = {
                    'title': _("Warning"),
                    'message': _("You can not give discount more than 100%")
                    }
            return {'warning': warning}

    def write(self, values):
        res = super(AccountMoveLine,self).write(values)
        if self.discount > 100:
            raise UserError(_('You can not give discount more than 100%'))
        return res

    @api.model
    def create(self, vals):
        res = super(AccountMoveLine,self).create(vals)
        if res.discount > 100.0:
            raise UserError(_('You can not give discount more than 100%'))
        return res
