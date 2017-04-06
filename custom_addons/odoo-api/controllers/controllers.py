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
        uid = common.authenticate(db, username, password, {}) # check user in model
        if uid != False :
            msg = "SUCCESS_LOGIN"
        else:
            msg = "LOGIN_FAIL"
        return {"status": 0, "message": msg, "data": []}

    @http.route('/sign_up', type='json', methods=['POST'], auth='user', csrf=False)
    def sign_up(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) # check user in model
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

        new_user_id = models.execute_kw(db, uid, password, 'res.users', 'create', [{'name':"newuser", 'login':'newuser', 'new_password':'password'}])
