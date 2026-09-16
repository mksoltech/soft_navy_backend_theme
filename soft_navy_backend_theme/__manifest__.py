# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Soft Navy Backend Theme",
    "summary": "Fully customizable navy backend theme with apps dashboard for Odoo 13 Community",
    "version": "13.0.2.1.0",
    "category": "Theme/Backend",
    "website": "https://mksoltech.com",
    "author": "MKSOL TECH",
    "license": "LGPL-3",
    "support": "mksoltech@gmail.com",
    "installable": True,
    "application": False,
    "depends": [
        "web",
    ],
    "data": [
        "views/assets.xml",
        "views/theme_assets.xml",
        "views/res_company_view.xml",
        "views/users.xml",
        "views/sidebar.xml",
        "views/login.xml",
    ],
    "images": [
        "static/description/banner.png",
        "static/description/icon.png",
        "static/description/app_dashboard.png",
        "static/description/theme_customization.png",
        "images/screen.png",
    ],
    "live_test_url": "",
    "description": """
    Soft Navy Backend Theme
    =====================
    A fully customizable enterprise-style backend theme for Odoo 13 Community.

    Features
    --------
    * Modern navy / teal color scheme (fully customizable)
    * Company-level theme settings: colors, fonts, layout
    * Per-user preferences: sidebar visibility and font size
    * Full-screen apps dashboard with custom background per company
    * Left app sidebar (show/hide in user preferences)
    * Styled login page
    * Compatible with Odoo 13 Community Edition

    Technical name: soft_navy_backend_theme
    """,
}
