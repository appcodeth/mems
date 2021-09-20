from odoo import models, fields, api


class Calibration(models.Model):
    _name = 'mems.calibration'
    _order = 'name desc'
    _rec_name = 'name'
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
    remark = fields.Text('Remark')
    file_attachments = fields.Many2many('ir.attachment', string='File Attachments')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    calibration_line = fields.One2many('mems.calibration_line', 'cal_id')

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


class CalibrationChecklist(models.Model):
    _name = 'mems.calibration_checklist'
    name = fields.Char('Name', required=True)
    value = fields.Char('Spec Value')
    unit = fields.Char('Unit')
    description = fields.Text('Description')


class CalibrationLine(models.Model):
    _name = 'mems.calibration_line'
    cal_id = fields.Many2one('mems.calibration', ondelete='cascade')
    checklist_id = fields.Many2one('mems.calibration_checklist', ondelete='cascade')
    checklist_value = fields.Char('Spec. Value', related='checklist_id.value', readonly=True, store=True)
    checklist_unit = fields.Char('Unit', related='checklist_id.unit', readonly=True, store=True)
    diff_value = fields.Char('Diff Value')
    real_value = fields.Char('Real Value')
    is_done = fields.Boolean('Is Done')
    description = fields.Text('Description')
