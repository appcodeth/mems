from odoo import models, fields, api


class UomCategory(models.Model):
    _name = 'mems.uom_category'
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
