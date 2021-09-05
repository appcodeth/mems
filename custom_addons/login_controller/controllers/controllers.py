# -*- coding: utf-8 -*-
# Copyright 2021 Artem Shurshilov

from odoo import http
from odoo.http import request
import werkzeug


class Login(http.Controller):
    @http.route('/login', type='http', auth='public')
    def login(self, **kw):
        site = request.params.get('site')
        if site:
            request.session['db'] = site
            return werkzeug.utils.redirect('/web/login')
        return 'Error! Could not redirect to Website %s' % site
