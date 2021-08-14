import json
import werkzeug
from odoo import http
from odoo.http import request, Response


class MenuApi(http.Controller):
    @http.route('/api/getmenu', type='http', auth='public')
    def get_menu(self, **kw):
        model_id = request.params.get('model_id')
        menu_name = request.params.get('menu_name')

        sql = """
            select id,name,type from ir_act_window where name='{0}' and res_model='{1}'
        """.format(menu_name, model_id)
        request.cr.execute(sql)
        actions = request.cr.fetchone()

        sql = """
            select * from ir_ui_menu where action='{0}'
        """.format(actions[2] + ',' + str(actions[0]))
        request.cr.execute(sql)
        menus = request.cr.fetchone()
        return Response(json.dumps({'ok': True, 'menu_id': menus[0], 'action_id': actions[0]}), content_type='application/json')
