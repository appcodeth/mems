from odoo import models, fields


class RFQCancelWizard(models.TransientModel):
    _name = 'mems.rfq.cancel.wizard'
    rfq_id = fields.Integer('RFQ ID')
    rfq_name = fields.Char('RFQ Name')

    def do_confirm_cancel(self):
        self.env['mems.rfq'].browse([self.rfq_id]).sudo().write({'state': 'cancel'})
