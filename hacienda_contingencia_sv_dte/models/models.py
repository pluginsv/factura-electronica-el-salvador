# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hacienda_contingencia_sv_dte(models.Model):
#     _name = 'hacienda_contingencia_sv_dte.hacienda_contingencia_sv_dte'
#     _description = 'hacienda_contingencia_sv_dte.hacienda_contingencia_sv_dte'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
