import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class EquipmentApi(http.Controller):

    @http.route('/api/equipment/all', type='http', auth='public')
    def equipment_all(self, **kw):
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
