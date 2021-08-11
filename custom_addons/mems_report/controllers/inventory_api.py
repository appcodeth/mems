import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class InventoryApi(http.Controller):

    @http.route('/api/inventory/balance', type='http', auth='public')
    def inventory_balance(self, **kw):
        sql = """
            select
                sp.code,
                sp.name,
                cte.name as categ_name,
                uom.name as uom_name,
                bnd.name as brand_name,
                loc.name as loc_name,
                sp.stock_qty,
                sp.cost_price,
                sp.stock_qty * sp.cost_price as total_cost
            from mems_spare_part sp
                left join mems_category cte on sp.category_id=cte.id
                left join mems_uom uom on sp.uom_id=uom.id
                left join mems_brand bnd on sp.brand_id=bnd.id
                left join mems_stock_location loc on sp.location_id=loc.id
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
                'loc_name': r[5],
                'stock_qty': r[6],
                'cost_price': r[7],
                'total_cost': r[8],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/inventory/move', type='http', auth='public')
    def inventory_move(self, **kw):
        sql = """
            select
                to_char(mv.move_date, 'DD-MM-YYYY HH:MI') as move_date,
                mv.product_code as code,
                mv.name,
                uom.name as uom_name,
                mv.doc_id,
                mv.doc_name,
                mv.doc_type,
                case
                    when mv.doc_type='init' then 'กำหนดค่าเริ่มต้น'
                    when mv.doc_type='adjust' then 'ปรับยอด'
                    when mv.doc_type='receive' then 'รับเข้า'
                    when mv.doc_type='issue' then 'เบิกออก' end as doc_type_desc,
                case when mv.move_type='in' then mv.qty else 0 end as int_qty,
                case when mv.move_type='out' then mv.qty else 0 end as out_qty,
                case when mv.move_type='adjust' then mv.qty else 0 end as adjust_qty,
                (select stock_qty from mems_spare_part sp where sp.code=mv.product_code) as stock_qty
            from mems_stock_move mv
                left join mems_uom uom on mv.uom_id=uom.id
            order by product_code, move_date asc
        """
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'move_date': r[0],
                'code': r[1],
                'name': r[2],
                'uom_name': r[3],
                'doc_id': r[4],
                'doc_name': r[5],
                'doc_type': r[6],
                'doc_type_desc': r[7],
                'int_qty': r[8],
                'out_qty': r[9],
                'adjust_qty': r[10],
                'stock_qty': r[11],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
