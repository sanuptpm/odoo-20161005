# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
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

    # http://localhost:8000/sign_up   {"params": {"username":"demo","password":"demo","new_name":"name","new_login":"new3","new_password":"password"}}
    @http.route('/sign_up', type='json', methods=['POST'], auth='user', csrf=False)
    def sign_up(self, **args):
        myurs = request.env['res.users'].search([])
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password

        new_name = args.get('new_name')
        new_login = args.get('new_login')
        new_password = args.get('new_password')

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) # check user in model
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        for x in myurs:
            if x.login == new_login:
                raise ValidationError("User already exists!")
        new_user_id = models.execute_kw(db, uid, password, 'res.users', 'create', [{'name':new_name, 'login':new_login, 'new_password':new_password}])
        
        return {"status": 0, "message": new_user_id, "data": []}
