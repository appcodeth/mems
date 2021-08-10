from odoo import models, fields, api


class Bank(models.Model):
    _name = 'mems.bank'
    _rec_name = 'name'
    name = fields.Char('Name', required=True)
    short_name = fields.Char('Short Name')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '[' + str(record.short_name) + ']' + ' ' + record.name
            result.append((record.id, name))
        return result


class BankAccount(models.Model):
    _name = 'mems.bank_account'
    _rec_name = 'account_name'
    account_name = fields.Char('Account Name', required=True)
    account_no = fields.Char('Account No')
    bank_id = fields.Many2one('mems.bank', string='Bank Name')
    bank_branch = fields.Char('Bank Branch')
    bank_type = fields.Selection([('saving', 'Saving'), ('current', 'Current')], string='Bank Type')
