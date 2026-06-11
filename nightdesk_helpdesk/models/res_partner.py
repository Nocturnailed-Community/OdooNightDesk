# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'partner_id',
        string='Support Tickets',
    )
    ticket_count = fields.Integer(
        compute='_compute_ticket_count',
        string='Tickets',
    )

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        for partner in self:
            partner.ticket_count = len(partner.ticket_ids)

    def action_view_tickets(self):
        return {
            'name': _('Tickets'),
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.ticket',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
