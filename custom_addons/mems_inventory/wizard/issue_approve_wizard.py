from odoo import models, fields, exceptions, _
from datetime import datetime


class IssueApproveWizard(models.TransientModel):
    _name = 'mems.issue.approve.wizard'
    issue_id = fields.Integer('Issue ID')
    issue_name = fields.Char('Issue Name')

    def do_confirm_approve(self):
        issue = self.env['mems.issue'].browse([self.issue_id])

        # validate unit of measure
        for line in issue.issue_line:
            if not line.uom_id:
                raise exceptions.ValidationError(_('Please select uom in issue line'))
            if not line.price:
                raise exceptions.ValidationError(_('Please enter product price in issue line'))

        for line in issue.issue_line:
            if line.part_id.type == 'service':
                continue
            # calculate purchase uom qty
            base_uom = line.part_id.uom_id
            issue_uom = line.uom_id
            ratio = base_uom.ratio
            if base_uom.id != issue_uom.id:
                if issue_uom.type == 'bigger':
                    ratio = base_uom.ratio * issue_uom.ratio
                elif issue_uom.type == 'smaller':
                    ratio = base_uom.ratio / issue_uom.ratio

            new_qty = line.qty * ratio
            last_purchase = datetime.now()

            # update spare part stock qty (decrement)
            spare_part = self.env['mems.spare_part'].browse([line.part_id.id])
            spare_part.sudo().write({
                'stock_qty': spare_part.stock_qty - new_qty,
            })

            # insert to stock move to journal
            self.env['mems.stock_move'].sudo().create({
                'name': line.part_id.name,
                'doc_id': self.issue_id,
                'doc_name': self.issue_name,
                'doc_type': 'issue',
                'product_id': line.part_id.id,
                'product_code': line.part_id.code,
                'user_id': self.env.user.id,
                'qty': new_qty,
                'uom_id': line.part_id.uom_id.id,
                'purchase_qty': line.qty,
                'purchase_uom_id': line.uom_id.id,
                'amount': line.price,
                'move_type': 'out',
                'move_date': datetime.now(),
            })
        issue.sudo().write({'state': 'complete'})
