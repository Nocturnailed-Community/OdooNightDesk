# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

PRIORITY_SELECTION = [
    ('0', 'Low'),
    ('1', 'Normal'),
    ('2', 'High'),
    ('3', 'Critical'),
]


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, create_date desc'
    _rec_name = 'name'

    # ─── Identification ────────────────────────────────────────────
    name = fields.Char(
        string='Ticket Number',
        required=True,
        readonly=True,
        default=lambda self: _('New'),
        copy=False,
    )
    ticket_title = fields.Char(
        string='Subject',
        required=True,
        tracking=True,
    )
    description = fields.Html(
        string='Description',
    )

    # ─── Classification ────────────────────────────────────────────
    team_id = fields.Many2one(
        'helpdesk.team',
        string='Team',
        required=True,
        tracking=True,
        default=lambda self: self.env['helpdesk.team'].search([], limit=1),
    )
    category_id = fields.Many2one(
        'helpdesk.category',
        string='Category',
        tracking=True,
    )
    stage_id = fields.Many2one(
        'helpdesk.stage',
        string='Stage',
        tracking=True,
        group_expand='_read_group_stage_ids',
        default=lambda self: self._get_default_stage(),
    )
    priority = fields.Selection(
        PRIORITY_SELECTION,
        string='Priority',
        default='1',
        tracking=True,
    )
    kanban_state = fields.Selection([
        ('normal', 'In Progress'),
        ('done', 'Ready for Next Stage'),
        ('blocked', 'Blocked'),
    ], string='Kanban State', default='normal', tracking=True)

    # ─── Assignment ────────────────────────────────────────────────
    user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        tracking=True,
        domain="[('share', '=', False)]",
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        tracking=True,
    )
    partner_name = fields.Char(related='partner_id.name', string='Customer Name')
    partner_email = fields.Char(related='partner_id.email', string='Customer Email')
    partner_phone = fields.Char(related='partner_id.phone', string='Customer Phone')

    # ─── SLA ───────────────────────────────────────────────────────
    sla_id = fields.Many2one('helpdesk.sla', string='SLA Policy')
    deadline = fields.Datetime(
        string='Deadline',
        tracking=True,
    )
    sla_status = fields.Selection([
        ('ok', 'On Track'),
        ('failed', 'Failed'),
        ('reached', 'Reached'),
    ], string='SLA Status', compute='_compute_sla_status', store=True)

    # ─── Dates ─────────────────────────────────────────────────────
    open_date = fields.Datetime(
        string='Opened On',
        default=fields.Datetime.now,
    )
    close_date = fields.Datetime(
        string='Closed On',
        tracking=True,
    )
    last_action_date = fields.Datetime(
        string='Last Action',
        default=fields.Datetime.now,
    )

    # ─── State flags ───────────────────────────────────────────────
    active = fields.Boolean(default=True)
    is_closed = fields.Boolean(
        related='stage_id.is_closed',
        string='Is Closed',
        store=True,
    )

    # ─── Computed ──────────────────────────────────────────────────
    color = fields.Integer(compute='_compute_color')
    ticket_count_by_partner = fields.Integer(
        compute='_compute_ticket_count_by_partner',
        string='Other Tickets',
    )
    hours_open = fields.Float(
        compute='_compute_hours_open',
        string='Time Open (hrs)',
    )

    # ───────────────────────────────────────────────────────────────
    # Default / grouping helpers
    # ───────────────────────────────────────────────────────────────

    def _get_default_stage(self):
        stage = self.env['helpdesk.stage'].search(
            [('sequence', '=', 1)], limit=1
        )
        return stage

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.search([], order=order)

    # ───────────────────────────────────────────────────────────────
    # Computed methods
    # ───────────────────────────────────────────────────────────────

    @api.depends('priority', 'sla_status')
    def _compute_color(self):
        for ticket in self:
            if ticket.sla_status == 'failed':
                ticket.color = 1      # red
            elif ticket.priority == '3':
                ticket.color = 2      # orange
            elif ticket.priority == '2':
                ticket.color = 3      # yellow
            else:
                ticket.color = 0

    @api.depends('partner_id')
    def _compute_ticket_count_by_partner(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.ticket_count_by_partner = self.search_count([
                    ('partner_id', '=', ticket.partner_id.id),
                    ('id', '!=', ticket.id),
                ])
            else:
                ticket.ticket_count_by_partner = 0

    @api.depends('open_date', 'close_date', 'is_closed')
    def _compute_hours_open(self):
        now = fields.Datetime.now()
        for ticket in self:
            end = ticket.close_date if ticket.is_closed and ticket.close_date else now
            if ticket.open_date:
                delta = end - ticket.open_date
                ticket.hours_open = delta.total_seconds() / 3600.0
            else:
                ticket.hours_open = 0.0

    @api.depends('deadline', 'is_closed', 'close_date')
    def _compute_sla_status(self):
        now = fields.Datetime.now()
        for ticket in self:
            if not ticket.deadline:
                ticket.sla_status = 'ok'
            elif ticket.is_closed:
                ticket.sla_status = 'reached' if (
                    ticket.close_date and ticket.close_date <= ticket.deadline
                ) else 'failed'
            elif now > ticket.deadline:
                ticket.sla_status = 'failed'
            else:
                ticket.sla_status = 'ok'

    # ───────────────────────────────────────────────────────────────
    # ORM overrides
    # ───────────────────────────────────────────────────────────────

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'helpdesk.ticket'
                ) or _('New')
        tickets = super().create(vals_list)
        for ticket in tickets:
            ticket._apply_sla()
        return tickets

    def write(self, vals):
        if 'stage_id' in vals:
            stage = self.env['helpdesk.stage'].browse(vals['stage_id'])
            if stage.is_closed:
                vals['close_date'] = fields.Datetime.now()
            else:
                vals['close_date'] = False
        result = super().write(vals)
        if 'sla_id' in vals or 'team_id' in vals or 'priority' in vals:
            self._apply_sla()
        return result

    # ───────────────────────────────────────────────────────────────
    # Business methods
    # ───────────────────────────────────────────────────────────────

    def _apply_sla(self):
        """Compute deadline based on SLA policy."""
        for ticket in self:
            sla = ticket.sla_id or ticket.team_id.sla_id
            if sla and ticket.open_date:
                hours = sla._get_response_hours(ticket.priority)
                ticket.deadline = ticket.open_date + timedelta(hours=hours)
                ticket.sla_id = sla

    def action_assign_to_me(self):
        self.write({'user_id': self.env.uid})

    def action_mark_done(self):
        done_stage = self.env['helpdesk.stage'].search(
            [('is_closed', '=', True)], limit=1
        )
        if not done_stage:
            raise UserError(_('No closed stage found. Please configure a closed stage first.'))
        self.write({'stage_id': done_stage.id})

    def action_reopen(self):
        open_stage = self.env['helpdesk.stage'].search(
            [('is_closed', '=', False)], order='sequence', limit=1
        )
        self.write({
            'stage_id': open_stage.id,
            'close_date': False,
        })

    def action_escalate(self):
        return {
            'name': _('Escalate Ticket'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket.escalate',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_ticket_id': self.id},
        }

    def action_view_partner_tickets(self):
        return {
            'name': _('Customer Tickets'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.partner_id.id)],
        }
