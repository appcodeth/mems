from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
from .bahttext import bahttext

TAX_RATE = 7


class RFQ(models.Model):
    _name = 'mems.rfq'
    _rec_name = 'name'
    _order = 'name desc'
    name = fields.Char('Name')
    date_order = fields.Date('Date Order', required=True, default=fields.Date.today())
    date_payment = fields.Date('Date Payment')
    tax_rate = fields.Float('Tax Rate', default=7)
    tax_type = fields.Selection([
        ('include', 'Include'),
        ('exclude', 'Exclude'),
    ], string='Tax Type', default='exclude')
    discount_type = fields.Selection([
        ('no', 'No Discount'),
        ('percent', 'Percent'),
        ('amount', 'Amount'),
    ], default='no', string='Discount Type')
    discount_rate = fields.Float(string='Discount %')
    amount_untaxed = fields.Float('Subtotal', readonly=True, store=True)
    amount_tax = fields.Float('Taxes', readonly=True, store=True)
    amount_discount = fields.Float('Discount Amount')
    amount_after_discount = fields.Float('Price after discount', readonly=True, store=True)
    amount_total = fields.Float('Total Amount', default=0, readonly=True, store=True)
    remark = fields.Text('Remark')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    payment_term_id = fields.Many2one('mems.payment_term', string='Payment Term')
    supplier_id = fields.Many2one('mems.supplier', string='Supplier', required=True)
    address = fields.Text('Address', related='supplier_id.address')
    phone = fields.Char('Phone', related='supplier_id.phone')
    fax = fields.Char('Fax', related='supplier_id.fax')
    email = fields.Char('Email', related='supplier_id.email')
    tax_id = fields.Char('Tax ID', related='supplier_id.tax_id')
    branch = fields.Char('Branch', related='supplier_id.branch')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    rfq_line = fields.One2many('mems.rfq_line', 'rfq_id')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('mems.rfq_no') or '-'
        vals['name'] = seq
        return super(RFQ, self).create(vals)

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            'amount_untaxed': 0,
            'amount_tax': 0,
            'amount_discount': 0,
            'amount_after_discount': 0,
            'amount_total': 0,
            'state': 'draft',
        })
        return super(RFQ, self).copy(default=default)

    @api.onchange('payment_term_id')
    def get_payment_term_id(self):
        pay_date = fields.Datetime.from_string(self.date_order) + \
                   timedelta(days=self.payment_term_id.number_of_day)
        self.date_payment = pay_date

    @api.onchange('rfq_line')
    def get_total_amount(self):
        subtotal = 0
        for r in self:
            for item in r.rfq_line:
                subtotal += item.amount

        discount = 0
        if self.discount_type == 'percent':
            discount = (subtotal * self.discount_rate / 100)
        elif self.discount_type == 'amount':
            discount = self.amount_discount

        price_after_discount = subtotal - discount

        self.tax_rate = TAX_RATE
        self.amount_tax = 0
        self.amount_untaxed = subtotal
        self.amount_after_discount = price_after_discount
        self.amount_total = price_after_discount

        if self.tax_type == 'include':
            amount_exclude_tax = (price_after_discount * 100) / (100 + TAX_RATE)
            self.amount_tax = price_after_discount - amount_exclude_tax
            self.amount_total = price_after_discount
        elif self.tax_type == 'exclude':
            self.amount_tax = (price_after_discount * TAX_RATE) / 100
            self.amount_total = price_after_discount + self.amount_tax

    @api.onchange('discount_type')
    def change_discount_type(self):
        self.discount_rate = 0
        self.amount_discount = 0
        self.get_total_amount()

    @api.onchange('discount_rate')
    def change_discount_rate(self):
        if self.discount_type == 'percent':
            if self.discount_rate or self.discount_rate == 0:
                self.get_total_amount()
            else:
                raise exceptions.ValidationError('Please enter a valid percent')

    @api.onchange('amount_discount')
    def change_amount_discount(self):
        if self.discount_type == 'amount':
            if self.amount_discount or self.amount_discount == 0:
                self.get_total_amount()
            else:
                raise exceptions.ValidationError('Please enter a valid amount')

    @api.onchange('tax_type')
    def get_tax_type_change(self):
        self.get_total_amount()

    @api.model
    def get_baht_text(self):
        return bahttext(self.amount_total)

    def do_rfq_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_purchase.rfq_form',
            'model': 'mems.rfq',
            'report_type': 'qweb-pdf',
        }

    def do_rfq_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.rfq.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_rfq_id': self.id,
                'default_rfq_name': self.name,
            }
        }

    def do_rfq_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.rfq.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_rfq_id': self.id,
                'default_rfq_name': self.name,
            }
        }

    def do_rfq_close(self):
        self.write({'state': 'close'})

    def do_rfq_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('mems_purchase', 'mail_template_rfq_form')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'mark_so_as_sent': True,
            'default_model': 'mems.rfq',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': ctx,
            'res_model': 'mail.compose.message',
            'view_id': compose_form_id,
            'views': [(compose_form_id, 'form')],
        }


class RFQLine(models.Model):
    _name = 'mems.rfq_line'
    rfq_id = fields.Many2one('mems.rfq', ondelete='cascade')
    part_id = fields.Many2one('mems.spare_part', string='Part')
    name = fields.Char('Name')
    description = fields.Text('Description')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    price = fields.Float('Unit Price')
    tax = fields.Float('Tax')
    discount = fields.Float('Discount')
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
