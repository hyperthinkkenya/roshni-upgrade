from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        pickings = self.mapped('picking_ids')
        for picking in pickings:
            if picking.action_assign():
                picking.auto_fill_quantity_done()
            picking.with_context(skip_overprocessed_check=True).button_validate()
        invoices = self._create_invoices()
        for invoice in invoices:
            invoice.post()
        return True


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def auto_fill_quantity_done(self):
        for line in self.move_line_ids_without_package:
            line.update({'qty_done':line.product_uom_qty})


