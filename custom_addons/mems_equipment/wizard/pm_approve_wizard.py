from odoo import models, fields


class PMApproveWizard(models.TransientModel):
    _name = 'mems.pm.approve.wizard'
    pm_id = fields.Integer('PM ID')
    pm_name = fields.Char('PM Name')

    def do_confirm_approve(self):
        pm = self.env['mems.pm'].browse([self.pm_id])
        pm.sudo().write({'state': 'approve'})
        self.env['mems.equipment'].browse([pm.equip_id.id]).sudo().write({'state': 'pm'})
