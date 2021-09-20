from odoo import models, fields
from datetime import datetime


class SRApproveWizard(models.TransientModel):
    _name = 'mems.sr.approve.wizard'
    sr_id = fields.Integer('SR ID')
    sr_name = fields.Char('SR Name')

    def do_confirm_approve(self):
        sr = self.env['mems.sr'].browse([self.sr_id])
        self.env['mems.workorder'].sudo().create({
            'sr_no': sr.name,
            'department_id': sr.department_id.id,
            'equip_id': sr.equip_id.id,
            'equip_brand': sr.equip_brand,
            'problem_text': sr.problem_text,
            'image_attachments': sr.image_attachments,
            'responsible_id': sr.responsible_id.id,
            'remark': sr.remark,
            'date_plan': sr.date_plan,
            'date_finish': sr.date_finish,
            'company_id': sr.company_id.id,
            'state': 'draft',
        })

        # update sr status
        sr.sudo().write({'state': 'approve'})
