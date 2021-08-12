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

    @http.route('/api/pulling/restore', type='http', auth='public')
    def pulling_restore(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                re.name,
                re.restore_date,
                dp.name as dept_name,
                br.name as borrow_name,
                br.borrow_date as borrow_date,
                eq.code,
                eq.name as equip_name,
                eq.model_name,
                eq.serial_no,
                bn.name as brand_name,
                u.login,
                1 as qty,
                date_part('day', br.restore_date::timestamp - br.borrow_date::timestamp) as no_day
            from mems_restore re
                left join mems_borrow br on re.borrow_id=br.id
                left join mems_equipment eq on br.equip_id=eq.id
                left join mems_department dp on br.department_id=dp.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join res_users u on re.responsible_id=u.id
            where re.state='close' and re.restore_date between '{0}' and '{1}'
            order by re.name asc
            """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'name': r[0],
                'restore_date': r[1],
                'dept_name': r[2],
                'borrow_name': r[3],
                'borrow_date': r[4],
                'code': r[5],
                'equip_name': r[6],
                'model_name': r[7],
                'serial_no': r[8],
                'brand_name': r[9],
                'login': r[10],
                'qty': r[11],
                'no_day': r[12],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')


    @http.route('/api/pulling/overdate', type='http', auth='public')
    def pulling_overdate(self, **kw):
        sql = """
            select
                eq.code,
                eq.name,
                eq.model_name,
                eq.serial_no,
                bn.name as brand_name,
                br.name as borrow_name,
                dp.name as dept_name,
                br.borrow_date,
                br.expect_date,
                date_part('day', now()::timestamp - br.expect_date::timestamp) as no_day
            from mems_borrow br
                left join mems_equipment eq on br.equip_id=eq.id
                left join mems_department dp on br.department_id=dp.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join res_users u on br.responsible_id=u.id
            where br.state='borrow' and now() > br.expect_date
            order by br.borrow_date,eq.code asc
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'model_name': r[2],
                'serial_no': r[3],
                'brand_name': r[4],
                'borrow_name': r[5],
                'dept_name': r[6],
                'borrow_date': r[7],
                'expect_date': r[8],
                'no_day': r[9],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
