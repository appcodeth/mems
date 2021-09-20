from odoo import models, fields


class WorkOrderCloseWizard(models.TransientModel):
    _name = 'mems.wo.close.wizard'
    wo_id = fields.Integer('WorkOrder ID')
    wo_name = fields.Char('WorkOrder Name')

    def do_confirm_close(self):
        wo = self.env['mems.workorder'].browse([self.wo_id])
        wo.sudo().write({'state': 'close'})
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'active'})
        self.env['mems.sr'].search([('name', '=', wo.sr_no)]).sudo().write({'state': 'close'})
