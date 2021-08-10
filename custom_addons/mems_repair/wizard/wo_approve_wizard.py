from odoo import models, fields


class WOApproveWizard(models.TransientModel):
    _name = 'mems.workorder.approve.wizard'
    wo_id = fields.Integer('Work Order ID')
    wo_name = fields.Char('Work Order Name')

    def do_confirm_approve(self):
        wo = self.env['mems.workorder'].browse([self.wo_id])

        total_qty = 0
        for item in wo.wo_line:
            total_qty += item.qty

        issue = self.env['mems.issue'].sudo().create({
            'wo_id': wo.id,
            'department_id': wo.department_id.id,
            'amount_qty': total_qty,
            'amount_untaxed': wo.amount_untaxed,
            'amount_tax': wo.amount_tax,
            'amount_total': wo.amount_total,
            'amount_discount': wo.amount_discount,
            'amount_after_discount': wo.amount_after_discount,
            'discount_type': wo.discount_type,
            'discount_rate': wo.discount_rate,
            'state': 'draft',
        })

        for item in wo.wo_line:
            self.env['mems.issue_line'].sudo().create({
                'issue_id': issue.id,
                'part_id': item.part_id.id,
                'uom_id': item.uom_id.id,
                'name': item.name,
                'qty': item.qty,
                'price': item.price,
            })

        wo.sudo().write({'state': 'approve'})
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'repair'})
