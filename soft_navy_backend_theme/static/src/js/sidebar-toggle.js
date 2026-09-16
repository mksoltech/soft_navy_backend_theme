/* Copyright 2026 MKSOL TECH — Soft Navy Backend Theme */

odoo.define('soft_navy_backend_theme.sidebar_toggle', function (require) {
    "use strict";

    var session = require('web.session');
    var rpc = require('web.rpc');

    function applySidebarVisible(visible) {
        var $sidebar = $("#app-sidebar");
        var $body = $("body.o_web_client");
        if (!$sidebar.length) {
            $body.removeClass("soft_navy_sidebar_on");
            return;
        }
        if (visible) {
            $sidebar.removeClass("toggle-sidebar");
            $body.addClass("soft_navy_sidebar_on");
        } else {
            $sidebar.addClass("toggle-sidebar");
            $body.removeClass("soft_navy_sidebar_on");
        }
    }

    function applyFontSize(size) {
        var $body = $("body.o_web_client");
        $body.removeClass("soft_navy_font_small soft_navy_font_medium soft_navy_font_large");
        $body.addClass("soft_navy_font_" + (size || "medium"));
    }

    if ($("#app-sidebar").length && window.innerWidth > 768) {
        $("body.o_web_client").addClass("soft_navy_sidebar_on");
    }

    rpc.query({
        model: 'res.users',
        method: 'read',
        args: [[session.uid], ['sidebar_visible', 'theme_font_size']],
    }).then(function (res) {
        var user = res[0] || {};
        applySidebarVisible(!!user.sidebar_visible);
        applyFontSize(user.theme_font_size);
    }).guardedCatch(function () {
        applySidebarVisible(true);
        applyFontSize("medium");
    });
});
