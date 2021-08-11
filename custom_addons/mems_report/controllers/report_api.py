import json
import base64
from datetime import datetime, date
from odoo import http
from odoo.http import request, Response


class ReportApi(http.Controller):

    @http.route('/api/report/saledaily', type='http', auth='public')
    def rpt_sale_daily(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                so.id,
                so.name,
                to_char(so.date_order, 'dd/mm/yyyy'),
                so.tax_rate,
                so.tax_type,
                p.code as product_code,
                p.name as product_name,
                p.cost_price as cost_price,
                sol.price,
                sol.qty,
                sol.amount,
                case
                    when so.tax_type = 'exclude' then
                        sol.amount * so.tax_rate / 100
                    when so.tax_type = 'include' then
                        sol.amount - (sol.amount * 100) / (100 + so.tax_rate)
                    else 0
                end as tax
            from mems_sale so
                left join mems_sale_line sol on so.id=sol.so_id
                left join mems_product p on sol.product_id=p.id
            where
                so.company_id={0} and
                so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
            order by so.date_order asc
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'name': r[1],
                'date_order': r[2],
                'tax_rate': r[3],
                'tax_type': r[4],
                'product_code': r[5],
                'product_name': r[6],
                'cost_price': r[7],
                'price': r[8],
                'qty': r[9],
                'amount': r[10],
                'tax': r[11],
            })

        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/bestseller', type='http', auth='public')
    def rpt_sale_bestseller(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        sql = """
            select
                p.id,
                p.code,
                p.name,
                sum(sl.qty) as sum_qty
            from mems_sale so
                left join mems_sale_line sl on so.id=sl.so_id
                left join mems_product p on sl.product_id=p.id
            where
                so.company_id={0} and
                so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
            group by p.id, p.code, p.name
            order by sum_qty desc limit 30
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'code': r[1],
                'name': r[2],
                'sum_qty': r[3],
            })

        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/purchase', type='http', auth='public')
    def rpt_purchase_daily(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date') + ' 00:00:00'
        end_date = request.params.get('end_date') + ' 23:59:59'
        sql = """
            select
                po.id,
                po.name,
                to_char(po.date_order, 'dd/mm/yyyy'),
                po.tax_rate,
                po.tax_type,
                p.code as product_code,
                p.name as product_name,
                p.cost_price as cost_price,
                pol.price,
                pol.qty,
                pol.amount,
                case
                    when po.tax_type = 'exclude' then
                    pol.amount * po.tax_rate / 100
                    when po.tax_type = 'include' then
                    pol.amount - (pol.amount * 100) / (100 + po.tax_rate)
                    else 0
                end as tax
            from mems_purchase po
                left join mems_purchase_line pol on po.id=pol.po_id
                left join mems_product p on pol.product_id=p.id
            where
                po.company_id={0} and
                po.state in ('invoice', 'paid') and po.date_order between '{1}' and '{2}'
            order by po.date_order asc
            """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'name': r[1],
                'date_order': r[2],
                'tax_rate': r[3],
                'tax_type': r[4],
                'product_code': r[5],
                'product_name': r[6],
                'cost_price': r[7],
                'price': r[8],
                'qty': r[9],
                'amount': r[10],
                'tax': r[11],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/inventory', type='http', auth='public')
    def rpt_inventory(self, **kw):
        company_id = request.params.get('company_id')
        sql = """
            select
                p.id,
                p.code,
                p.name,
                p.cost_price,
                c.name as category_name,
                u.name as uom_name,
                p.stock_qty,
                p.reorder_qty
             from mems_product p
                left join mems_category c on p.category_id=c.id
                left join mems_uom u on p.uom_id=u.id
            where p.company_id={0}
            order by p.category_id, p.code
        """.format(company_id)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'id': r[0],
                'code': r[1],
                'name': r[2],
                'cost_price': r[3],
                'category_name': r[4],
                'uom_name': r[5],
                'stock_qty': r[6],
                'reorder_qty': r[7],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/account/ar', type='http', auth='public')
    def rpt_account_ar(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        sql = """
            select
                so.name,
                cust.code as cust_code,
                cust.name as cust_name,
                to_char(inv.date_order, 'dd/mm/yyyy'),
                to_char(inv.date_payment, 'dd/mm/yyyy'),
                pt.number_of_day as payment_term,
                inv.amount_total,
                inv.state,
                to_char(pay.pay_date, 'dd/mm/yyyy')
            from mems_invoice inv
                left join mems_sale so on inv.so_id=so.id
                left join mems_payment_term pt on inv.payment_term_id=pt.id
                left join mems_payment pay on inv.id=pay.doc_id and pay.doc_type='invoice'
                left join mems_customer cust on inv.customer_id=cust.id
            where inv.state <> 'cancel' and inv.company_id={0} and inv.date_order between '{1}' and '{2}'
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()

        date_format = '%d/%m/%Y'

        rows = []
        for r in results:
            today = datetime.today()
            date_payment = datetime.strptime(r[4], date_format)
            rows.append({
                'name': r[0],
                'cust_code': r[1],
                'cust_name': r[2],
                'date_order': r[3],
                'date_payment': r[4],
                'payment_term': r[5],
                'amount_total': r[6],
                'state': r[7],
                'pay_date': r[8],
                'due_days': (today - date_payment).days,
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/account/ap', type='http', auth='public')
    def rpt_account_ap(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        sql = """
            select
                po.name,
                sup.code as supplier_code,
                sup.name as supplier_name,
                to_char(inv.date_order, 'dd/mm/yyyy'),
                to_char(inv.date_payment, 'dd/mm/yyyy'),
                pt.number_of_day as payment_term,
                inv.amount_total,
                inv.state,
                to_char(pay.pay_date, 'dd/mm/yyyy')
            from mems_sup_invoice inv
                left join mems_purchase po on inv.po_id=po.id
                left join mems_payment_term pt on inv.payment_term_id=pt.id
                left join mems_payment pay on inv.id=pay.doc_id and pay.doc_type='sup_invoice'
                left join mems_supplier sup on inv.supplier_id=sup.id
            where inv.state <> 'cancel' and inv.company_id={0} and inv.date_order between '{1}' and '{2}'
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        date_format = '%d/%m/%Y'
        rows = []
        for r in results:
            today = datetime.today()
            date_payment = datetime.strptime(r[4], date_format)
            rows.append({
                'name': r[0],
                'sup_code': r[1],
                'sup_name': r[2],
                'date_order': r[3],
                'date_payment': r[4],
                'payment_term': r[5],
                'amount_total': r[6],
                'state': r[7],
                'pay_date': r[8],
                'due_days': (today - date_payment).days,
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/account/outtax', type='http', auth='public')
    def rpt_account_output_tax(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        sql = """
            select * from
            (
                select
                    pay.pay_date,
                    so.name,
                    cust.name as cust_name,
                    cust.tax_id as cust_tax,
                    cust.branch as cust_branch,
                    so.amount_total,
                    so.amount_tax,
                    so.company_id
                from mems_sale so
                    left join mems_payment pay on so.id=pay.doc_id and pay.doc_type='sale'
                    left join mems_customer cust on so.customer_id=cust.id
                where so.state = 'paid' and pay.id is not null

                union

                select
                    pay.pay_date,
                    inv.name,
                    cust.name as cust_name,
                    cust.tax_id as cust_tax,
                    cust.branch as cust_branch,
                    inv.amount_total,
                    inv.amount_tax,
                    inv.company_id
                from mems_invoice inv
                    left join mems_payment pay on inv.id=pay.doc_id and pay.doc_type='invoice'
                    left join mems_customer cust on inv.customer_id=cust.id
                where inv.state='paid' and pay.id is not null
            ) as z
            where z.company_id={0} and z.pay_date between '{1}' and '{2}'
            order by z.pay_date asc
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'pay_date': r[0],
                'name': r[1],
                'cust_name': r[2],
                'cust_tax': r[3],
                'cust_branch': r[4],
                'amount_total': r[5],
                'amount_tax': r[6],
                'company_id': r[7],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')

    @http.route('/api/report/account/intax', type='http', auth='public')
    def rpt_account_input_tax(self, **kw):
        company_id = request.params.get('company_id')
        start_date = request.params.get('start_date')
        end_date = request.params.get('end_date')
        sql = """
            select * from
            (
                select
                    pay.pay_date,
                    po.name,
                    sup.name as sup_name,
                    sup.tax_id as sup_tax,
                    sup.branch as sup_branch,
                    po.amount_total,
                    po.amount_tax,
                    po.company_id
                from mems_purchase po
                    left join mems_payment pay on po.id=pay.doc_id and pay.doc_type='sale'
                    left join mems_supplier sup on po.supplier_id=sup.id
                where po.state = 'paid' and pay.id is not null

                union

                select
                    pay.pay_date,
                    inv.name,
                    sup.name as sup_name,
                    sup.tax_id as sup_tax,
                    sup.branch as sup_branch,
                    inv.amount_total,
                    inv.amount_tax,
                    inv.company_id
                from mems_sup_invoice inv
                    left join mems_payment pay on inv.id=pay.doc_id and pay.doc_type='sup_invoice'
                    left join mems_supplier sup on inv.supplier_id=sup.id
                where inv.state='paid' and pay.id is not null
            ) as z
            where z.company_id={0} and z.pay_date between '{1}' and '{2}'
            order by z.pay_date asc
        """.format(company_id, start_date, end_date)
        request.cr.execute(sql)
        results = request.cr.fetchall()
        rows = []
        for r in results:
            rows.append({
                'pay_date': datetime.strptime(r[0], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y'),
                'name': r[1],
                'sup_name': r[2],
                'sup_tax': r[3],
                'sup_branch': r[4],
                'amount_total': r[5],
                'amount_tax': r[6],
                'company_id': r[7],
            })
        return Response(json.dumps({'ok': True, 'rows': rows}), content_type='application/json')
