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

    @api.constrains('discount')
    def restrict_discount_above_100(self):
        if any(line.discount > 100 for line in self):
            raise UserError(_("Discount value cannot be greater than 100"))

    @api.onchange('discount')
    def onchnage_discount(self):
        if self.discount > 100:
            raise UserError(_("Discount value cannot be greater than 100"))


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('discount')
    def restrict_discount_above_100(self):
        if any(line.discount > 100 for line in self):
            raise UserError(_("Discount value cannot be greater than 100"))

    @api.onchange('discount')
    def onchnage_discount(self):
        if self.discount > 100:
            raise UserError(_("Discount value cannot be greater than 100"))
