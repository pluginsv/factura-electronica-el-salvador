# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    dui = fields.Char(string="D.U.I.")

    @api.constrains('dui')
    def _check_dui_format(self):
        pattern = re.compile(r'^\d{8}-\d$')
        for partner in self:
            if partner.dui and not pattern.match(partner.dui):
                raise ValidationError("El formato del DUI debe ser XXXXXXXX-X (8 dígitos, guion, 1 dígito).")

    @api.constrains('vat')
    def _check_vat_format(self):
        pattern = re.compile(r'^\d{4}-\d{6}-\d{3}-\d$')
        for partner in self:
            if partner.vat and not pattern.match(partner.vat):
                raise ValidationError("El formato del NIT debe ser XXXX-XXXXXX-XXX-X (4 dígitos, guion, 6 dígitos, guion, 3 dígitos, guion, 1 dígito).")
