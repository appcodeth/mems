import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class StaffApi(http.Controller):
    @http.route('/api/staff/performance', type='http', auth='public')
    def staff_performance(self, **kw):
        sql = """
            select
                us.id,
                pt.name,
                pt.email,
                (select count(*) from mems_workorder w1 where w1.responsible_id=us.id) as total_work,
                (select count(*) from mems_workorder w1 where w1.responsible_id=us.id and w1.state='complete') as total_complete,
                (select count(*) from mems_workorder w1 where w1.responsible_id=us.id and w1.state='close') as total_close
            from mems_workorder wo
                left join res_users us on wo.responsible_id=us.id
                left join res_partner pt on us.partner_id=pt.id
            where wo.responsible_id is not null
            group by us.id, pt.name, pt.email
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'name': r[1],
                'email': r[2],
                'total_work': r[3],
                'total_complete': r[4],
                'total_close': r[5],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
