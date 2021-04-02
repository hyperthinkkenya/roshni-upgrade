# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models
import datetime


class DispatchRegisterLine(models.Model):
    _name = 'dispatch.register.line'
    _description = 'Dispath Register Line'

    name = fields.Char(string='Name', readonly=True)
    order_id = fields.Many2one('dispatch.register', ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string="Inv. No.", required=True)
    inv_date = fields.Date('Inv. Date')
    period = fields.Char('Period')
    # account_id = fields.Many2one('account.account', string="Acc No")
    comment = fields.Text('Comments')
    partner_id = fields.Many2one('res.partner', string="Customer Name")
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.user.company_id.currency_id.id)
    invoice_amt = fields.Monetary(string='Invoice Amount', compute="_get_subtotal", readonly=True, store=True, track_visibility='always')

    @api.onchange('invoice_id')
    def onchange_invoice_id(self):
        self.inv_date = self.invoice_id.invoice_date
        # self.account_id = self.invoice_id.account_id
        self.partner_id = self.invoice_id.partner_id
        if self.inv_date:
            date = datetime.datetime.strptime(self.inv_date, "%Y-%m-%d")
            self.period = date.month

    @api.depends('invoice_id.amount_total')
    def _get_subtotal(self):
        for do in self:
            do.invoice_amt = do.invoice_id.amount_total

    @api.model
    def create(self, vals):
        res = super(DispatchRegisterLine, self).create(vals)
        if res.invoice_id:
            res.invoice_id.dispatch_reg_num = res.order_id.name
        return res

    def unlink(self):
        self.invoice_id.dispatch_reg_num = False
        return super(DispatchRegisterLine, self).unlink()


class DispatchRegister(models.Model):
    _name = "dispatch.register"
    _inherit = ['mail.thread']
    _description = 'Dispath Register'

    name = fields.Char(string="Name", readonly=True, default=lambda self: ('New'))
    reg_date = fields.Datetime(string='Date')
    veh_reg_no = fields.Char(string='Vehical Reg No.')
    driver = fields.Char(string='Driver')
    loader = fields.Char(string='Loader')
    dispathched_line_ids = fields.One2many('dispatch.register.line', 'order_id', string='Dispath Order Lines')
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True, default=lambda self: self.env.user.company_id.currency_id.id)
    amount_total = fields.Monetary(string='Total Value',  compute="_account_all", readonly=True, store=True, track_visibility='always')
    total_line = fields.Integer(string='Total Lines', compute="_count_total_lines", store=True, readonly=True)

    @api.depends('dispathched_line_ids')
    def _count_total_lines(self):
        for do in self:
            do.total_line = len(do.dispathched_line_ids)

    @api.depends('dispathched_line_ids.invoice_amt')
    def _account_all(self):
        for do in self:
            for line in do.dispathched_line_ids:
                do.amount_total += line.invoice_id.amount_total

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('dispatch.register') or 'New'
        result = super(DispatchRegister, self).create(vals)
        return result