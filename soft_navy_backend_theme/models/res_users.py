# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    sidebar_visible = fields.Boolean("Show App Sidebar", default=True)
    theme_font_size = fields.Selection(
        selection=[
            ("small", "Small"),
            ("medium", "Medium"),
            ("large", "Large"),
        ],
        string="Font Size",
        default="medium",
    )

    def __init__(self, pool, cr):
        init_res = super(ResUsers, self).__init__(pool, cr)
        extra_fields = ["sidebar_visible", "theme_font_size"]
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(extra_fields)
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(extra_fields)
        return init_res

    @api.model
    def default_get(self, fields_list):
        res = super(ResUsers, self).default_get(fields_list)
        if "sidebar_visible" in fields_list:
            company = self.env.user.company_id
            if company:
                res["sidebar_visible"] = company.theme_show_sidebar_default
        return res
