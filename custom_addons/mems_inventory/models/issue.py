from odoo import models, fields, api, exceptions
from datetime import datetime

TAX_RATE = 7


class Issue(models.Model):
    _name = 'mems.issue'
    _order = 'name desc'
    _rec_name = 'name'
    name = fields.Char('Issue No')
    date_issue = fields.Date('Issue Date', default=fields.Date.today())
    department_id = fields.Many2one('mems.department', string='Department', required=True)
    wo_id = fields.Many2one('mems.workorder', string='Work Order')
    doc_no = fields.Char('Document No')
    reason_id = fields.Many2one('mems.issue_reason', string='Reason')
    amount_qty = fields.Float('Total Qty', readonly=True, store=True)
    amount_tax = fields.Float('Taxes', readonly=True, store=True)
    amount_total = fields.Float('Total Amount', readonly=True, store=True)
    remark = fields.Text('Remark')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('complete', 'Complete'),
        ('cancel', 'Cancel'),
    ], default='draft', string='State')
    issue_line = fields.One2many('mems.issue_line', 'issue_id')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.issue_no') or '-'
        vals['name'] = seq
        return super(Issue, self).create(vals)

    @api.onchange('issue_line')
    def get_total_amount(self):
        total_qty = 0
        subtotal = 0
        for r in self:
            for item in r.issue_line:
                total_qty += item.qty
                subtotal += item.amount

        discount = 0
        price_after_discount = subtotal - discount
        self.amount_qty = total_qty
        self.amount_tax = (price_after_discount * TAX_RATE) / 100
        self.amount_total = price_after_discount + self.amount_tax

    def do_issue_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.issue.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_issue_id': self.id,
                'default_issue_name': self.name,
            }
        }

    def do_issue_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.issue.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_issue_id': self.id,
                'default_issue_name': self.name,
            }
        }

    def do_issue_print(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_inventory.issue_form',
            'model': 'mems.issue',
            'report_type': 'qweb-pdf',
        }


class IssueLine(models.Model):
    _name = 'mems.issue_line'
    issue_id = fields.Many2one('mems.issue', ondelete='cascade')
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
