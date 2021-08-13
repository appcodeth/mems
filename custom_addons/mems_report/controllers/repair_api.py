import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class RepairApi(http.Controller):

    @http.route('/api/repair/workorder', type='http', auth='public')
    def repair_workorder(self, **kw):
        sql = """
            select
                wo.name,
                wo.problem_text,
                wo.date_order,
                wo.date_finish,
                wo.equip_code as eq_code,
                eq.name as eq_name,
                wo.equip_brand as eq_brand,
                wo.equip_model as eq_model,
                eq.serial_no as eq_sn,
                wo.service_type,
                sp.name as sup_name,
                wo.amount_total,
                case when wo.state = 'approve' then 1 end as total_approve,
                case when wo.state = 'complete' then 1 end as total_complete,
                case when wo.state = 'close' then 1 end as total_close,
                wo.state,
                us.login
            from mems_workorder wo
                left join mems_department dp on wo.department_id=dp.id
                left join mems_equipment eq on wo.equip_id=eq.id
                left join mems_supplier sp on wo.supplier_id=sp.id
                left join res_users us on wo.responsible_id=us.id
            where wo.state <> 'draft'
            order by wo.name asc
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'name': r[0],
                'problem_text': r[1],
                'date_order': r[2],
                'date_finish': r[3],
                'eq_code': r[4],
                'eq_name': r[5],
                'eq_brand': r[6],
                'eq_model': r[7],
                'eq_sn': r[8],
                'service_type': r[9],
                'sup_name': r[10],
                'amount_total': r[11],
                'approved': r[12],
                'completed': r[13],
                'closed': r[14],
                'state': r[15],
                'login': r[16],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
