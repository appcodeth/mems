from odoo import models, fields
from datetime import datetime


class SparePartAdjustWizard(models.TransientModel):
    _name = 'mems.spare_part.adjust.wizard'
    doc_id = fields.Integer('ID')
    name = fields.Char('Name')
    code = fields.Char('Code')
    uom_id = fields.Integer('Uom')
    stock_qty = fields.Float('Stock Qty')
    new_qty = fields.Float('New Qty')
    amount = fields.Float('Amount')

    def do_confirm_adjust(self):
        # update current stock qty
        self.env['mems.spare_part'].browse([self.doc_id]).sudo().write({
            'stock_qty': self.new_qty
        })

        # insert the stock_move to keep history for tracking
        data = {
            'name': self.name,
            'doc_name': self.code,
            'doc_type': 'adjust',
            'move_type': 'adjust',
            'qty': self.new_qty,
            'amount': self.amount,
            'user_id': self.env.user.id,
            'move_data': datetime.now(),
        }

        if self.doc_id:
            data['id'] = self.doc_id
            data['product_id'] = self.doc_id

        if self.uom_id:
            data['uom_id'] = self.uom_id
        self.env['mems.stock_move'].sudo().create(data)
