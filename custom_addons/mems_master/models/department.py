from odoo import models, fields, api


class Department(models.Model):
    _name = 'mems.department'
    name = fields.Char('Name', required=True)
    name_en = fields.Char('Name English')
    address = fields.Text('Address')
    phone = fields.Char('Phone')
    fax = fields.Char('Fax')
    email = fields.Char('Email')
    contact = fields.Char('Contact')
