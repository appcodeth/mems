import json
import base64
from datetime import datetime, date, timedelta
from odoo import http
from odoo.http import request, Response


class DashboardApi(http.Controller):

    @http.route('/api/dashboard/all', type='http', auth='public')
    def sale_dashboard(self, **kw):
        company_id = request.params.get('company_id')
        yesterday = date.today() - timedelta(days=1)
        from_date = str(yesterday) + ' 00:00:00'
        to_date = str(yesterday) + ' 23:59:59'

        sql = """
            select
                sum(so.amount_total) as sum_amount
            from mems_sale so
            where so.company_id={0} and so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
        """.format(company_id, from_date, to_date)

        request.cr.execute(sql)
        results = request.cr.fetchone()
        sale_amount_yesterday = results[0] or 1

        from_date = str(date.today()) + ' 00:00:00'
        to_date = str(date.today()) + ' 23:59:59'
        sql = """
            select
                sum(so.amount_total) as sum_amount
            from mems_sale so
            where so.company_id={0} and so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
        """.format(company_id, from_date, to_date)
        request.cr.execute(sql)
        results = request.cr.fetchone()
        sale_amount = results[0] or 0

        sql = """
            select
                count(name) as count_bill
            from mems_sale so
            where so.company_id={0} and so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
        """.format(company_id, from_date, to_date)
        request.cr.execute(sql)
        results = request.cr.fetchone()
        count_bill = results[0] or 0

        grow_rate = ((sale_amount - sale_amount_yesterday) / sale_amount_yesterday) * 100
        return Response(json.dumps({'ok': True, 'sale_amount': sale_amount, 'count_bill': count_bill, 'grow_rate': grow_rate}), content_type='application/json')

    @http.route('/api/dashboard/hours', type='http', auth='public')
    def sale_by_hours(self, **kw):
        company_id = request.params.get('company_id')
        from_date = str(date.today()) + ' 00:00:00'
        to_date = str(date.today()) + ' 23:59:59'
        sql = """
            select
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '0' then so.amount_total end) as h00,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '1' then so.amount_total end) as h01,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '2' then so.amount_total end) as h02,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '3' then so.amount_total end) as h03,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '4' then so.amount_total end) as h04,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '5' then so.amount_total end) as h05,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '6' then so.amount_total end) as h06,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '7' then so.amount_total end) as h07,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '8' then so.amount_total end) as h08,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '9' then so.amount_total end) as h00,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7  = '10' then so.amount_total end) as h10,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '11' then so.amount_total end) as h11,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '12' then so.amount_total end) as h12,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '13' then so.amount_total end) as h13,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '14' then so.amount_total end) as h14,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '15' then so.amount_total end) as h15,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '16' then so.amount_total end) as h16,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '17' then so.amount_total end) as h17,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '18' then so.amount_total end) as h18,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '19' then so.amount_total end) as h19,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '20' then so.amount_total end) as h20,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '21' then so.amount_total end) as h21,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '22' then so.amount_total end) as h22,
                sum(case when cast(to_char(so.date_order, 'hh') as integer) + 7 = '23' then so.amount_total end) as h23
            from mems_sale so
            where so.company_id={0} and so.state in ('invoice', 'paid') and so.date_order between '{1}' and '{2}'
        """.format(company_id, from_date, to_date)
        request.cr.execute(sql)
        results = request.cr.fetchone()
        labels = [
            '00:00',
            '01:00',
            '02:00',
            '03:00',
            '04:00',
            '05:00',
            '06:00',
            '07:00',
            '08:00',
            '09:00',
            '10:00',
            '11:00',
            '12:00',
            '13:00',
            '14:00',
            '15:00',
            '16:00',
            '17:00',
            '18:00',
            '19:00',
            '20:00',
            '21:00',
            '22:00',
            '23:00',
        ]
        data = [r or 0 for r in results]
        return Response(json.dumps({'ok': True, 'labels': labels, 'data': data}), content_type='application/json')

    @http.route('/api/dashboard/category', type='http', auth='public')
    def sale_by_category(self, **kw):
        company_id = request.params.get('company_id')
        from_date = str(date.today()) + ' 00:00:00'
        to_date = str(date.today()) + ' 23:59:59'
        sql = """
            select
                c.name,
                sum(sl.amount) as sale_amount
            from mems_sale so
                left join mems_sale_line sl on so.id=sl.so_id
                left join mems_product p on sl.product_id=p.id
                left join mems_category c on p.category_id=c.id
            where so.state in ('invoice', 'paid') and
                so.company_id={0} and
                so.date_order between '{1}' and '{2}'
            group by c.name
        """.format(company_id, from_date, to_date)
        request.cr.execute(sql)

        results = request.cr.fetchall()
        labels = []
        data = []

        for r in results:
            labels.append(r[0])
            data.append(r[1])
        return Response(json.dumps({'ok': True, 'labels': labels, 'data': data}), content_type='application/json')

    @http.route('/api/dashboard/payment', type='http', auth='public')
    def sale_by_payment(self, **kw):
        company_id = request.params.get('company_id')
        from_date = str(date.today()) + ' 00:00:00'
        to_date = str(date.today()) + ' 23:59:59'
        sql = """
        select
            sum(case when pay_method='cash' then pay_amount else 0 end) as Cash,
            sum(case when pay_method='credit' then pay_amount else 0 end) as Credit,
            sum(case when pay_method='transfer' then pay_amount else 0 end) as BankTransfer,
            sum(case when pay_method='card' then pay_amount else 0 end) as CreditCard,
            sum(pay_amount) as Total
        from mems_payment where doc_type in ('sale', 'invoice') and
            company_id={0} and
            pay_date between '{1}' and '{2}'
        """.format(company_id, from_date, to_date)
        request.cr.execute(sql)

        results = request.cr.fetchone()
        labels = [
            'Cash',
            'Credit',
            'Bank Transfer',
            'Credit Card',
        ]
        data = [results[0] or 0, results[1] or 0, results[2] or 0, results[3] or 0]
        return Response(json.dumps({'ok': True, 'labels': labels, 'data': data}), content_type='application/json')
