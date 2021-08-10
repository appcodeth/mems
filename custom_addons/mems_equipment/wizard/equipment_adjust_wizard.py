from odoo import models, fields


class EquipmentAdjustWizard(models.TransientModel):
    _name = 'mems.equipment.adjust.wizard'
    equip_id = fields.Integer('Equipment ID')
    equip_name = fields.Char('Equipment Name')
    equip_qty = fields.Float('Equipment Qty')

    def do_confirm_adjust(self):
        self.env['mems.equipment'].browse([self.equip_id]).sudo().write({'stock_qty': self.equip_qty})
