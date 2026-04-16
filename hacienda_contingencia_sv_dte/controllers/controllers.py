# -*- coding: utf-8 -*-
# from odoo import http


# class L10nSvHaciendaContingencia(http.Controller):
#     @http.route('/hacienda_contingencia_sv_dte/hacienda_contingencia_sv_dte', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hacienda_contingencia_sv_dte/hacienda_contingencia_sv_dte/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hacienda_contingencia_sv_dte.listing', {
#             'root': '/hacienda_contingencia_sv_dte/hacienda_contingencia_sv_dte',
#             'objects': http.request.env['hacienda_contingencia_sv_dte.hacienda_contingencia_sv_dte'].search([]),
#         })

#     @http.route('/hacienda_contingencia_sv_dte/hacienda_contingencia_sv_dte/objects/<model("hacienda_contingencia_sv_dte.hacienda_contingencia_sv_dte"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hacienda_contingencia_sv_dte.object', {
#             'object': obj
#         })
