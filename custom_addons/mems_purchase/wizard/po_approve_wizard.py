from odoo import models, fields


class POApproveWizard(models.TransientModel):
    _name = 'mems.po.approve.wizard'
    po_id = fields.Integer('PO ID')
    po_name = fields.Char('PO Name')

    def do_confirm_approve(self):
        po = self.env['mems.purchase'].browse([self.po_id])
        po.sudo().write({'state': 'approve'})


        # purchase = self.env['mems.purchase'].browse([self.po_id])
        #
        # total_qty = 0
        # for item in purchase.purchase_line:
        #     total_qty += item.qty
        #
        # receive = self.env['mems.receive'].sudo().create({
        #     'po_id': purchase.id,
        #     'supplier_id': purchase.supplier_id.id,
        #     'amount_qty': total_qty,
        #     'amount_untaxed': purchase.amount_untaxed,
        #     'amount_tax': purchase.amount_tax,
        #     'amount_total': purchase.amount_total,
        #     'amount_discount': purchase.amount_discount,
        #     'amount_after_discount': purchase.amount_after_discount,
        #     'discount_type': purchase.discount_type,
        #     'discount_rate': purchase.discount_rate,
        #     'state': 'draft',
        # })
        #
        # for item in purchase.purchase_line:
        #     self.env['mems.receive_line'].sudo().create({
        #         'rcv_id': receive.id,
        #         'part_id': item.part_id.id,
        #         'uom_id': item.uom_id.id,
        #         'name': item.name,
        #         'qty': item.qty,
        #         'price': item.price,
        #     })
        #
        # purchase.sudo().write({'state': 'approve'})
