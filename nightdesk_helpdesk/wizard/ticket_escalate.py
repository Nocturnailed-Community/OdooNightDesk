# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HelpdeskTicketEscalate(models.TransientModel):
    _name = 'helpdesk.ticket.escalate'
    _description = 'Escalate Ticket'

    ticket_id = fields.Many2one('helpdesk.ticket', required=True)
    new_team_id = fields.Many2one(
        'helpdesk.team',
        string='New Team',
        required=True,
    )
    new_user_id = fields.Many2one(
        'res.users',
        string='New Assignee',
        domain="[('share', '=', False)]",
    )
    reason = fields.Text(string='Escalation Reason', required=True)
    new_priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Critical'),
    ], string='New Priority')

    def action_escalate(self):
        self.ensure_one()
        ticket = self.ticket_id
        vals = {
            'team_id': self.new_team_id.id,
        }
        if self.new_user_id:
            vals['user_id'] = self.new_user_id.id
        if self.new_priority:
            vals['priority'] = self.new_priority

        ticket.write(vals)
        ticket.message_post(
            body=_('Ticket escalated to team <b>%s</b>.<br/>Reason: %s') % (
                self.new_team_id.name, self.reason
            ),
            subtype_xmlid='mail.mt_note',
        )
        return {'type': 'ir.actions.act_window_close'}
