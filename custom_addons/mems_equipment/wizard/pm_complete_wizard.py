from odoo import models, fields


class PMCompleteWizard(models.TransientModel):
    _name = 'mems.pm.complete.wizard'
    pm_id = fields.Integer('PM ID')
    pm_name = fields.Char('PM Name')

    def do_confirm_complete(self):
        pm = self.env['mems.pm'].browse([self.pm_id])
        pm.sudo().write({'state': 'close'})
        self.env['mems.equipment'].browse([pm.equip_id.id]).sudo().write({'state': 'active'})
