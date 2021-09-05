# -*- coding: utf-8 -*-
# Copyright 2021 Artem Shurshilov

from odoo import http
from odoo.http import request
import werkzeug


class Login(http.Controller):
    # @http.route('/login', type='http', auth='public')
    # def login(self, **kw):
    #     site = request.params.get('site')
    #     if site and site in http.db_list():
    #         request.session['db'] = site
    #         return werkzeug.utils.redirect('/web/login')
    #     return 'Error! Could not redirect to Website %s' % site
    #
    @http.route('/tranghos', type='http', auth="none", sitemap=False)
    def tranghos(self, redirect=None, **kw):
        request.session['db'] = 'tranghos'
        return werkzeug.utils.redirect('/web/login')

    @http.route('/kingnaraihos', type='http', auth="none", sitemap=False)
    def kingnaraihos(self, redirect=None, **kw):
        request.session['db'] = 'kingnaraihos'
        return werkzeug.utils.redirect('/web/login')
