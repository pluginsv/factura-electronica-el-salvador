from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMoveLineReportWizard(models.TransientModel):
    _name = 'account.move.line.report.wizard'
    _description = 'Wizard Reporte Partidas Contables'

    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company,
    )

    partida_type = fields.Selection(
        [
            ('sale', 'Ventas'),
            ('purchase', 'Compras'),
            ('bank', 'Banco'),
            ('cash', 'Efectivo'),
            ('general', 'General'),
            ('diario', 'Por diario'),
            ('all', 'Todos'),
        ],
        string='Tipo de partida',
        required=True,
        default='sale',
    )

    journal_ids = fields.Many2many(
        'account.journal',
        string='Filtrar por diarios',
        domain="[('company_id', '=', company_id)]",
        help="Cuando el tipo sea 'Por diario', debe seleccionar al menos un diario.",
    )

    date_from = fields.Date(
        string='Fecha desde',
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1),
    )
    date_to = fields.Date(
        string='Fecha hasta',
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    report_date = fields.Date(
        string='Fecha de partida',
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help='Fecha usada para el correlativo de la partida.',
    )
    target_move = fields.Selection(
        [
            ('posted', 'Solo publicados'),
            ('all', 'Todos'),
        ],
        string='Asientos',
        required=True,
        default='posted',
    )
    correlativo = fields.Char(
        string='Correlativo',
        readonly=True,
        copy=False,
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for wizard in self:
            if wizard.date_from and wizard.date_to and wizard.date_from > wizard.date_to:
                raise ValidationError(_('La fecha inicial no puede ser mayor que la fecha final.'))

    @api.constrains('partida_type', 'journal_ids')
    def _check_journals_required(self):
        for wizard in self:
            if wizard.partida_type == 'diario' and not wizard.journal_ids:
                raise ValidationError(_('Debe seleccionar al menos un diario cuando el tipo de partida sea "Por diario".'))

    def _get_sequence_info(self):
        """Devuelve el código de secuencia y etiqueta según el filtro del wizard.

        Reglas:
        - Tipos fijos usan su propia secuencia.
        - "Todos" siempre usa la secuencia general.
        - "Por diario" usa la secuencia del tipo del diario si todos los diarios seleccionados
          son del mismo tipo; en cualquier mezcla usa la secuencia general.
        """
        self.ensure_one()

        seq_map = {
            'sale': ('sv.partida.sale', 'PARTIDA DE VENTAS'),
            'purchase': ('sv.partida.purchase', 'PARTIDA DE COMPRAS'),
            'bank': ('sv.partida.bank', 'PARTIDA DE BANCO'),
            'cash': ('sv.partida.cash', 'PARTIDA DE EFECTIVO'),
            'general': ('sv.partida.general', 'PARTIDA DIARIO GENERAL'),
            'situation': ('sv.partida.general', 'PARTIDA DIARIO GENERAL'),
            'all': ('sv.partida.general', 'PARTIDA DIARIO GENERAL'),
        }

        if self.partida_type != 'diario':
            return seq_map.get(self.partida_type, seq_map['general'])

        journal_types = set(self.journal_ids.mapped('type'))
        if len(journal_types) == 1:
            only_type = next(iter(journal_types))
            return seq_map.get(only_type, seq_map['general'])

        return seq_map['general']

    def _build_domain(self):
        self.ensure_one()
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('company_id', '=', self.company_id.id),
        ]

        if self.journal_ids:
            domain.append(('journal_id', 'in', self.journal_ids.ids))
        elif self.partida_type not in ('all', 'diario'):
            if self.partida_type == 'general':
                domain.append(('journal_id.type', 'in', ['general', 'situation']))
            else:
                domain.append(('journal_id.type', '=', self.partida_type))

        if self.target_move == 'posted':
            domain.append(('parent_state', '=', 'posted'))

        return domain

    def _assign_correlativo(self):
        self.ensure_one()
        if self.correlativo:
            return self.correlativo

        seq_code, _tipo_label = self._get_sequence_info()
        correlativo = self.env['ir.sequence'].next_by_code(
            seq_code,
            sequence_date=self.report_date,
        ) or '/'
        self.correlativo = correlativo
        return correlativo

    def action_print_report(self):
        self.ensure_one()
        domain = self._build_domain()
        correlativo = self._assign_correlativo()
        _logger.info(
            'Reporte partidas | wizard=%s | correlativo=%s | domain=%s',
            self.id,
            correlativo,
            domain,
        )

        return self.env.ref(
            'l10n_sv_partidas.action_report_account_move_line'
        ).report_action(
            self,
            data={
                'wizard_id': self.id,
                'domain': domain,
            }
        )
