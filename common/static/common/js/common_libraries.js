define(['domReady!', 'jquery', 'backbone', 'underscore', 'underscore.string', 'gettext'],
    function() {
        'use strict';

        // Underscore.string no longer installs itself directly on "_". For compatibility with existing
        // code, add it to "_" with its previous name.
        if (window._ && window.s) {
            window._.str = window.s;
        }
    });
