# Odoo Helpdesk - NightDesk

This repository contains the source code for the **NightDesk Helpdesk** module, a premium ticketing system built for Odoo 17.

![NightDesk Logo](nightdesk_helpdesk/static/description/icon.png)

## Overview

NightDesk Helpdesk is a comprehensive solution for managing customer support tickets with focus on efficiency, transparency, and automation.

## Key Features

- 🎫 **Full Ticket Lifecycle**: Track tickets from creation to resolution.
- 📂 **Smart Organization**: Categorize by type and priority for better workflow.
- 👥 **Agent Management**: Dedicated teams and agent assignment.
- ⏳ **SLA Management**: Configure and monitor Service Level Agreements.
- 🚀 **Advanced Escalation**: Automated rules to handle critical issues.
- 💬 **Integrated Mail**: Seamless communication through Odoo chatter.
- 📊 **Dynamic Dashboards**: Real-time insights into your support performance.

## Installation

### Odoo Community (On-Premise)

1.  **Navigate to your Odoo custom addons directory:**
    ```bash
    cd /path/to/odoo/custom-addons/
    ```

2.  **Clone the repository:**
    ```bash
    # Using SSH
    git clone ssh://git@github.com:Nocturnailed-Community/nightdesk_helpdesk.git
    
    # Or Using HTTPS
    git clone https://github.com/Nocturnailed-Community/nightdesk_helpdesk.git
    ```

3.  **Switch to the 17.0 branch:**
    ```bash
    cd nightdesk_helpdesk
    git checkout 17.0
    ```

4.  **Configure Odoo addons path:**
    Add the repository path to your `odoo.conf` file:
    ```ini
    addons_path = /path/to/odoo/addons,/path/to/custom-addons/nightdesk_helpdesk
    ```

5.  **Restart Odoo:**
    ```bash
    sudo systemctl restart odoo
    ```

6.  **Update Module List:**
    ```bash
    ./odoo-bin -u all -d your_database_name
    ```

### Via Odoo UI

1.  Activate **Developer Mode**.
2.  Go to **Apps** menu → click **Update Apps List**.
3.  Search for `NightDesk Helpdesk`.
4.  Click **Install**.

## Module Structure

```text
nightdesk_helpdesk/
├── __init__.py             # Module initialization
├── __manifest__.py         # Module metadata
├── models/                 # Database models
├── views/                  # XML views and menus
├── security/               # Access rights and rules
├── data/                   # Default data and sequences
├── static/                 # CSS, JS, and images
├── controllers/            # Web controllers
└── wizard/                 # Transient models (wizards)
```

## Technologies

- **Odoo 17**
- **Python**
- **XML**
- **JavaScript (OWL)**
- **CSS**

## Credits

Developed and maintained by **[Muhammad Ikhwan Fathulloh](https://github.com/Muhammad-Ikhwan-Fathulloh)**.

## License

This project is licensed under the [LGPL-3](LICENSE) license.
