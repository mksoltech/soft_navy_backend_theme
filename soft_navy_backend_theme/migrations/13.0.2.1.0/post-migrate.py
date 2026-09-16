# -*- coding: utf-8 -*-
# Copyright 2026 MKSOL TECH
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

_logger = logging.getLogger(__name__)

# Old Login Page / Advanced CSS customization columns (removed from the model).
_OBSOLETE_COLUMNS = (
    "theme_login_primary",
    "theme_login_secondary",
    "theme_login_dark",
    "theme_custom_css",
)


def migrate(cr, version):
    cr.execute(
        """
        SELECT column_name
          FROM information_schema.columns
         WHERE table_name = 'res_company'
           AND column_name = ANY(%s)
        """,
        (list(_OBSOLETE_COLUMNS),),
    )
    existing = [row[0] for row in cr.fetchall()]
    for column in existing:
        _logger.info("Dropping obsolete res_company.%s", column)
        cr.execute('ALTER TABLE res_company DROP COLUMN IF EXISTS "%s"' % column)
