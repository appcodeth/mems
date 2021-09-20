import pytz
from datetime import datetime
from odoo import models, fields, api


class Payment(models.Model):
    _name = 'mems.payment'
    _rec_name = 'name'
    _order = 'name desc'
    name = fields.Char(string='Name', required=True)
    doc_id = fields.Integer(string='Doc Id')
    doc_name = fields.Char(string='Doc Name')
    doc_type = fields.Char(string='Doc Type')
    doc_amount = fields.Float(string='Doc Amount')
    pay_date = fields.Datetime(string='Pay Date', default=fields.Date.today())
    pay_method = fields.Char(string='Pay Method')
    pay_amount = fields.Float(string='Pay Amount')
    pay_receive = fields.Float(string='Pay Receive')
    memo = fields.Text(string='Note')
    bank_account_id = fields.Many2one('mems.bank_account', string='Bank Account')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('payment.payment_no') or '-'
        vals['name'] = seq
        return super(Payment, self).create(vals)
