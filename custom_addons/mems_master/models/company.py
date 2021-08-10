from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'
    fax = fields.Char('Fax')
    sig_image = fields.Binary('Signature', attachment=True)
    rub_image = fields.Binary('Rubber', attachment=True)
