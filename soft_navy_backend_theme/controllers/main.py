# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64

from odoo.http import Controller, request, route
from werkzeug.utils import redirect

DEFAULT_IMAGE = "/soft_navy_backend_theme/static/src/img/dashboard-bg.svg"


class SoftNavyThemeController(Controller):

    @route(["/soft_navy/dashboard"], type="http", auth="user", website=False)
    def dashboard(self, **post):
        company = request.env.user.company_id
        if company.dashboard_background:
            image = base64.b64decode(company.dashboard_background)
            return request.make_response(image, [("Content-Type", "image")])
        return redirect(DEFAULT_IMAGE)

    @route(["/soft_navy/theme.css"], type="http", auth="user", website=False)
    def backend_theme_css(self, **post):
        company = request.env.user.company_id
        css = request.env["res.company"].sudo().generate_backend_theme_css(company)
        return request.make_response(
            css,
            [
                ("Content-Type", "text/css; charset=utf-8"),
                ("Cache-Control", "no-cache"),
            ],
        )
