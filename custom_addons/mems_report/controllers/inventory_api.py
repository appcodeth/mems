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
