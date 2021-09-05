# -*- coding: utf-8 -*-
# Copyright 2021 Artem Shurshilov

from odoo import http
from odoo.http import request
import werkzeug
from werkzeug import url_encode
from odoo import _, SUPERUSER_ID
from odoo.tools import config


class Login(http.Controller):
    # @http.route('/login', type='http', auth='public')
    # def login(self, **kw):
    #     site = request.params.get('site')
    #     if site and site in http.db_list():
    #         request.session['db'] = site
    #         return werkzeug.utils.redirect('/web/login')
    #     return 'Error! Could not redirect to Website %s' % site

    @http.route('/tranghos', type='http', auth='public')
    def tranghos(self, **kw):
        request.session['db'] = 'tranghos'
        return werkzeug.utils.redirect('/web/login')

    @http.route('/kingnaraihos', type='http', auth='public')
    def kingnaraihos(self, **kw):
        request.session['db'] = 'kingnaraihos'
        return werkzeug.utils.redirect('/web/login')
