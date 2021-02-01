# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class  SaleOrder(models.Model):
    _inherit = 'sale.order'

    amended = fields.Boolean('Amended')

    def print_loading_sheet(self):
        return self.env.ref('report_customization.report_loading_sheet').report_action(self)


    def quotation_to_sale(self):
        sale_ids = self.env.context.get('active_ids')
        sale_orders = self.env['sale.order'].browse(sale_ids)
        for sale in sale_orders:
            if sale.state in ['draft', 'sent']:
                sale.action_confirm()


    def create_invoices_for_sale(self):
        sale_ids = self.env.context.get('active_ids')
        sale_orders = self.env['sale.order'].browse(sale_ids)
        for sale in sale_orders:
            if sale.state == 'sale' and sale.order_line.ids:
                sale.action_invoice_create()


    def write(self, values):
        if values.get('order_line'):
            values['amended'] = True
        result = super(SaleOrder, self).write(values)
        return result



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.constrains('discount')
    def _check_discount(self):
        for rec in self:
            if rec.discount:
                if rec.discount > 100:
                    raise ValidationError(_('You can not set more than discount of product price'))



class  ProductUom(models.Model):
    _inherit = 'uom.uom'

    general_name = fields.Char('UOM')


class AccountInvoice(models.Model):
    _inherit = "account.move"

    vehicle_number = fields.Char('Vehicle Number')
    dispatch_reg_num = fields.Char('Dispatch Reg. No.')
    custom_entry_number = fields.Char('Custom Entry Number')


    def custom_invoice_print(self):
        self.ensure_one()
        self.sent = True
        return self.env.ref('report_customization.account_invoices_custom').report_action(self)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_flag = fields.Selection([('import', 'IMPORT'), ('local', 'LOCAL')], string='Customer Flag')

class AccountBatchDeposit(models.Model):
    _inherit = 'account.batch.payment'

    pay_in_slip = fields.Char('Pay In Slip For')


    def get_company_bank(self):
        user = self.env['res.users'].browse(self.env.uid)
        bank_id = self.env['res.partner.bank'].search([('partner_id', '=', user.partner_id.id)])
        return bank_id

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    branch = fields.Char('Branch')
    bank_acc_id = fields.Many2one('res.bank', string="Bank")
