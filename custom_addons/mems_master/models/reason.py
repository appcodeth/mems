from odoo import models, fields, api


class IssueReason(models.Model):
    _name = 'mems.issue_reason'
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
