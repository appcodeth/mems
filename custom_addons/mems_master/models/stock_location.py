from odoo import models, fields, api


class StockLocation(models.Model):
    _name = 'mems.stock_location'
    name = fields.Char('Name', required=True)
    shelf_no = fields.Char('Shelf Name')
    description = fields.Text('Description')
