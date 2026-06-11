# -*- coding: utf-8 -*-
from odoo import fields, models


class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Helpdesk Category'
    _order = 'name'

    name = fields.Char(string='Category', required=True, translate=True)
    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one(
        'helpdesk.category',
        string='Parent Category',
        ondelete='set null',
    )
    child_ids = fields.One2many(
        'helpdesk.category',
        'parent_id',
        string='Sub-categories',
    )
