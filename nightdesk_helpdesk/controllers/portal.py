# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class HelpdeskPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            values['ticket_count'] = request.env['helpdesk.ticket'].search_count([
                ('partner_id', '=', request.env.user.partner_id.id)
            ])
        return values

    @http.route(['/my/tickets', '/my/tickets/page/<int:page>'],
                type='http', auth='user', website=True)
    def portal_my_tickets(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        ticket_count = request.env['helpdesk.ticket'].search_count(domain)
        pager = portal_pager(
            url='/my/tickets',
            total=ticket_count,
            page=page,
            step=20,
        )
        tickets = request.env['helpdesk.ticket'].search(
            domain,
            order='create_date desc',
            limit=20,
            offset=pager['offset'],
        )
        return request.render('helpdesk_ticketing.portal_my_tickets', {
            'tickets': tickets,
            'page_name': 'ticket',
            'pager': pager,
        })
