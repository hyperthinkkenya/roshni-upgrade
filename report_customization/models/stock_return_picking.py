# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval



class ReturnPicking(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking'

    return_product_ids = fields.Many2many('product.product', string="Return Product")
    move_lines_pro_ids = fields.Many2many('product.product', compute="_compute_product_ids")
    has_credit_note = fields.Boolean()
    credit_invoice_id = fields.Many2one('account.move')

    @api.depends('move_lines')
    def _compute_product_ids(self):
        for rec in self:
            product_ids = []
            if rec.move_lines:
                for mv in rec.move_lines:
                    product_ids.append(mv.product_id.id)
                rec.move_lines_pro_ids = product_ids

    def create_credit_note(self):
        for rec in self:
            invoice_ids = []
            if rec.sale_id:
                if not rec.sale_id.invoice_ids.ids:
                    raise UserError(
                        _("Invoice is not generated for this order Please\
                            Create Invoice"))
                for invoice in rec.sale_id.invoice_ids:
                    if invoice.type == 'out_invoice' and \
                            invoice.state in ['draft', 'cancel']:
                        raise UserError(
                            _("It looks like one of invoice is \
                                cancelled/not validate"))
                    invoice_ids.append(invoice)
                invoice = self.env['account.move'].create({
                    'partner_id': rec.partner_id.id,
                    'type': 'out_refund',
                    'account_id': rec.partner_id.property_account_receivable_id.id,
                    'fiscal_position_id': rec.partner_id.property_account_position_id.id,
                    'invoice_date': fields.Date.context_today(rec),
                    'origin': rec.sale_id.name
                })
                for line in rec.move_lines:
                    line_values = {
                        'product_id': line.product_id.id,
                        'invoice_id': invoice.id,
                        'origin': rec.sale_id.name,
                        'quantity': line.product_uom_qty
                    }
                    # create a record in cache, apply onchange then revert back
                    # to a dictionnary
                    invoice_line = self.env['account.move.line'].new(
                        line_values)
                    invoice_line._onchange_product_id()
                    line_values = invoice_line._convert_to_write(
                        {name: invoice_line[name] for name in invoice_line._cache})
                    line_values['invoice_line_tax_ids'] = False
                    if invoice_ids:
                        for inv in invoice_ids:
                            for l in inv.invoice_line_ids:
                                if not line_values['invoice_line_tax_ids']:
                                    if l.product_id.id == line.product_id.id and l.invoice_line_tax_ids:
                                        line_values['invoice_line_tax_ids'] = [
                                            (6, 0, l.invoice_line_tax_ids.ids)]
                    invoice.write({'invoice_line_ids': [(0, 0, line_values)]})
                invoice.compute_taxes()
                xml_id = (invoice.type in ['out_refund', 'out_invoice']) and \
                    'action_invoice_out_refund' or (invoice.type in
                                               ['in_refund', 'in_invoice']) and 'action_invoice_in_refund'
                # Put the reason in the chatter
                subject = _("Invoice refund")
                body = 'Invoice Refund'
                invoice.message_post(body=body, subject=subject)
                self.has_credit_note = True
                self.credit_invoice_id = invoice.id
                if xml_id:
                    result = self.env.ref('account.%s' % (xml_id)).read()[0]
                    invoice_domain = safe_eval(result['domain'])
                    invoice_domain.append(('id', '=', invoice.id))
                    result['domain'] = invoice_domain
                    return result
                return True

    def action_see_credit_note(self):
        return {
            'name': _('Credit Note'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('id', '=', self.credit_invoice_id.id)],
        }


class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'
    _description = 'Return Picking'


    @api.model
    def default_get(self, fields):
        if len(self.env.context.get('active_ids', list())) > 1:
            raise UserError("You may only return one picking at a time!")
        res = super(ReturnPicking, self).default_get(fields)
        Quant = self.env['stock.quant']
        move_dest_exists = False
        product_return_moves = []
        picking = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        if picking:
            if picking.state != 'done':
                raise UserError(_("You may only return Done pickings"))
            for move in picking.move_lines:
                if move.product_id in picking.return_product_ids:
                    if move.scrapped:
                        continue
                    if move.move_dest_ids:
                        move_dest_exists = True
                    # Sum the quants in that location that can be returned (they should have been moved by the moves that were included in the returned picking)
                    quantity = sum(quant.quantity for quant in Quant.search([
                        # ('history_ids', 'in', move.id),
                        ('quantity', '>', 0.0), ('location_id', 'child_of', move.location_dest_id.id)
                    ]))
                    quantity = move.product_id.uom_id._compute_quantity(quantity, move.product_uom)
                    product_return_moves.append((0, 0, {'product_id': move.product_id.id, 'quantity': quantity, 'move_id': move.id}))

            if not product_return_moves:
                raise UserError(_("No products to return (only lines in Done state and not fully returned yet can be returned)!"))
            if 'product_return_moves' in fields:
                res.update({'product_return_moves': product_return_moves})
            if 'move_dest_exists' in fields:
                res.update({'move_dest_exists': move_dest_exists})
            if 'parent_location_id' in fields and picking.location_id.usage == 'internal':
                res.update({'parent_location_id': picking.picking_type_id.warehouse_id and picking.picking_type_id.warehouse_id.view_location_id.id or picking.location_id.location_id.id})
            if 'original_location_id' in fields:
                res.update({'original_location_id': picking.location_id.id})
            if 'location_id' in fields:
                location_id = picking.location_id.id
                if picking.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
                    location_id = picking.picking_type_id.return_picking_type_id.default_location_dest_id.id
                res['location_id'] = location_id
        return res
