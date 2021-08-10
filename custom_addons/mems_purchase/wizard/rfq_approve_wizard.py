from odoo import models, fields


class RFQApproveWizard(models.TransientModel):
    _name = 'mems.rfq.approve.wizard'
    rfq_id = fields.Integer('RFQ ID')
    rfq_name = fields.Char('RFQ Name')

    def do_confirm_approve(self):
        # get RFQ data
        rfq = self.env['mems.rfq'].browse([self.rfq_id])

        # create purchase header
        data_dict = {
            'ref_rfq': rfq.name,
            'date_payment': rfq.date_payment,
            'tax_rate': rfq.tax_rate,
            'tax_type': rfq.tax_type,
            'discount_type': rfq.discount_type,
            'discount_rate': rfq.discount_rate,
            'amount_untaxed': rfq.amount_untaxed,
            'amount_tax': rfq.amount_tax,
            'amount_discount': rfq.amount_discount,
            'amount_after_discount': rfq.amount_after_discount,
            'amount_total': rfq.amount_total,
            'remark': rfq.remark,
            'state': 'draft',
            'user_id': rfq.user_id.id,
            'company_id': rfq.company_id.id,
        }

        if rfq.payment_term_id:
            data_dict['payment_term_id'] = rfq.payment_term_id.id
        if rfq.supplier_id:
            data_dict['supplier_id'] = rfq.supplier_id.id
        purchase = self.env['mems.purchase'].sudo().create(data_dict)

        # create purchase line
        for line in rfq.rfq_line:
            item_dict = {
                'po_id': purchase.id,
                'name': line.name,
                'description': line.description,
                'qty': line.qty,
                'price': line.price,
                'tax': line.tax,
                'discount': line.discount,
                'amount': line.amount,
            }
            if line.part_id:
                item_dict['part_id'] = line.part_id.id
            if line.uom_id:
                item_dict['uom_id'] = line.uom_id.id
            self.env['mems.purchase_line'].sudo().create(item_dict)

        # finally write RFQ update approve status
        rfq.sudo().write({'state': 'approve'})
