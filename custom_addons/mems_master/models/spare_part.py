from odoo import models, fields, api, _


class SparePart(models.Model):
    _name = 'mems.spare_part'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True, unique=True)
    barcode = fields.Char('Barcode', unique=True)
    lot_no = fields.Char('Lot No')
    image = fields.Binary('Image', attatchment=True)
    category_id = fields.Many2one('mems.category', string='Category')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    purchase_uom_id = fields.Many2one('mems.uom', string='Purchase Uom')
    brand_id = fields.Many2one('mems.brand', string='Brand')
    stock_qty = fields.Float('Stock Qty', default=1, store=True, readonly=True)
    min_qty = fields.Float('Min Qty')
    max_qty = fields.Float('Max Qty')
    unit_price = fields.Float('Unit Price')
    cost_price = fields.Float('Cost Price')
    location_id = fields.Many2one('mems.stock_location', string='Stock Location')
    last_purchase_date = fields.Date('Last Purchase Date', readonly=True)
    description = fields.Text('Description')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    _sql_constraints = [
        ('field_code', 'unique (code,company_id)', _('Product code is existed')),
        ('field_barcode', 'unique (barcode,company_id)', _('Product barcode is existed')),
    ]

    @api.model
    def create(self, vals):
        count = self.env['mems.stock_move'].search_count([('doc_name', '=', vals['code'])])
        if not count:
            data = {
                'name': vals['name'],
                'doc_name': vals['code'],
                'doc_type': 'init',
                'qty': vals['stock_qty'],
                'amount': vals['cost_price'],
                'move_type': 'in',
                'user_id': self.env.user.id,
            }

            if vals.get('id'):
                data['id'] = vals['id']
                data['product_id'] = vals['id']

            if vals.get('uom_id'):
                data['uom_id'] = vals['uom_id']
            self.env['mems.stock_move'].create(data)

        return super(SparePart, self).create(vals)

    def do_spare_part_adjust(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mems.spare_part.adjust.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_doc_id': self.id,
                'default_name': self.name,
                'default_code': self.code,
                'default_uom_id': self.uom_id.id if self.uom_id else 0,
                'default_amount': self.cost_price,
                'default_stock_qty': self.stock_qty,
                'default_new_qty': self.stock_qty,
            }
        }

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '[' + str(record.code) + ']' + ' ' + record.name
            result.append((record.id, name))
        return result
