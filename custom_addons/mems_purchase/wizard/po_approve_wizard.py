from odoo import models, fields
from datetime import datetime


class POApproveWizard(models.TransientModel):
    _name = 'mems.po.approve.wizard'
    po_id = fields.Integer('PO ID')
    po_name = fields.Char('PO Name')

    def do_confirm_approve(self):
        # get purchase order by id
        purchase = self.env['mems.purchase'].browse([self.po_id])

        # calculate total qty
        total_qty = 0
        total_amount = 0
        for item in purchase.purchase_line:
            total_qty += item.qty
            total_amount += item.amount

        # create receive header
        receive = self.env['mems.receive'].sudo().create({
            'po_id': purchase.id,
            'supplier_id': purchase.supplier_id.id,
            'date_rcv': datetime.now(),
            'discount_rate': purchase.discount_rate,
            'amount_qty': total_qty,
            'amount_total': total_amount,
            'state': 'draft',
        })

        # create receive line items
        for item in purchase.purchase_line:
            self.env['mems.receive_line'].sudo().create({
                'rcv_id': receive.id,
                'part_id': item.part_id.id,
                'uom_id': item.uom_id.id,
                'name': item.name,
                'qty': item.qty,
                'price': item.price,
                'amount': item.amount,
            })

        # update purchase status
        purchase.sudo().write({'state': 'approve'})
