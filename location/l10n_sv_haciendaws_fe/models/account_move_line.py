import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.common_utils.utils import config_utils
    _logger.info("SIT Modulo config_utils [hacienda -account_move_line]")
except ImportError as e:
    _logger.error(f"Error al importar 'config_utils': {e}")
    config_utils = None

class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']

    allowed_invoice_tax_ids = fields.Many2many(
        'account.tax',
        string='Impuestos permitidos (diario)',
        compute='_compute_invoice_allowed_tax_ids',
        store=False,
    )

    @api.depends('move_id.journal_id', 'move_id.journal_id.sit_tax_ids')
    def _compute_invoice_allowed_tax_ids(self):
        for line in self:
            _logger.info("=== [SOL COMPUTE ALLOWED TAX IDS] line=%s ===", line.id)

            company = line.move_id.company_id if line.move_id else None
            move = line.move_id
            move_type = move.move_type if move else False
            journal = line.move_id.journal_id if line.move_id and line.move_id.journal_id else None
            tax_ids_journal = True if journal and journal.sit_tax_ids else False
            _logger.info("[SOL] Journal=%s | Impuesto del diario= %s", journal.id if journal else None, tax_ids_journal)

            is_purchase = move_type in ('in_invoice', 'in_refund')

            # ----------------------------------------------------------------------
            # 0) Compras → comportamiento estándar de Odoo (NO restringir impuestos)
            # ----------------------------------------------------------------------
            if is_purchase:
                _logger.info("[SOL] Compra detectada → usar comportamiento estándar de Odoo")

                if not company:
                    line.allowed_invoice_tax_ids = False
                    continue

                all_taxes_purchase = self.env['account.tax'].search([
                    ('company_id', '=', company.id),
                    ('type_tax_use', 'in', ['purchase', 'none']),
                    ('active', '=', True),
                ])
                line.allowed_invoice_tax_ids = all_taxes_purchase
                continue

            # ----------------------------------------------------------------------
            # 1) Empresa NO usa facturación → usar impuestos estándar de Odoo
            # ----------------------------------------------------------------------
            if not company or not company.sit_facturacion or (company and company.sit_facturacion and company.sit_entorno_test) or not tax_ids_journal:
                _logger.info("[SOL] Empresa NO usa facturación → usar comportamiento estándar de impuestos")
                # ✔️ Comportamiento estándar: permitir TODOS los impuestos
                if not company:
                    line.allowed_invoice_tax_ids = False
                    continue

                all_taxes = self.env['account.tax'].search([
                    ('company_id', '=', company.id),
                    ('type_tax_use', 'in', ['sale', 'none']),
                    ('active', '=', True)
                ])
                _logger.info("[SOL] Impuestos disponibles (estándar): %s", all_taxes.ids)

                line.allowed_invoice_tax_ids = all_taxes
                continue

            # ----------------------------------------------------------------------
            # 2) Empresa con facturación → usar impuestos definidos en el diario
            # ----------------------------------------------------------------------
            if journal and journal.sit_tax_ids:
                _logger.info("[SOL] Impuestos permitidos por diario: %s", journal.sit_tax_ids.ids)
                line.allowed_invoice_tax_ids = journal.sit_tax_ids
            else:
                _logger.info("[SOL] Diario sin impuestos configurados → sin taxes permitidos")
                line.allowed_invoice_tax_ids = False
