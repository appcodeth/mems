from odoo import models, fields, api


class Category(models.Model):
    _name = 'mems.category'
    name = fields.Char('Name', required=True)
    parent_id = fields.Many2one('mems.category', string='Parent')
