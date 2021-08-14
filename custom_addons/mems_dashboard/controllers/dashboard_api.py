import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class DashboardApi(http.Controller):

    @http.route('/api/dashboard/count', type='http', auth='public')
    def dashboard_count(self, **kw):
        sql = """
            select
                (select count(*) from mems_equipment where state='active') as count_active,
                (select count(*) from mems_equipment where state='repair') as count_repair,
                (select count(*) from mems_equipment where state='pm' or state='calibrate') as count_pm,
                (select count(*) from mems_equipment where state='borrow') as count_pulling
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'count_active': r[0],
                'count_repair': r[1],
                'count_pm': r[2],
                'count_pulling': r[3],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/dashboard/barchart', type='http', auth='public')
    def dashboard_barchart(self, **kw):
        sql = """
            select
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='01' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon1_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='01' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon1_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='02' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon2_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='02' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon2_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='03' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon3_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='03' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon3_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='04' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon4_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='04' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon4_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='05' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon5_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='05' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon5_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='06' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon6_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='06' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon6_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='07' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon7_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='07' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon7_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='08' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon8_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='08' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon8_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='09' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon9_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='09' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon9_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='10' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon10_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='10' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon10_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='11' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon11_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='11' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon11_02,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='12' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state not in ('draft', 'cancel')) as mon12_01,
                (select count(*) from mems_workorder where to_char(date_order, 'MM')='12' and to_char(date_order,'YYYY')=to_char(now(),'YYYY') and state in ('close')) as mon12_02
                    """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows1 = []
        rows2 = []
        for r in results:
            rows1 = [r[0], r[2], r[4], r[6], r[8], r[10], r[12], r[14], r[16], r[18], r[20], r[22], ]
            rows2 = [r[1], r[3], r[5], r[7], r[9], r[11], r[13], r[15], r[17], r[19], r[21], r[23], ]
        return Response(json.dumps({'ok': True, 'rows1': rows1, 'rows2': rows2}), content_type='application/json')

    @http.route('/api/dashboard/piechart', type='http', auth='public')
    def dashboard_piechart(self, **kw):
        sql = """
            select
                (select count(*) from mems_workorder where service_type='by_team' and state not in ('draft', 'cancel') and to_char(date_order,'YYYY')=to_char(now(),'YYYY')) as count_team,
                (select count(*) from mems_workorder where service_type='by_vendor' and state not in ('draft', 'cancel') and to_char(date_order,'YYYY')=to_char(now(),'YYYY')) as count_vendor
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows = [r[0], r[1]]
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/dashboard/workorder', type='http', auth='public')
    def staff_performance(self, **kw):
        sql = """
            select
                wo.id,
                wo.name,
                wo.date_order,
                'งานซ่อม [' || eq.code || ']' || eq.name as wo_name,
                case
                    when wo.state='approve' then 'รอซ่อม'
                    when wo.state='complete' then 'ซ่อมเสร็จ รอตรวจสอบ' end as state
            from mems_workorder wo
                left join mems_equipment eq on wo.equip_id=eq.id
            where wo.state not in ('draft', 'close', 'cancel') and wo.responsible_id={0}
            order by wo.name asc
        """.format(http.request.env.context.get('uid'))
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'name': r[1],
                'date_order': r[2],
                'wo_name': r[3],
                'state': r[4],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
