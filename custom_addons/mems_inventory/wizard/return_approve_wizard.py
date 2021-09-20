from odoo import models, fields, exceptions, _
from datetime import datetime


class ReturnApproveWizard(models.TransientModel):
    _name = 'mems.return.approve.wizard'
    rtn_id = fields.Integer('Return ID')
    rtn_name = fields.Char('Return Name')

    def do_confirm_approve(self):
        rtn = self.env['mems.return'].browse([self.rtn_id])

        # validate unit of measure
        for line in rtn.return_line:
            if not line.uom_id:
                raise exceptions.ValidationError(_('Please select uom in return line'))
            if not line.price:
                raise exceptions.ValidationError(_('Please enter product price in return line'))

        for line in rtn.return_line:
            if line.part_id.type == 'service':
                continue
            # calculate purchase uom qty
            base_uom = line.part_id.uom_id
            return_uom = line.uom_id
            ratio = base_uom.ratio or 1
            if base_uom.id != return_uom.id:
                if return_uom.type == 'bigger':
                    ratio = base_uom.ratio * return_uom.ratio
                elif return_uom.type == 'smaller':
                    ratio = base_uom.ratio / return_uom.ratio
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
                'doc_id': self.rtn_id,
                'doc_name': self.rtn_name,
                'doc_type': 'return',
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
        rtn.sudo().write({'state': 'complete'})
