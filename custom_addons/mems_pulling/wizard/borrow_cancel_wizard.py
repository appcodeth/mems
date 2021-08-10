from odoo import models, fields


class BorrowCancelWizard(models.TransientModel):
    _name = 'mems.borrow.cancel.wizard'
    borrow_id = fields.Integer('Borrow ID')
    borrow_name = fields.Char('Borrow Name')

    def do_confirm_cancel(self):
        bm = self.env['mems.borrow'].browse([self.borrow_id])
        bm.sudo().write({'state': 'cancel'})
        self.env['mems.equipment'].browse([bm.equip_id.id]).sudo().write({'state': 'active'})
