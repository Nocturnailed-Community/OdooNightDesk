# -*- coding: utf-8 -*-
{
    'name': 'NightDesk Helpdesk',
    'version': '17.0.1.0.0',
    'category': 'Services/Helpdesk',
    'summary': 'Modern helpdesk ticketing system with full lifecycle tracking',
    'description': """
NightDesk Helpdesk
==================
A premium and sophisticated helpdesk ticketing system built on Odoo 17. 
Designed for speed, efficiency, and professional support management.

Key Features:
-------------
- 🎫 **Ticket Management**: Create and track support tickets effortlessly.
- 📂 **Categorization**: Organize tickets by category and priority.
- 👥 **Team Assignment**: Assign tickets to specialized teams and agents.
- ⏳ **SLA Tracking**: Monitor Service Level Agreements in real-time.
- 🚀 **Automated Escalation**: Automatic ticket escalation for urgent issues.
- 💬 **Communication History**: Full audit trail of all customer interactions.
- 📊 **Insightful Dashboards**: Comprehensive reporting and analytics.
    """,
    'author': 'Muhammad Ikhwan Fathulloh (NightDesk)',
    'website': 'https://github.com/Nocturnailed-Community/OdooNightDesk',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'portal',
        'web',
    ],
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/helpdesk_data.xml',
        'data/helpdesk_sequence.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_stage_views.xml',
        'views/helpdesk_category_views.xml',
        'views/helpdesk_sla_views.xml',
        'views/helpdesk_menu.xml',
        'views/portal_templates.xml',
        'wizard/ticket_escalate_views.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [
            'nightdesk_helpdesk/static/src/css/helpdesk.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
}
