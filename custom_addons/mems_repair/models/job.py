from odoo import models, fields, api


class Job(models.Model):
    _name = 'mems.job'
    name = fields.Char('Name', required=True)
