# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HelpdeskSLA(models.Model):
    _name = 'helpdesk.sla'
    _description = 'Helpdesk SLA Policy'
    _order = 'name'

    name = fields.Char(string='SLA Policy', required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)

    # Response time by priority (in hours)
    time_low = fields.Float(
        string='Low Priority (hrs)',
        default=72.0,
        help='Maximum response time in hours for Low priority tickets.',
    )
    time_normal = fields.Float(
        string='Normal Priority (hrs)',
        default=48.0,
        help='Maximum response time in hours for Normal priority tickets.',
    )
    time_high = fields.Float(
        string='High Priority (hrs)',
        default=24.0,
        help='Maximum response time in hours for High priority tickets.',
    )
    time_critical = fields.Float(
        string='Critical Priority (hrs)',
        default=4.0,
        help='Maximum response time in hours for Critical priority tickets.',
    )

    def _get_response_hours(self, priority):
        """Return hours based on ticket priority."""
        self.ensure_one()
        mapping = {
            '0': self.time_low,
            '1': self.time_normal,
            '2': self.time_high,
            '3': self.time_critical,
        }
        return mapping.get(priority, self.time_normal)
