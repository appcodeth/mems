from odoo import models, fields
from datetime import datetime


class WOApproveWizard(models.TransientModel):
    _name = 'mems.workorder.approve.wizard'
    wo_id = fields.Integer('Work Order ID')
    wo_name = fields.Char('Work Order Name')

    def do_confirm_approve(self):
        # get workorder by id
        wo = self.env['mems.workorder'].browse([self.wo_id])

        # calculate total qty and amount
        total_qty = 0
        total_amount = 0
        for item in wo.wo_line:
            if item.part_id.type == 'product':
                total_qty += item.qty
                total_amount += item.amount

        # create issue header
        issue = self.env['mems.issue'].sudo().create({
            'wo_id': wo.id,
            'department_id': wo.department_id.id,
            'date_issue': datetime.now(),
            'amount_qty': total_qty,
            'amount_total': total_amount,
            'state': 'draft',
        })

        # create issue line item
        for item in wo.wo_line:
            if item.part_id.type == 'product':
                self.env['mems.issue_line'].sudo().create({
                    'issue_id': issue.id,
                    'part_id': item.part_id.id,
                    'uom_id': item.uom_id.id,
                    'name': item.name,
                    'qty': item.qty,
                    'price': item.price,
                    'amount': item.amount,
                })

        # update workorder status
        wo.sudo().write({'state': 'approve'})

        # update equipment status
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'repair'})
