from odoo import models, fields


class IssueCancelWizard(models.TransientModel):
    _name = 'mems.issue.cancel.wizard'
    issue_id = fields.Integer('Issue ID')
    issue_name = fields.Char('Issue Name')

    def do_confirm_cancel(self):
        self.env['mems.issue'].browse([self.issue_id]).sudo().write({'state': 'cancel'})
