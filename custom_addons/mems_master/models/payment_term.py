from odoo import models, fields, api


class PaymentTerm(models.Model):
    _name = 'mems.payment_term'
    name = fields.Char('Name', required=True)
    name_en = fields.Char('Name English')
    number_of_day = fields.Integer('No. of Days')
