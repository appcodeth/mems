import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class EquipmentApi(http.Controller):

    @http.route('/api/equipment/status', type='http', auth='public')
    def equipment_status(self, **kw):
        sql = """
            select
                substring(eqp.code, 0, position('/' in eqp.code)) as code,
                eqp.name,
                cate.name as categ_name,
                uom.name as uom_name,
                brn.name as brand_name,
                eqp.model_name,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name) as total_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='active') as active_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='borrow') as borrow_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='pm') as pm_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='calibrate') as calibrate_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='repair') as repair_count,
                (select count(*) from mems_equipment e1 where e1.model_name=eqp.model_name and e1.state='inactive') as inactive_count
            from mems_equipment eqp
                left join mems_category cate on eqp.category_id=cate.id
                left join mems_uom uom on eqp.uom_id=uom.id
                left join mems_brand brn on eqp.brand_id=brn.id
                left join mems_department dep on eqp.department_id=dep.id
            group by substring(eqp.code, 0, position('/' in eqp.code)), eqp.name, cate.name, uom.name, brn.name, eqp.model_name
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'categ_name': r[2],
                'uom_name': r[3],
                'brand_name': r[4],
                'model_name': r[5],
                'total_count': r[6],
                'active_count': r[7],
                'borrow_count': r[8],
                'pm_count': r[9],
                'calibrate_count': r[10],
                'repair_count': r[11],
                'inactive_count': r[12]
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/equipment/calibrate', type='http', auth='public')
    def equipment_calibrate(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                eq.code,
                eq.name,
                ct.name as categ_name,
                um.name as uom_name,
                bn.name as brand_name,
                eq.model_name,
                eq.serial_no,
                ca.name as ca_name,
                ca.start_date,
                ca.end_date,
                sp.name as sup_name,
                us.login
            from mems_calibration ca
                left join mems_equipment eq on ca.equip_id=eq.id
                left join mems_supplier sp on ca.supplier_id=sp.id
                left join mems_category ct on eq.category_id=ct.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join mems_uom um on eq.uom_id=um.id
                left join res_users us on ca.responsible_id=us.id
            where ca.state='approve' and ca.start_date between '{0}' and '{1}'
            order by ca.name,eq.code asc
        """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'categ_name': r[2],
                'uom_name': r[3],
                'brand_name': r[4],
                'model_name': r[5],
                'serial_no': r[6],
                'ca_name': r[7],
                'start_date': r[8],
                'end_date': r[9],
                'sup_name': r[10],
                'login': r[11],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/equipment/pm', type='http', auth='public')
    def equipment_pm(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                eq.code,
                eq.name,
                ct.name as categ_name,
                um.name as uom_name,
                bn.name as brand_name,
                eq.model_name,
                eq.serial_no,
                pm.name as pm_name,
                pm.start_date,
                pm.end_date,
                us.login
            from mems_pm pm
                left join mems_equipment eq on pm.equip_id=eq.id
                left join mems_category ct on eq.category_id=ct.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join mems_uom um on eq.uom_id=um.id
                left join res_users us on pm.responsible_id=us.id
            where pm.state='approve' and pm.start_date between '{0}' and '{1}'
            order by pm.name,eq.code asc
        """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'categ_name': r[2],
                'uom_name': r[3],
                'brand_name': r[4],
                'model_name': r[5],
                'serial_no': r[6],
                'pm_name': r[7],
                'start_date': r[8],
                'end_date': r[9],
                'login': r[10],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/equipment/downtime', type='http', auth='public')
    def equipment_downtime(self, **kw):
        sql = """
            select
                eq.code,
                eq.name,
                ca.name as categ_name,
                um.name as uom_name,
                bn.name as brand_name,
                eq.model_name,
                eq.serial_no,
                case when eq.state = 'pm' then pm.start_date
                    when eq.state = 'calibrate' then cl.start_date
                    when eq.state = 'repair' then wo.date_order
                    when eq.state = 'borrow' then bw.borrow_date end as start_date,
                case when eq.state = 'pm' then pm.end_date
                    when eq.state = 'calibrate' then cl.end_date
                    when eq.state = 'repair' then wo.date_finish
                    when eq.state = 'borrow' then bw.expect_date end as end_date,
                case when eq.state = 'pm' then date_part('day', now()::timestamp - pm.start_date::timestamp)
                    when eq.state = 'calibrate' then date_part('day', now()::timestamp - cl.start_date::timestamp)
                    when eq.state = 'repair' then date_part('day', now()::timestamp - wo.date_order::timestamp)
                    when eq.state = 'borrow' then  date_part('day', now()::timestamp -bw.borrow_date::timestamp) end as no_day,
                case when eq.state='pm' then 'บำรุงรักษา'
                    when eq.state = 'calibrate' then 'สอบเทียบ/วัด'
                    when eq.state = 'repair' then 'ส่งซ่อม'
                    when eq.state = 'borrow' then 'ยืม' end as state
            from mems_equipment eq
                left join mems_category ca on eq.category_id=ca.id
                left join mems_brand bn on eq.brand_id=bn.id
                left join mems_uom um on eq.uom_id=um.id
                left join mems_pm pm on pm.equip_id=eq.id
                left join mems_calibration cl on cl.equip_id=eq.id
                left join mems_borrow bw on bw.equip_id=eq.id
                left join mems_workorder wo on wo.equip_id=eq.id
            where eq.state not in('active', 'cancel')
            order by eq.code asc
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'categ_name': r[2],
                'uom_name': r[3],
                'brand_name': r[4],
                'model_name': r[5],
                'serial_no': r[6],
                'start_date': r[7],
                'end_date': r[8],
                'no_day': r[9],
                'state': r[10],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
