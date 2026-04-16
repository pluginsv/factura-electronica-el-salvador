from collections import defaultdict
from datetime import date
import logging

from odoo import models, api

_logger = logging.getLogger(__name__)


class AccountMoveLineReport(models.AbstractModel):
    """
    Reporte de partidas contables:
    - Cuenta hija con movimiento -> Monto + fila de SubTotal
    - Cuenta padre inmediata -> Parcial
    - Cuenta padre principal -> solo Debe/Haber
    Soporta cuentas de cualquier longitud porque usa la jerarquía real
    existente en account.account y no una longitud fija.
    """
    _name = 'report.partidas_sv_dte.report_move_line_template'
    _description = 'Reporte Partidas Contables SV'

    def _get_existing_parent_accounts(self, grouped_accounts):
        account_codes = [acc.code for acc in grouped_accounts if acc.code]
        candidate_prefixes = set()

        for code in account_codes:
            for size in range(1, len(code)):
                prefix = code[:size]
                if prefix != code:
                    candidate_prefixes.add(prefix)

        if not candidate_prefixes:
            return {}

        parent_accounts = self.env['account.account'].search([
            ('code', 'in', list(candidate_prefixes))
        ], order='code asc')
        return {acc.code: acc for acc in parent_accounts if acc.code and len(acc.code) >= 4}

    def _build_parent_totals(self, lines_source, parent_accounts_by_code):
        parent_totals = defaultdict(lambda: {'debit': 0.0, 'credit': 0.0})
        if not parent_accounts_by_code:
            return parent_totals

        parent_codes = set(parent_accounts_by_code.keys())
        for line in lines_source:
            code = line.account_id.code or ''
            for size in range(1, len(code)):
                prefix = code[:size]
                if prefix in parent_codes:
                    parent_totals[prefix]['debit'] += line.debit
                    parent_totals[prefix]['credit'] += line.credit
        return parent_totals

    def _get_parent_chain(self, code, parent_accounts_by_code):
        chain = []
        if not code:
            return chain

        for size in range(1, len(code)):
            prefix = code[:size]
            if prefix in parent_accounts_by_code:
                chain.append(prefix)
        return chain

    def _get_parent_level(self, parent_code, parent_accounts_by_code):
        return len(self._get_parent_chain(parent_code, parent_accounts_by_code))

    @staticmethod
    def _pick_side_amount(debit, credit):
        return debit if debit > 0 else credit

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        wizard_id = data.get('wizard_id')
        domain = data.get('domain', [])

        wizard = (
            self.env['account.move.line.report.wizard'].browse(wizard_id)
            if wizard_id
            else self.env['account.move.line.report.wizard']
        )

        lines_source = self.env['account.move.line'].search(
            domain,
            order='account_id asc, date asc, move_id asc, id asc'
        )

        date_from = wizard.date_from if wizard else False
        date_to = wizard.date_to if wizard else False

        grouped_accounts = defaultdict(list)
        for line in lines_source:
            grouped_accounts[line.account_id].append(line)

        parent_accounts_by_code = self._get_existing_parent_accounts(grouped_accounts)
        parent_totals = self._build_parent_totals(lines_source, parent_accounts_by_code)

        rows = []
        emitted_main_parents = set()
        emitted_partial_parents = set()

        sorted_accounts = sorted(grouped_accounts.keys(), key=lambda a: a.code or '')

        for account in sorted_accounts:
            code = account.code or ''
            acc_lines = grouped_accounts[account]
            subtotal_debit = sum(l.debit for l in acc_lines)
            subtotal_credit = sum(l.credit for l in acc_lines)
            subtotal_cuenta = self._pick_side_amount(subtotal_debit, subtotal_credit)

            chain = self._get_parent_chain(code, parent_accounts_by_code)
            main_parent_code = chain[0] if chain else None
            immediate_parent_code = chain[-1] if chain else None

            if main_parent_code and main_parent_code not in emitted_main_parents:
                parent_account = parent_accounts_by_code[main_parent_code]
                totals = parent_totals[main_parent_code]
                rows.append({
                    'type': 'parent_main',
                    'code': main_parent_code,
                    'name': parent_account.name or '—',
                    'total_debit': totals['debit'],
                    'total_credit': totals['credit'],
                    'level': self._get_parent_level(main_parent_code, parent_accounts_by_code),
                })
                emitted_main_parents.add(main_parent_code)

            if (
                immediate_parent_code
                and immediate_parent_code != main_parent_code
                and immediate_parent_code not in emitted_partial_parents
            ):
                parent_account = parent_accounts_by_code[immediate_parent_code]
                totals = parent_totals[immediate_parent_code]
                rows.append({
                    'type': 'parent_partial',
                    'code': immediate_parent_code,
                    'name': parent_account.name or '—',
                    'partial_amount': self._pick_side_amount(totals['debit'], totals['credit']),
                    'total_debit': totals['debit'],
                    'total_credit': totals['credit'],
                    'level': self._get_parent_level(immediate_parent_code, parent_accounts_by_code),
                })
                emitted_partial_parents.add(immediate_parent_code)

            rows.append({
                'type': 'account_total',
                'account_code': code,
                'account_name': account.name or '',
                'subtotal_debit': subtotal_debit,
                'subtotal_credit': subtotal_credit,
                'subtotal_cuenta': subtotal_cuenta,
            })

            total = len(acc_lines)
            for idx, line in enumerate(acc_lines):
                rows.append({
                    'type': 'detail',
                    'account_code': code,
                    'account_name': account.name or '',
                    'is_first': idx == 0,
                    'is_last': idx == (total - 1),
                    'debit': line.debit,
                    'credit': line.credit,
                    'date': str(line.date),
                    'journal_code': line.journal_id.code or '',
                    'sello_recepcion': getattr(line.move_id, 'hacienda_selloRecibido', '') or '',
                    'ref': line.move_id.ref or '',
                    'partner': line.partner_id.name if line.partner_id else '',
                    'label': line.name or '',
                    'amount': line.debit if line.debit else line.credit,
                })

        total_debit = sum(l.debit for l in lines_source)
        total_credit = sum(l.credit for l in lines_source)
        rows.append({
            'type': 'grand_total',
            'total_debit': total_debit,
            'total_credit': total_credit,
        })

        seq_code = 'sv.partida.general'
        tipo_label = 'PARTIDA DIARIO GENERAL'
        correlativo = ''
        company = self.env.company
        report_date = date.today().strftime('%d/%m/%Y')

        if wizard:
            seq_code, tipo_label = wizard._get_sequence_info()
            correlativo = wizard.correlativo or ''
            company = wizard.company_id or self.env.company
            report_date = (wizard.report_date or date.today()).strftime('%d/%m/%Y')

        _logger.info(
            'Render reporte partidas | wizard=%s | seq=%s | correlativo=%s | rows=%s | parents=%s | label=%s',
            wizard.id if wizard else False,
            seq_code,
            correlativo,
            len(rows),
            len(parent_accounts_by_code),
            tipo_label
        )

        return {
            'doc_ids': [wizard.id] if wizard_id else [],
            'doc_model': 'account.move.line.report.wizard',
            'docs': [wizard] if wizard_id else [None],
            'rows': rows,
            'date_from': date_from,
            'date_to': date_to,
            'date_report': report_date,
            'correlativo': correlativo,
            'tipo_label': tipo_label,
            'company': company,
        }
