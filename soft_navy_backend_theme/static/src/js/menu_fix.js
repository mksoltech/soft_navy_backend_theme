/* Copyright 2026 MKSOL TECH — Soft Navy Backend Theme */

odoo.define('soft_navy_backend_theme.menu_fix', function (require) {
    "use strict";

    var dom = require('web.dom');

    if (!dom || typeof dom.initAutoMoreMenu !== 'function') {
        return;
    }

    var originalInit = dom.initAutoMoreMenu.bind(dom);

    dom.initAutoMoreMenu = function ($el, options) {
        try {
            if (!$el || !$el.length || !$el[0]) {
                return;
            }
            return originalInit($el, options);
        } catch (err) {
            console.warn('Soft Navy theme: AutoMoreMenu skipped.', err);
        }
    };
});
