from odoo import models, fields


class CalibrateCancelWizard(models.TransientModel):
    _name = 'mems.cal.cancel.wizard'
    cal_id = fields.Integer('Calibrate ID')
    cal_name = fields.Char('Calibrate Name')

    def do_confirm_cancel(self):
        cal = self.env['mems.calibration'].browse([self.cal_id])
        cal.sudo().write({'state': 'draft'})
        self.env['mems.equipment'].browse([cal.equip_id.id]).sudo().write({'state': 'active'})
