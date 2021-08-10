from odoo import models, fields, api, exceptions
from datetime import datetime

TAX_RATE = 7


class WorkOrder(models.Model):
    _name = 'mems.workorder'
    name = fields.Char('Name')
    date_order = fields.Date('Order Date', default=datetime.now())
    department_id = fields.Many2one('mems.department', string='Department', required=True)
    equip_id = fields.Many2one('mems.equipment', string='Equipment', required=True, domain=[('state', '=', 'active')])
    equip_code = fields.Char('Code', related='equip_id.code', readonly=True, store=True)
    equip_brand = fields.Char('Brand', readonly=True, store=True)
    equip_model = fields.Char('Model', related='equip_id.model_name', readonly=True, store=True)
    equip_price = fields.Float('Unit Price', related='equip_id.unit_price', readonly=True, store=True)
    equip_sn = fields.Char('S/N', related='equip_id.serial_no', readonly=True, store=False)
    equip_warty_type = fields.Selection('Warranty Type', related='equip_id.warranty_type', readonly=True, store=False)
    equip_warty_expire = fields.Date('Warranty Expire', related='equip_id.warranty_end_date', readonly=True, store=False)
    equip_image = fields.Binary('Image', related='equip_id.image', readonly=True, store=False)
    problem_text = fields.Text('Problem Description')
    suggestion_text = fields.Text('Suggest Description')
    image_attachments = fields.Many2many('ir.attachment', string='Image Attachment')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)
    service_type = fields.Selection([
        ('by_team', 'By Team'),
        ('by_vendor', 'By Vendor'),
    ], default='by_team', string='Service Type', required=True)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    supplier_id = fields.Many2one('mems.supplier', string='Supplier')
    po_id = fields.Many2one('mems.purchase', string='PO No.')
    date_plan = fields.Date('Plan Date')
    date_finish = fields.Date('Finish Date')
    tax_rate = fields.Float('Tax Rate', default=7)
    tax_type = fields.Selection([
        ('include', 'Include'),
        ('exclude', 'Exclude'),
    ], default='exclude', string='Tax Type')
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
    amount_total = fields.Float('Total', readonly=True, store=True)
    remark = fields.Text('Remark')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
        ('vendor', 'Vendor'),
        ('complete', 'Complete'),
        ('close', 'Close'),
    ], string='Status', group_expand='_expand_groups', default='draft')
    wo_line = fields.One2many('mems.workorder_line', 'wo_id')
    issue_count = fields.Integer('Issue Count', compute='get_count_issue', readonly=True)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('workorder.wo_no') or '-'
        vals['name'] = seq
        return super(WorkOrder, self).create(vals)

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['draft', 'approve', 'vendor', 'complete', 'close']

    @api.onchange('equip_id')
    def get_equipment_detail(self):
        self.equip_brand = self.equip_id.brand_id.name

    @api.onchange('wo_line')
    def get_total_amount(self):
        subtotal = 0
        for r in self:
            for item in r.wo_line:
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

    def do_work_approve(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.workorder.approve.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_wo_id': self.id,
                'default_wo_name': self.name,
            }
        }

    def do_work_complete(self):
        self.write({'state': 'complete'})

    def do_workorder_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.wo.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_wo_id': self.id,
                'default_wo_name': self.name,
            }
        }

    def do_workorder_close(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.wo.close.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_wo_id': self.id,
                'default_wo_name': self.name,
            }
        }

    def do_workorder_revise(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.wo.revise.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_wo_id': self.id,
                'default_wo_name': self.name,
            }
        }

    def do_workorder_print(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.report',
            'report_name': 'mems_repair.workorder_form',
            'model': 'mems.workorder',
            'report_type': 'qweb-pdf',
        }

    def get_count_issue(self):
        if self.id:
            sql = """
                    select
                        coalesce(count(*), 0) as count_issue
                    from mems_issue
                    where wo_id={0} and state not in ('close', 'cancel')
                """.format(self.id)
            self.env.cr.execute(sql)
            res = self.env.cr.dictfetchone()
            self.issue_count = res['count_issue']
            return res['count_issue']
        return 0

    def action_view_workorder(self):
        if self.id:
            sql = """
                    select
                        id as issue_id
                    from mems_issue
                    where wo_id={0} and state not in ('close', 'cancel') limit 1
                """.format(self.id)
            self.env.cr.execute(sql)
            res = self.env.cr.dictfetchone()
            return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mems.issue',
                'target': 'current',
                'res_id': res['issue_id'],
                'type': 'ir.actions.act_window',
            }

    def do_workorder_email(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('mems_repair', 'mail_template_workorder_form')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'mark_so_as_sent': True,
            'default_model': 'mems.workorder',
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


class WorkOrderLine(models.Model):
    _name = 'mems.workorder_line'
    wo_id = fields.Many2one('mems.workorder', ondelete='cascade')
    part_id = fields.Many2one('mems.spare_part', string='Part')
    name = fields.Char('Name')
    description = fields.Text('Description')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    price = fields.Float('Price')
    amount = fields.Float('Amount', readonly=True, store=True)

    @api.onchange('part_id')
    def get_product_change(self):
        if not self.part_id:
            return
        self.name = '[%s] %s' % (self.part_id.code, self.part_id.name)
        self.uom_id = self.part_id.uom_id
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
