from odoo import models, fields


class ReceiveCancelWizard(models.TransientModel):
    _name = 'mems.receive.cancel.wizard'
    rcv_id = fields.Integer('Receive ID')
    rcv_name = fields.Char('Receive Name')

    def do_confirm_cancel(self):
        self.env['mems.receive'].browse([self.rcv_id]).sudo().write({'state': 'cancel'})
