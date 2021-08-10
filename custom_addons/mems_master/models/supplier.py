from odoo import models, fields, api


class Supplier(models.Model):
    _name = 'mems.supplier'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code')
    address = fields.Text('Address')
    tax_id = fields.Char('Tax ID')
    branch = fields.Char('Branch')
    phone = fields.Char('Phone')
    fax = fields.Char('Fax')
    email = fields.Char('Email')
    website = fields.Char('Website')
    image = fields.Binary('Image', attachment=True)
    type = fields.Selection([
        ('company', 'Company'),
        ('personal', 'Personal'),
    ], default='company', string='Type')
    contact = fields.Char('Contact Name')
