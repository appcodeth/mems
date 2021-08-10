from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Equipment(models.Model):
    _name = 'mems.equipment'
    _rec_name = 'name'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, unique=True)
    barcode = fields.Char('Barcode', unique=True)
    unit_price = fields.Float(string='Unit Price')
    image = fields.Binary('Image', attatchment=True)
    category_id = fields.Many2one('mems.category', string='Category')
    uom_id = fields.Many2one('mems.uom', string='Unit of Measure')
    department_id = fields.Many2one('mems.department', string='Department')
    brand_id = fields.Many2one('mems.brand', string='Brand')
    model_name = fields.Char('Model Name')
    serial_no = fields.Char('Serial No')
    warranty_type = fields.Selection([
        ('no', 'No Warranty'),
        ('on-warranty', 'On Warranty'),
        ('out-warranty', 'Out of Warranty'),
    ], default='', string='Warranty Type')
    warranty_start_date = fields.Date('Warranty Start Date')
    warranty_end_date = fields.Date('Warranty End Date')
    supplier_id = fields.Many2one('mems.supplier', string='Supplier')
    receive_date = fields.Date('Receive Date')
    receive_by = fields.Many2one('mems.receive_type', string='Receive By')
    receive_doc_name = fields.Char('Receive Doc Name')
    stock_qty = fields.Integer('Stock Qty')
    min_qty = fields.Integer('Min Qty')
    max_qty = fields.Integer('Max Qty')
    stock_location = fields.Many2one('mems.stock_location', string='Stock Location')
    description = fields.Text('Description')
    spec_attachments = fields.Many2many('ir.attachment', string='File Attachments')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([
        ('active', 'Active'),
        ('borrow', 'Borrow'),
        ('pm', 'PM'),
        ('calibrate', 'Calibrate'),
        ('repair', 'Repair'),
        ('inactive', 'In Active'),
    ], default='active', string='State')
    note = fields.Char('Note')
    pm_line = fields.One2many('mems.pm', 'equip_id', domain=[('state', '!=', 'draft')])
    calibrate_line = fields.One2many('mems.calibration', 'equip_id', domain=[('state', '!=', 'draft')])
    equipment_line = fields.One2many('mems.equipment_line', 'equip_id')

    _sql_constraints = [
        ('field_code', 'unique (code,company_id)', _('Equipment code is existed')),
        ('field_barcode', 'unique (barcode,company_id)', _('Equipment barcode is existed')),
    ]

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = '[{0}] {1}'.format(record.code, record.name)
            result.append((record.id, name))
        return result

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default.update({
            'code': '',
            'barcode': '',
            'state': 'active',
        })
        return super(Equipment, self).copy(default=default)

    def do_equipment_adjust(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.equipment.adjust.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_equip_id': self.id,
                'default_equip_name': self.name,
                'default_equip_qty': 1,
            }
        }

    def do_equipment_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.equipment.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_equip_id': self.id,
                'default_equip_name': '[%s] %s' % (self.code, self.name),
            }
        }


class EquipmentLine(models.Model):
    _name = 'mems.equipment_line'
    equip_id = fields.Many2one('mems.equipment', ondelete='cascade')
    part_id = fields.Many2one('mems.spare_part', string='Part')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    price = fields.Float('Price')
    amount = fields.Float('Amount', readonly=True, store=True)

    @api.onchange('part_id')
    def get_part_change(self):
        if not self.part_id:
            return
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


class EquipmentReason(models.Model):
    _name = 'mems.equipment_reason'
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
