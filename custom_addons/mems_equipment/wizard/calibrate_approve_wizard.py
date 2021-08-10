from odoo import models, fields


class CalibrateApproveWizard(models.TransientModel):
    _name = 'mems.cal.approve.wizard'
    cal_id = fields.Integer('Calibrate ID')
    cal_name = fields.Char('Calibrate Name')

    def do_confirm_approve(self):
        cal = self.env['mems.calibration'].browse([self.cal_id])
        cal.sudo().write({'state': 'approve'})
        self.env['mems.equipment'].browse([cal.equip_id.id]).sudo().write({'state': 'calibrate'})
