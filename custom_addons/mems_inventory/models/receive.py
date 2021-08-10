from odoo import models, fields, api, exceptions
from datetime import datetime


class Receive(models.Model):
    _name = 'mems.receive'
    name = fields.Char('Receive No')
    po_id = fields.Many2one('mems.purchase', string='Purchase', required=True)
    supplier_id = fields.Many2one('mems.supplier', string='Supplier')
    date_rcv = fields.Date('Receive Date', default=datetime.now())
    doc_no = fields.Char('Document No')
    discount_rate = fields.Float(string='Discount %')
    amount_qty = fields.Float('Total Qty', readonly=True, store=True)
    amount_total = fields.Float('Total Amount', readonly=True, store=True)
    remark = fields.Text('Remark')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('complete', 'Complete'),
        ('cancel', 'Cancel'),
    ], default='draft', string='State')
    receive_line = fields.One2many('mems.receive_line', 'rcv_id')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.receive_no') or '-'
        vals['name'] = seq
        return super(Receive, self).create(vals)

    @api.onchange('receive_line')
    def get_total_amount(self):
        total_qty = 0
        total_amount = 0
        for r in self:
            for item in r.receive_line:
                total_qty += item.qty
                total_amount += item.amount

        self.amount_qty = total_qty
        self.amount_total = total_amount

    def do_receive_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.receive.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_rcv_id': self.id,
                'default_rcv_name': self.name,
            }
        }

    def do_receive_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.receive.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_rcv_id': self.id,
                'default_rcv_name': self.name,
            }
        }

    def do_receive_print(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_inventory.receive_form',
            'model': 'mems.receive',
            'report_type': 'qweb-pdf',
        }


class ReceiveLine(models.Model):
    _name = 'mems.receive_line'
    rcv_id = fields.Many2one('mems.receive', ondelete='cascade')
    part_id = fields.Many2one('mems.spare_part', string='Part')
    name = fields.Char('Name')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    price = fields.Float('Price')
    amount = fields.Float('Amount', readonly=True, store=True)

    @api.onchange('part_id')
    def get_part_change(self):
        if not self.part_id:
            return
        self.uom_id = self.part_id.purchase_uom_id or self.part_id.uom_id
        self.price = self.part_id.cost_price
        if not self.qty:
            self.qty = 1
        self.amount = self.price * self.qty

    @api.onchange('price', 'qty')
    def price_qty_change(self):
        if not self.qty:
            self.qty = 1
        if not self.price:
            self.price = 0
        self.amount = self.price * self.qty
