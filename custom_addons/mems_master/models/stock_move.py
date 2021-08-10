from odoo import models, fields, api
from datetime import datetime


class StockMove(models.Model):
    _name = 'mems.stock_move'
    name = fields.Char('Name', required=True)
    doc_id = fields.Integer('Doc ID')
    doc_name = fields.Char('Doc Name')
    doc_type = fields.Selection([
        ('init', 'Initial'),
        ('receive', 'Receive'),
        ('issue', 'Issue'),
        ('equipment', 'Equipment'),
        ('adjust', 'Adjust'),
    ], string='Doc Type')
    product_id = fields.Integer('Product ID')
    product_code = fields.Char('Product Code')
    user_id = fields.Integer('User ID')
    qty = fields.Float('Qty')
    uom_id = fields.Many2one('mems.uom', string='Uom')
    purchase_qty = fields.Float('Purchase Qty')
    purchase_uom_id = fields.Many2one('mems.uom', string='Purchase Uom')
    amount = fields.Float('Amount')
    move_type = fields.Selection([
        ('in', 'In'),
        ('out', 'Out'),
        ('adjust', 'Adjust'),
    ], string='Move Type')
    move_date = fields.Datetime('Move Date', default=datetime.now())
