from odoo import models, fields


class WorkOrderCancelWizard(models.TransientModel):
    _name = 'mems.wo.cancel.wizard'
    wo_id = fields.Integer('WorkOrder ID')
    wo_name = fields.Char('WorkOrder Name')

    def do_confirm_cancel(self):
        wo = self.env['mems.workorder'].browse([self.wo_id])
        wo.sudo().write({'state': 'cancel'})
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'active'})
