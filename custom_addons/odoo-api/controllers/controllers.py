# -*- coding: utf-8 -*-
from odoo import http

from odoo.http import request
import xmlrpclib

class MyController(http.Controller):
    @http.route('/hello/world/', type="http", auth='public')
    # @http.route('/hello/world/', auth='user')
    def index(self, **kw):
        myobj = request.env['res.partner'].search([])
        for x in myobj:
            print "======res.partner==name=====", x.name
        return "ok"
    
