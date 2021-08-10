import pytz
from datetime import datetime
from odoo import models, fields, api, exceptions, _


class PaymentWizard(models.TransientModel):
    _name = 'mems.purchase.payment.wizard'
    po_id = fields.Many2one('mems.purchase', string='Purchase Order', required=True)
    supplier_id = fields.Many2one('mems.supplier', string='Supplier')
    bank_account_id = fields.Many2one('mems.bank_account', string='Bank Account')
    pay_date = fields.Datetime(string='Payment Date', required=True, default=datetime.now(pytz.timezone('UTC')))
    pay_method = fields.Selection([('cash', 'Cash'), ('transfer', 'Transfer')], string='Payment Method', default='cash')
    pay_amount = fields.Float(string='Payment Amount')
    pay_receive = fields.Float(string='Payment Receive')
    memo = fields.Text(string='Note')

    @api.multi
    def action_save_payment(self):
        if not self.pay_receive:
            raise exceptions.ValidationError('Please enter payment receive')

        self.env['mems.payment'].sudo().create({
            'doc_id': self.po_id,
            'doc_name': self.po_id.name,
            'doc_amount': self.po_id.amount_total,
            'doc_type': 'purchase',
            'pay_date': self.pay_date,
            'pay_method': self.pay_method,
            'pay_amount': self.pay_amount,
            'pay_receive': self.pay_receive,
            'bank_account_id': self.bank_account_id.id,
            'memo': self.memo,
        })

        sql = """
            select
                coalesce(sum(pay_receive), 0) as sum_receive
            from mems_payment
            where doc_id={0} and doc_type='{1}'""".format(self.po_id.id, 'purchase')
        self.env.cr.execute(sql)
        res = self.env.cr.dictfetchone()

        remaining_amount = self.po_id.amount_total - res['sum_receive']
        if remaining_amount <= 0:
            po = self.env['mems.purchase'].browse([self.po_id.id])
            po.sudo().write({
                'state': 'paid',
            })
