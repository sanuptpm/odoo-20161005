# -*- coding: utf-8 -*-
from odoo import http

# class Academy(http.Controller):
#     @http.route('/academy/academy/', auth='public')
#     def index(self, **kw):
#         return http.request.render('academy.index', {
#             'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
#         })

class Academy(http.Controller):
    @http.route('/academy/academy/', auth='public', website=True)
    def index(self, **kw):
        Teachers = http.request.env['academy.teachers']
        return http.request.render('academy.index', {
            'teachers': Teachers.search([])
        })

