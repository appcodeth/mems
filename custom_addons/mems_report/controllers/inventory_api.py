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
            where sp.type='product'
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

    @http.route('/api/inventory/low', type='http', auth='public')
    def inventory_low(self, **kw):
        sql = """
            select
                sp.code,
                sp.name,
                ct.name as categ_name,
                uom.name as uom_name,
                bn.name as brand_name,
                lc.name as loc_name,
                sp.stock_qty
            from mems_spare_part sp
                left join mems_category ct on sp.category_id=ct.id
                left join mems_uom uom on sp.uom_id=uom.id
                left join mems_stock_location lc on sp.location_id=lc.id
                left join mems_brand bn on sp.brand_id=bn.id
            where sp.stock_qty <= sp.min_qty and sp.type='product'
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
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/inventory/topuse', type='http', auth='public')
    def inventory_topuse(self, **kw):
        sql = """
            select
                sp.code,
                sp.name,
                ca.name as categ_name,
                um.name as uom_name,
                bn.name as brand_name,
                lc.name as loc_name,
                sum(ml.qty) as qty
            from mems_issue_line ml
                left join mems_issue mi on ml.issue_id=mi.id
                left join mems_spare_part sp on ml.part_id=sp.id
                left join mems_category ca on sp.category_id=ca.id
                left join mems_uom um on sp.uom_id=um.id
                left join mems_brand bn on sp.brand_id=bn.id
                left join mems_stock_location lc on sp.location_id=lc.id
            where mi.state='complete' and sp.type='product'
            group by sp.code, sp.name, ca.name, um.name, bn.name, lc.name
            order by qty desc limit 20
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
                'qty': r[6],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/inventory/receive', type='http', auth='public')
    def inventory_receive(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                pt.code,
                pt.name,
                mr.name as rcv_name,
                mr.date_rcv as rcv_date,
                po.name as po_name,
                po.date_order as po_date,
                sp.name as sup_name,
                um.name as uom_name,
                ml.qty,
                ml.price,
                ml.amount
            from mems_receive_line ml
                left join mems_receive mr on ml.rcv_id=mr.id
                left join mems_purchase po on mr.po_id=po.id
                left join mems_supplier sp on mr.supplier_id=sp.id
                left join mems_spare_part pt on ml.part_id=pt.id
                left join mems_uom um on ml.uom_id=um.id
            where mr.date_rcv between '{0}' and '{1}' and mr.state='complete' and pt.type='product'
            order by pt.code,rcv_name asc
        """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'rcv_name': r[2],
                'rcv_date': r[3],
                'po_name': r[4],
                'po_date': r[5],
                'sup_name': r[6],
                'uom_name': r[7],
                'qty': r[8],
                'price': r[9],
                'amount': r[10],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')


    @http.route('/api/inventory/issue', type='http', auth='public')
    def inventory_issue(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                pt.code,
                pt.name,
                isu.name as issue_name,
                isu.date_issue as issue_date,
                wo.name as wo_name,
                wo.date_order as wo_date,
                dp.name as dept_name,
                um.name as uom_name,
                isl.qty,
                isl.price,
                isl.amount
            from mems_issue_line isl
                left join mems_issue isu on isl.issue_id=isu.id
                left join mems_workorder wo on isu.wo_id=wo.id
                left join mems_department dp on isu.department_id=dp.id
                left join mems_spare_part pt on isl.part_id=pt.id
                left join mems_uom um on isl.uom_id=um.id
            where isu.date_issue between '{0}' and '{1}' and isu.state='complete' and pt.type='product'
            order by pt.code,issue_name asc
        """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'code': r[0],
                'name': r[1],
                'issue_name': r[2],
                'issue_date': r[3],
                'wo_name': r[4],
                'wo_date': r[5],
                'dept_name': r[6],
                'uom_name': r[7],
                'qty': r[8],
                'price': r[9],
                'amount': r[10],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')


    @http.route('/api/inventory/purchase', type='http', auth='public')
    def inventory_purchase(self, **kw):
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                po.name,
                po.date_order,
                po.date_payment,
                po.ref_rfq,
                sp.name as sup_name,
                po.amount_untaxed,
                po.amount_tax,
                po.amount_discount,
                po.amount_total,
                po.state
            from mems_purchase po
                left join mems_supplier sp on po.supplier_id=sp.id
            where po.state not in ('draft', 'cancel') and po.date_order between '{0}' and '{1}'
            order by po.name asc
        """.format(start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'name': r[0],
                'date_order': r[1],
                'date_payment': r[2],
                'ref_rfq': r[3],
                'sup_name': r[4],
                'amount_untaxed': r[5],
                'amount_tax': r[6],
                'amount_discount': r[7],
                'amount_total': r[8],
                'state': r[9],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
