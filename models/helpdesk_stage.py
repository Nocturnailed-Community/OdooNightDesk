# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpdeskStage(models.Model):
    _name = 'helpdesk.stage'
    _description = 'Helpdesk Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(default=10)
    description = fields.Text(translate=True)
    is_closed = fields.Boolean(
        string='Closing Stage',
        help='Tickets in this stage are considered closed.',
    )
    fold = fields.Boolean(
        string='Folded in Kanban',
        help='Folded in the Kanban view.',
    )
    legend_normal = fields.Char(
        string='In Progress Legend',
        default='In Progress',
        translate=True,
    )
    legend_blocked = fields.Char(
        string='Blocked Legend',
        default='Blocked',
        translate=True,
    )
    legend_done = fields.Char(
        string='Ready Legend',
        default='Ready for Next Stage',
        translate=True,
    )
