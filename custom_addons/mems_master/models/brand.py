from odoo import models, fields, api


class Brand(models.Model):
    _name = 'mems.brand'
    name = fields.Char('Name', required=True)
    name_en = fields.Char('Name English')
