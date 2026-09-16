/* Copyright 2026 MKSOL TECH — Soft Navy Backend Theme */

odoo.define('soft_navy_backend_theme.Sidebar', function (require) {
    "use strict";

    var session = require('web.session');

    $(function () {
        (function ($) {
            $.addDebug = function (url) {
                return url.replace(/(.{4})/, "$1?debug");
            };
            $.addDebugWithAssets = function (url) {
                return url.replace(/(.{4})/, "$1?debug=assets");
            };
            $.delDebug = function (url) {
                return url.replace(/\?debug(=[^#]*)?/, "");
            };
        })(jQuery);

        $("#sidebar a").each(function () {
            var url = $(this).attr('href');
            if (!url) {
                return;
            }
            if (session.debug == 1) {
                $(this).attr('href', $.addDebug(url));
            } else if (session.debug == 'assets') {
                $(this).attr('href', $.addDebugWithAssets(url));
            } else if (session.debug == false) {
                $(this).attr('href', $.delDebug(url));
            }
        });
    });
});
