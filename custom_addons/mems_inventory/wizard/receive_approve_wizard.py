from odoo import models, fields, exceptions, _
from datetime import datetime


class ReceiveApproveWizard(models.TransientModel):
    _name = 'mems.receive.approve.wizard'
    rcv_id = fields.Integer('Receive ID')
    rcv_name = fields.Char('Receive Name')

    def do_confirm_approve(self):
        receive = self.env['mems.receive'].browse([self.rcv_id])

        # validate unit of measure
        for line in receive.receive_line:
            if not line.uom_id:
                raise exceptions.ValidationError(_('Please select uom in receive line'))
            if not line.price:
                raise exceptions.ValidationError(_('Please enter product price in receive line'))

        for line in receive.receive_line:
            # calculate purchase uom qty
            base_uom = line.part_id.uom_id
            receive_uom = line.uom_id
            ratio = base_uom.ratio
            if base_uom.id != receive_uom.id:
                if receive_uom.type == 'bigger':
                    ratio = base_uom.ratio * receive_uom.ratio
                elif receive_uom.type == 'smaller':
                    ratio = base_uom.ratio / receive_uom.ratio

            new_qty = line.qty * ratio
            last_purchase = datetime.now()

            # update spare part stock qty
            spare_part = self.env['mems.spare_part'].browse([line.part_id.id])
            spare_part.sudo().write({
                'last_purchase_date': last_purchase,
                'stock_qty': spare_part.stock_qty + new_qty,
            })

            # insert to stock move to journal
            self.env['mems.stock_move'].sudo().create({
                'name': line.part_id.name,
                'doc_id': self.rcv_id,
                'doc_name': self.rcv_name,
                'doc_type': 'receive',
                'product_id': line.part_id.id,
                'product_code': line.part_id.code,
                'user_id': self.env.user.id,
                'qty': new_qty,
                'uom_id': line.part_id.uom_id.id,
                'purchase_qty': line.qty,
                'purchase_uom_id': line.uom_id.id,
                'amount': line.price,
                'move_type': 'in',
                'move_date': datetime.now(),
            })
        receive.sudo().write({'state': 'complete'})
