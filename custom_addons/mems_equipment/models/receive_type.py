from odoo import models, fields, api


class ReceiveType(models.Model):
    _name = 'mems.receive_type'
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
