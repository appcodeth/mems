from odoo import models, fields


class CalibrateCompleteWizard(models.TransientModel):
    _name = 'mems.cal.complete.wizard'
    cal_id = fields.Integer('Calibrate ID')
    cal_name = fields.Char('Calibrate Name')

    def do_confirm_complete(self):
        cal = self.env['mems.calibration'].browse([self.cal_id])
        cal.sudo().write({'state': 'close'})
        self.env['mems.equipment'].browse([cal.equip_id.id]).sudo().write({'state': 'active'})
