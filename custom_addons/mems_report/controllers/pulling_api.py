import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class PullingApi(http.Controller):

    @http.route('/api/pulling/borrow', type='http', auth='public')
    def pulling_borrow(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                br.name,
                br.borrow_date,
                br.expect_date,
                dp.name as dept_name,
                eq.code,
                eq.name as equip_name,
                eq.model_name,
                eq.serial_no,
                bn.name as brand_name,
                u.login,
                1 as qty,
                date_part('day', br.expect_date::timestamp - br.borrow_date::timestamp) as no_day
            from mems_borrow br
                left join mems_equipment eq on br.equip_id=eq.id
                left join mems_department dp on br.department_id=dp.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join res_users u on br.responsible_id=u.id
            where br.state='borrow' and br.borrow_date between '{0}' and '{1}'
            order by br.name asc
            """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'name': r[0],
                'borrow_date': r[1],
                'expect_date': r[2],
                'dept_name': r[3],
                'code': r[4],
                'equip_name': r[5],
                'model_name': r[6],
                'serial_no': r[7],
                'brand_name': r[8],
                'login': r[9],
                'qty': r[10],
                'no_day': r[11],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
