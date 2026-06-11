# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HelpdeskTeam(models.Model):
    _name = 'helpdesk.team'
    _description = 'Helpdesk Team'
    _inherit = ['mail.thread']
    _order = 'sequence, name'

    name = fields.Char(string='Team Name', required=True, tracking=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index')

    member_ids = fields.Many2many(
        'res.users',
        string='Team Members',
        domain="[('share', '=', False)]",
    )
    leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        domain="[('share', '=', False)]",
    )
    sla_id = fields.Many2one(
        'helpdesk.sla',
        string='Default SLA Policy',
    )
    alias_name = fields.Char(
        string='Email Alias',
        help='Incoming emails with this alias will create tickets.',
    )

    ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'team_id',
        string='Tickets',
    )
    ticket_count = fields.Integer(
        compute='_compute_ticket_count',
        string='Open Tickets',
    )
    ticket_open_count = fields.Integer(
        compute='_compute_ticket_count',
        string='Open Tickets',
    )

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for team in self:
            team.ticket_count = len(team.ticket_ids)
            team.ticket_open_count = len(
                team.ticket_ids.filtered(lambda t: not t.is_closed)
            )

    def action_view_tickets(self):
        return {
            'name': _('Tickets'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'list,kanban,form',
            'domain': [('team_id', '=', self.id)],
            'context': {'default_team_id': self.id},
        }
