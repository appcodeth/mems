from odoo import models, fields
from datetime import datetime


class SparePartAdjustWizard(models.TransientModel):
    _name = 'mems.spare_part.adjust.wizard'
    product_id = fields.Integer('ID')
    name = fields.Char('Name')
    code = fields.Char('Code')
    uom_id = fields.Integer('Uom')
    stock_qty = fields.Float('Stock Qty')
    new_qty = fields.Float('New Qty')
    amount = fields.Float('Amount')

    def do_confirm_adjust(self):
        part = self.env['mems.spare_part'].browse([self.product_id])

        # check type of product
        if part.type == 'product':
            # update current stock qty
            part.sudo().write({
                'stock_qty': self.new_qty
            })

            # insert the stock_move to keep history for tracking
            data = {
                'doc_id': None,
                'doc_name': '',
                'doc_type': 'adjust',
                'move_type': 'adjust',
                'qty': self.new_qty,
                'purchase_qty': self.new_qty,
                'amount': self.amount,
                'user_id': self.env.user.id,
                'move_date': datetime.now(),
                'name': self.name,
                'product_id': self.product_id,
                'product_code': self.code,
            }
            if self.uom_id:
                data['uom_id'] = self.uom_id
                data['purchase_uom_id'] = self.uom_id
            self.env['mems.stock_move'].sudo().create(data)
        else:
            print('** product type is service **')
