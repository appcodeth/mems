from odoo import models, fields, exceptions


class SRCancelWizard(models.TransientModel):
    _name = 'mems.sr.cancel.wizard'
    sr_id = fields.Integer('SR ID')
    sr_name = fields.Char('SR Name')

    def do_confirm_cancel(self):
        sr = self.env['mems.sr'].browse([self.sr_id])
        wos = self.env['mems.workorder'].search([('sr_no', '=', sr.name), ('state', 'in', ['approve', 'vendor', 'complete'])])
        if len(wos):
            raise exceptions.ValidationError("Can't cancel because workorder is opened!!")

        # cancel workorder corresponding to sr
        self.env['mems.workorder'].search([('sr_no', '=', sr.name), ('state', 'in', ['draft'])]).sudo().write({'state': 'cancel'})

        # cancel this sr
        sr.sudo().write({'state': 'cancel'})
