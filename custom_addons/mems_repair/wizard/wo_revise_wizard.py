import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class WorkOrderReviseWizard(models.TransientModel):
    _name = 'mems.wo.revise.wizard'
    wo_id = fields.Integer('WorkOrder ID')
    wo_name = fields.Char('WorkOrder Name')

    def do_confirm_revise(self):
        sql = """
                select
                    id as issue_id
                from mems_issue
                where wo_id={0} limit 1
            """.format(self.wo_id)
        self.env.cr.execute(sql)
        res = self.env.cr.dictfetchone()

        # have found issue recently
        if res:
            issue_id = res['issue_id']
            _logger.debug('issue_id={0}'.format(issue_id))

            issue = self.env['mems.issue'].browse([issue_id])
            sql = """
                select
                    coalesce(count(*), 0) as count_issue
                from mems_stock_move
                where doc_id={0} and doc_name='{1}' and doc_type='issue'
            """.format(issue_id, issue.name)
            self.env.cr.execute(sql)
            res = self.env.cr.dictfetchone()
            count_issue = res['count_issue']
            _logger.debug('count_issue={0}'.format(count_issue))
            if count_issue > 0:
                pass
            else:
                issue.sudo().write({'state': 'cancel'})
                _logger.info('** Cancel issue **')

        wo = self.env['mems.workorder'].browse([self.wo_id])
        wo.sudo().write({'state': 'draft'})
        self.env['mems.equipment'].browse([wo.equip_id.id]).sudo().write({'state': 'active'})
