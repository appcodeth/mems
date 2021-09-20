from odoo import models, fields


class WorkOrderCancelWizard(models.TransientModel):
    _name = 'mems.wo.cancel.wizard'
    wo_id = fields.Integer('WorkOrder ID')
    wo_name = fields.Char('WorkOrder Name')

    def do_confirm_cancel(self):
        wo = self.env['mems.workorder'].browse([self.wo_id])
        # cancel this workorder
        wo.sudo().write({'state': 'cancel'})

        # release allocation for equipment
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'active'})

        # cancel corresponding sr
        self.env['mems.sr'].search([('name', '=', wo.sr_no)]).sudo().write({'state': 'cancel'})
