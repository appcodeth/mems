from odoo import models, fields, api


class Calibration(models.Model):
    _name = 'mems.calibration'
    name = fields.Char('Name')
    equip_id = fields.Many2one('mems.equipment', string='Equipment', domain=[('state', '=', 'active')])
    supplier_id = fields.Many2one('mems.supplier', string='Supplier')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('close', 'Close'),
    ], default='draft', string='State')
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.calibrate_no') or '-'
        vals['name'] = seq
        return super(Calibration, self).create(vals)

    def do_cal_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_equipment.calibrate_form',
            'model': 'mems.calibration',
            'report_type': 'qweb-pdf',
        }

    def do_cal_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.cal.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_cal_id': self.id,
                'default_cal_name': self.name,
            }
        }

    def do_cal_complete(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.cal.complete.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_cal_id': self.id,
                'default_cal_name': self.name,
            }
        }

    def do_cal_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.cal.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_cal_id': self.id,
                'default_cal_name': self.name,
            }
        }
