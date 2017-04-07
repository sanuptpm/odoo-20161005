# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request
import werkzeug.contrib.sessions
import xmlrpclib

class MyController(http.Controller):

    # http://localhost:8000/login  {"params": {"username":"admin","password":"admin"}}
    @http.route('/login', type='json', methods=['POST'], auth='user', csrf=False)
    def login(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        # self.sessions = request.csrf_token()
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) # check user in model
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Adding/Updating the token for session
        models.execute_kw(db, uid, password, 'res.users', 'write', [[uid], 
            {'session': request.csrf_token()}])
        if uid != False :
            msg = "SUCCESS_LOGIN"
        else:
            msg = "LOGIN_FAIL"
        return {"status": 0, "message": msg, "data": []}

    # http://localhost:8000/sign_up   {"params": {"username":"demo","password":"demo","new_name":"name","new_login":"new3","new_password":"password","image":"/9j....."}}
    @http.route('/sign_up', type='json', methods=['POST'], auth='user', csrf=False)
    def sign_up(self, **args):
        myurs = request.env['res.users'].search([])
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        img = args.get('image')
        new_name = args.get('new_name')
        new_login = args.get('new_login')
        new_password = args.get('new_password')

        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) # check user in model
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        for x in myurs:
            if x.login == new_login:
                raise ValidationError("User already exists!")
        new_user_id = models.execute_kw(db, uid, password, 'res.users', 'create', [{'name':new_name, 'login':new_login, 'new_password':new_password, 'image':img}])
        
        return {"status": 0, "message": new_user_id, "data": []}

    # http://localhost:8000/res_partner    {"params": {"username":"demo","password":"demo"}}
    @http.route('/res_partner', type='json', methods=['POST'], auth='user', csrf=False)
    def res_partner(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        ids = models.execute_kw(db, uid, password, 'res.partner', 'search_read', 
            [[['is_company', '=', True], ['customer', '=', True]]], 
            {'fields': ['name', 'user_ids', 'email', 'image_small'], 'limit': 5})
        return ids

    @http.route('/image_of_res_user', type='json', methods=['POST'], auth='user', csrf=False)
    def image_of_res_user(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

        partner_ids = models.execute_kw(db, uid, password, 'res.users', 'search_read', 
            [[['id', '=', uid]]], 
            {'fields': ['partner_id'], 'limit': 1})
        # print "====partner_ids====", partner_ids[0]['partner_id'][0]
        ids_partner = models.execute_kw(db, uid, password, 'res.partner', 'search_read', 
            [[['commercial_partner_id', '=', partner_ids[0]['partner_id'][0]]]], 
            {'fields': ['name', 'user_ids', 'email', 'image_medium','commercial_partner_id'], 'limit': 5})
        # print "=====ids_partner======", ids_partner
        ids = models.execute_kw(db, uid, password, 'res.users', 'search_read', 
            [[['partner_id', '=', ids_partner[0]['commercial_partner_id'][0]]]], 
            {'fields': ['image_medium'], 'limit': 5})
        return ids

    @http.route('/partner_list', type='json', methods=['POST'], auth='user', csrf=True)
    def partner_list(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        # print "====self.sessions===", self.sessions
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        users_ids = models.execute_kw(db, uid, password, 'res.users', 'search_read', 
            [[['id', '=', uid]]], 
            {'fields': ['session'], 'limit': 1})
        print "=====session====", users_ids
        if users_ids[0]['session'] == False:
            print "=======Hai==========="
            msg = "Login To Access Data"
        else:
            msg = "SUCCESS"
        # partner_ids = models.execute_kw(db, uid, password, 'res.partner', 
            # 'search', [[['is_company', '=', True], ['customer', '=', True]]])

        return {"status": 0, "message": msg, "data": [users_ids]}
    
    @http.route('/log_out', type='json', methods=['POST'], auth='user', csrf=True)
    def log_out(self, **args):
        url = "http://localhost:8000"
        db = "apidb"
        username = args.get('username') # username
        password = args.get('password') # password
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {}) # check user in model
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Deleting/Updating the token for session
        models.execute_kw(db, uid, password, 'res.users', 'write', [[uid], 
            {'session': 0}])
