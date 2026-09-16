# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

from .theme_utils import darken, lighten, normalize_hex, rgba


THEME_DEFAULTS = {
    "theme_primary_color": "#0F2747",
    "theme_secondary_color": "#2EC4B6",
    "theme_accent_color": "#F4A261",
    "theme_surface_color": "#F4F7FA",
    "theme_sidebar_color": "#0A1A2F",
    "theme_text_color": "#334155",
    "theme_border_radius": 8,
    "theme_font_family": "segoe",
    "theme_sidebar_width": 200,
    "theme_navbar_height": 46,
    "theme_dashboard_overlay": 0.75,
    "theme_show_sidebar_default": True,
}

FONT_FAMILIES = {
    "segoe": '"Segoe UI", "Helvetica Neue", Arial, sans-serif',
    "roboto": '"Roboto", "Helvetica Neue", Arial, sans-serif',
    "inter": '"Inter", "Segoe UI", Arial, sans-serif',
    "open_sans": '"Open Sans", "Segoe UI", Arial, sans-serif',
    "lato": '"Lato", "Segoe UI", Arial, sans-serif',
    "system": 'system-ui, -apple-system, "Segoe UI", Arial, sans-serif',
}


class ResCompany(models.Model):
    _inherit = "res.company"

    dashboard_background = fields.Binary(
        string="Apps Dashboard Background",
        attachment=True,
    )

    # --- Theme customization ---
    theme_primary_color = fields.Char(
        string="Primary Color",
        default=THEME_DEFAULTS["theme_primary_color"],
        help="Navbar, headers, and primary UI accents.",
    )
    theme_secondary_color = fields.Char(
        string="Secondary Color",
        default=THEME_DEFAULTS["theme_secondary_color"],
        help="Buttons, links, and interactive highlights.",
    )
    theme_accent_color = fields.Char(
        string="Accent Color",
        default=THEME_DEFAULTS["theme_accent_color"],
        help="Optional accent for badges and decorative elements.",
    )
    theme_surface_color = fields.Char(
        string="Background Color",
        default=THEME_DEFAULTS["theme_surface_color"],
        help="Main content area background.",
    )
    theme_sidebar_color = fields.Char(
        string="Sidebar Color",
        default=THEME_DEFAULTS["theme_sidebar_color"],
    )
    theme_text_color = fields.Char(
        string="Text Color",
        default=THEME_DEFAULTS["theme_text_color"],
    )
    theme_border_radius = fields.Integer(
        string="Border Radius (px)",
        default=THEME_DEFAULTS["theme_border_radius"],
    )
    theme_font_family = fields.Selection(
        selection=[
            ("segoe", "Segoe UI"),
            ("roboto", "Roboto"),
            ("inter", "Inter"),
            ("open_sans", "Open Sans"),
            ("lato", "Lato"),
            ("system", "System Default"),
        ],
        string="Font Family",
        default=THEME_DEFAULTS["theme_font_family"],
    )
    theme_sidebar_width = fields.Integer(
        string="Sidebar Width (px)",
        default=THEME_DEFAULTS["theme_sidebar_width"],
    )
    theme_navbar_height = fields.Integer(
        string="Navbar Height (px)",
        default=THEME_DEFAULTS["theme_navbar_height"],
    )
    theme_dashboard_overlay = fields.Float(
        string="Dashboard Overlay Opacity",
        default=THEME_DEFAULTS["theme_dashboard_overlay"],
        help="Gradient overlay strength on the apps dashboard (0.0 – 1.0).",
    )
    theme_show_sidebar_default = fields.Boolean(
        string="Show Sidebar by Default",
        default=THEME_DEFAULTS["theme_show_sidebar_default"],
        help="Default sidebar visibility for new users in this company.",
    )

    @api.model
    def _theme_value(self, company, field_name):
        value = company[field_name] if company else THEME_DEFAULTS[field_name]
        if value in (False, None, ""):
            return THEME_DEFAULTS[field_name]
        return value

    @api.model
    def get_theme_config(self, company=None):
        """Return normalized theme settings for the given company."""
        company = company or self.env.user.company_id
        if not company:
            company = self.search([], limit=1)

        primary = normalize_hex(
            self._theme_value(company, "theme_primary_color"),
            THEME_DEFAULTS["theme_primary_color"],
        )
        secondary = normalize_hex(
            self._theme_value(company, "theme_secondary_color"),
            THEME_DEFAULTS["theme_secondary_color"],
        )
        accent = normalize_hex(
            self._theme_value(company, "theme_accent_color"),
            THEME_DEFAULTS["theme_accent_color"],
        )
        surface = normalize_hex(
            self._theme_value(company, "theme_surface_color"),
            THEME_DEFAULTS["theme_surface_color"],
        )
        sidebar = normalize_hex(
            self._theme_value(company, "theme_sidebar_color"),
            THEME_DEFAULTS["theme_sidebar_color"],
        )
        text = normalize_hex(
            self._theme_value(company, "theme_text_color"),
            THEME_DEFAULTS["theme_text_color"],
        )

        font_key = self._theme_value(company, "theme_font_family")
        font_family = FONT_FAMILIES.get(font_key, FONT_FAMILIES["segoe"])

        border_radius = max(0, min(24, int(
            self._theme_value(company, "theme_border_radius") or 8
        )))
        sidebar_width = max(160, min(320, int(
            self._theme_value(company, "theme_sidebar_width") or 200
        )))
        navbar_height = max(40, min(64, int(
            self._theme_value(company, "theme_navbar_height") or 46
        )))
        overlay = max(0.0, min(1.0, float(
            self._theme_value(company, "theme_dashboard_overlay") or 0.75
        )))

        return {
            "primary": primary,
            "primary_dark": darken(primary, 0.08),
            "primary_mid": darken(primary, 0.04),
            "secondary": secondary,
            "secondary_dark": darken(secondary, 0.10),
            "accent": accent,
            "surface": surface,
            "sidebar": sidebar,
            "sidebar_dark": darken(sidebar, 0.04),
            "text": text,
            "gray": lighten(text, 0.25),
            "gray_lighter": lighten(text, 0.55),
            "font_family": font_family,
            "border_radius": border_radius,
            "sidebar_width": sidebar_width,
            "navbar_height": navbar_height,
            "overlay": overlay,
        }

    @api.model
    def generate_backend_theme_css(self, company=None):
        cfg = self.get_theme_config(company)
        p, s = cfg["primary"], cfg["secondary"]
        r = cfg["border_radius"]

        return """
:root {
    --sn-primary: %(primary)s;
    --sn-primary-dark: %(primary_dark)s;
    --sn-secondary: %(secondary)s;
    --sn-secondary-dark: %(secondary_dark)s;
    --sn-accent: %(accent)s;
    --sn-surface: %(surface)s;
    --sn-sidebar: %(sidebar)s;
    --sn-text: %(text)s;
    --sn-radius: %(border_radius)spx;
    --sn-sidebar-width: %(sidebar_width)spx;
    --sn-navbar-height: %(navbar_height)spx;
}

body {
    font-family: %(font_family)s !important;
    background-color: %(surface)s !important;
    color: %(text)s !important;
}

.o_loading {
    background-color: %(secondary)s !important;
}

.o_main_navbar {
    background: linear-gradient(90deg, %(primary)s 0%%, %(primary_mid)s 60%%, %(primary_dark)s 100%%) !important;
    border-bottom: 2px solid %(secondary)s !important;
    box-shadow: 0 2px 12px %(rgba_primary_25)s !important;
}

.o_main_navbar > a:hover,
.o_main_navbar > a:focus,
.o_main_navbar > button:hover,
.o_main_navbar > button:focus,
.o_main_navbar > ul > li > a:hover,
.o_main_navbar > ul > li > label:hover,
.o_main_navbar .show .dropdown-toggle {
    background-color: %(rgba_secondary_18)s !important;
}

.btn-primary {
    background-color: %(secondary)s !important;
    border-color: %(secondary)s !important;
    box-shadow: 0 2px 8px %(rgba_secondary_35)s !important;
}

.btn-primary:hover {
    background-color: %(secondary_dark)s !important;
    border-color: %(secondary_dark)s !important;
}

.btn-link, a {
    color: %(secondary)s !important;
}

.btn-link:hover, a:hover {
    color: %(secondary_dark)s !important;
}

.btn, .btn-secondary, .dropdown-menu, .o_input,
input[type="text"], input[type="password"], input[type="number"],
textarea, select, .o_searchview {
    border-radius: %(border_radius)spx !important;
}

.o_web_client input:focus,
.o_web_client textarea:focus,
.o_web_client select:focus {
    border-color: %(secondary)s !important;
    box-shadow: 0 0 0 3px %(rgba_secondary_20)s !important;
}

.o_required_modifier.o_input,
.o_required_modifier .o_input {
    background-color: %(rgba_secondary_08)s !important;
}

.o_list_view.table thead {
    background: linear-gradient(180deg, %(list_head)s 0%%, %(list_head_dark)s 100%%) !important;
    color: %(primary)s !important;
}

.o_list_view tfoot {
    background-color: %(primary)s !important;
}

.o_form_view .o_form_sheet_bg {
    background-color: %(surface)s !important;
}

.o_form_view .o_form_sheet_bg .o_form_sheet {
    border-radius: %(sheet_radius)spx !important;
}

.o_form_view .o_horizontal_separator {
    color: %(primary)s !important;
}

.o_form_view .oe_button_box .oe_stat_button .o_stat_info .o_stat_value {
    color: %(secondary)s !important;
}

.o_searchview .o_searchview_facet .o_searchview_facet_label {
    background-color: %(primary)s !important;
}

.badge {
    border-color: %(secondary)s !important;
}

.o_external_button, .o_button_icon {
    color: %(secondary)s !important;
}

oe_highlight {
    background-color: %(primary)s !important;
}

.datepicker .table-sm > thead {
    background-color: %(primary)s !important;
}

.datepicker .table-sm > tbody > tr > td.active,
.datepicker .table-sm > tbody > tr > td .active {
    background-color: %(secondary)s !important;
}

.o_calendar_container .o_calendar_sidebar_container .ui-datepicker table .ui-state-active {
    background-color: %(primary)s !important;
}

.o_calendar_container .o_calendar_sidebar_container .ui-datepicker table .ui-state-default {
    color: %(primary)s !important;
}

.o_thread_window .o_thread_window_header {
    background-color: %(primary)s !important;
}

.app-sidebar-panel {
    top: %(navbar_height)spx !important;
    width: %(sidebar_width)spx !important;
    background: linear-gradient(180deg, %(sidebar)s 0%%, %(sidebar_dark)s 100%%) !important;
    border-right: 1px solid %(rgba_secondary_25)s !important;
}

body.o_web_client.soft_navy_sidebar_on .o_action_manager {
    margin-left: %(sidebar_width)spx !important;
}

.app-sidebar .app-sidebar-menu > li:hover > a {
    background: %(rgba_secondary_16)s !important;
    box-shadow: inset 3px 0 0 %(secondary)s !important;
}

.o_menu_apps .dropdown-menu.show {
    background-color: %(primary)s !important;
    background-image:
        linear-gradient(135deg, %(rgba_primary_88)s 0%%, %(rgba_primary_mid_75)s 45%%, %(rgba_secondary_50)s 100%%),
        url(/soft_navy/dashboard) !important;
    padding-top: %(navbar_pad)spx !important;
}
""" % {
            **cfg,
            "rgba_primary_25": rgba(p, 0.25),
            "rgba_primary_88": rgba(p, 0.88),
            "rgba_primary_mid_75": rgba(cfg["primary_mid"], 0.75),
            "rgba_secondary_08": rgba(s, 0.08),
            "rgba_secondary_16": rgba(s, 0.16),
            "rgba_secondary_18": rgba(s, 0.18),
            "rgba_secondary_20": rgba(s, 0.20),
            "rgba_secondary_25": rgba(s, 0.25),
            "rgba_secondary_35": rgba(s, 0.35),
            "rgba_secondary_50": rgba(s, cfg["overlay"] * 0.67),
            "list_head": lighten(p, 0.82),
            "list_head_dark": lighten(p, 0.78),
            "sheet_radius": min(r + 4, 24),
            "navbar_pad": cfg["navbar_height"] + 16,
        }

    def action_reset_theme_defaults(self):
        for company in self:
            for field, default in THEME_DEFAULTS.items():
                company[field] = default
        return True
