from odoo import models, fields


class EquipmentCancelWizard(models.TransientModel):
    _name = 'mems.equipment.cancel.wizard'
    equip_id = fields.Integer('Equipment ID')
    equip_name = fields.Char('Equipment Name')
    reason_id = fields.Many2one('mems.equipment_reason', string='Reason')

    def do_confirm_cancel(self):
        self.env['mems.equipment'].browse([self.equip_id]).sudo().write({
            'state': 'inactive',
            'note': self.reason_id.name,
        })
