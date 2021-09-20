from odoo import models, fields


class ReturnCancelWizard(models.TransientModel):
    _name = 'mems.return.cancel.wizard'
    rtn_id = fields.Integer('Return ID')
    rtn_name = fields.Char('Return Name')

    def do_confirm_cancel(self):
        self.env['mems.return'].browse([self.rtn_id]).sudo().write({'state': 'cancel'})
