from odoo import models, fields, api
from datetime import datetime


class Restore(models.Model):
    _name = 'mems.restore'
    name = fields.Char('Name')
    borrow_id = fields.Many2one('mems.borrow', string='Borrow No.', domain=[('state', '=', 'borrow')])
    department = fields.Char('Department', readonly=True, store=True)
    equip_id = fields.Many2one('mems.equipment', related='borrow_id.equip_id', string='Equipment')
    borrow_date = fields.Date('Borrow Date', related='borrow_id.expect_date', readonly=True)
    restore_date = fields.Date('Restore Date', default=datetime.now())
    over_day = fields.Integer('Over Day', compute='cal_duration_day')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('restore', 'Restore'),
        ('cancel', 'Cancel'),
        ('close', 'Close'),
    ], default='draft', string='State')
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.onchange('borrow_id')
    def get_borrow_detail(self):
        self.department = self.borrow_id.department_id.name

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.restore_no') or '-'
        vals['name'] = seq
        return super(Restore, self).create(vals)

    @api.depends('borrow_date', 'restore_date')
    def cal_duration_day(self):
        for r in self:
            if r.borrow_date and r.restore_date:
                restore_date = fields.Datetime.from_string(r.restore_date)
                borrow_date = fields.Datetime.from_string(r.borrow_date)
                r.over_day = (restore_date - borrow_date).days
            else:
                r.over_day = 0

    def do_restore_approve(self):
        bw = self.env['mems.borrow'].browse([self.borrow_id.id])
        bw.sudo().write({'state': 'close'})
        self.env['mems.equipment'].browse([bw.equip_id.id]).sudo().write({'state': 'active'})
        self.write({'state': 'close'})
