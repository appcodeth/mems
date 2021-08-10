from odoo import models, fields


class POApproveWizard(models.TransientModel):
    _name = 'mems.po.approve.wizard'
    po_id = fields.Integer('PO ID')
    po_name = fields.Char('PO Name')

    def do_confirm_approve(self):
        po = self.env['mems.purchase'].browse([self.po_id])
        po.sudo().write({'state': 'approve'})
