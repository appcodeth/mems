from odoo import models, fields, api


class PM(models.Model):
    _name = 'mems.pm'
    name = fields.Char('Name')
    equip_id = fields.Many2one('mems.equipment', string='Equipment', domain=[('state', '=', 'active')])
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('close', 'Close'),
    ], default='draft', string='State')
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    pm_line = fields.One2many('mems.pm_line', 'pm_id')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.pm_no') or '-'
        vals['name'] = seq
        return super(PM, self).create(vals)

    def do_pm_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_equipment.pm_form',
            'model': 'mems.pm',
            'report_type': 'qweb-pdf',
        }

    def do_pm_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.pm.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_pm_id': self.id,
                'default_pm_name': self.name,
            }
        }

    def do_pm_complete(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.pm.complete.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_pm_id': self.id,
                'default_pm_name': self.name,
            }
        }

    def do_pm_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.pm.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_pm_id': self.id,
                'default_pm_name': self.name,
            }
        }


class PMItem(models.Model):
    _name = 'mems.pm_checklist'
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')


class PMLine(models.Model):
    _name = 'mems.pm_line'
    pm_id = fields.Many2one('mems.pm', ondelete='cascade')
    checklist_id = fields.Many2one('mems.pm_checklist', ondelete='cascade')
    description = fields.Text('Description')
    is_done = fields.Boolean('Is Done')
