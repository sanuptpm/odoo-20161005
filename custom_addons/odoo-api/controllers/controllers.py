# -*- coding: utf-8 -*-
from odoo import http

from odoo.http import request
import xmlrpclib

class MyController(http.Controller):

    # http://localhost:8000/login  {"params": {"username":"admin","password":"admin"}}
    @http.route('/login', type='json', methods=['POST'], auth='user', csrf=False)
    def login(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid == 1 :
            msg = "SUCCESS_LOGIN"
        else:
            msg = "LOGIN_FAIL"
        return {"status": 0, "message": msg, "data": []}

    def sign_up():
        pass