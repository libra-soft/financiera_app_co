# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraApp(http.Controller):
#     @http.route('/financiera_app/financiera_app/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_app/financiera_app/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_app.listing', {
#             'root': '/financiera_app/financiera_app',
#             'objects': http.request.env['financiera_app.financiera_app'].search([]),
#         })

#     @http.route('/financiera_app/financiera_app/objects/<model("financiera_app.financiera_app"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_app.object', {
#             'object': obj
#         })