from odoo import models, fields, api
from datetime import datetime


class Borrow(models.Model):
    _name = 'mems.borrow'
    _order = 'name desc'
    _rec_name = 'name'
    name = fields.Char('Name')
    equip_id = fields.Many2one('mems.equipment', string='Equipment', required=True, domain=[('state', '=', 'active')])
    department_id = fields.Many2one('mems.department', string='Department', required=True)
    borrow_date = fields.Date('Borrow Date', required=True, default=fields.Date.today())
    expect_date = fields.Date('Expected Date')
    restore_date = fields.Date('Restore Date')
    duration_day = fields.Integer('Duration Day', compute='cal_duration_day')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrow', 'Borrow'),
        ('cancel', 'Cancel'),
        ('close', 'Close'),
    ], default='draft', string='State')
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.borrow_no') or '-'
        vals['name'] = seq
        return super(Borrow, self).create(vals)

    @api.depends('borrow_date', 'expect_date')
    def cal_duration_day(self):
        for r in self:
            if r.borrow_date and r.expect_date:
                expected_date = fields.Datetime.from_string(r.expect_date)
                borrow_date = fields.Datetime.from_string(r.borrow_date)
                r.duration_day = (expected_date - borrow_date).days
            else:
                r.duration_day = 0

    def do_borrow_approve(self):
        borrow = self.env['mems.borrow'].browse([self.id])
        borrow.sudo().write({'state': 'borrow'})
        self.env['mems.equipment'].browse([borrow.equip_id.id]).sudo().write({'state': 'borrow'})

    def do_borrow_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_pulling.borrow_form',
            'model': 'mems.borrow',
            'report_type': 'qweb-pdf',
        }

    def do_borrow_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.borrow.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_borrow_id': self.id,
                'default_borrow_name': '%s' % self.name,
            }
        }
