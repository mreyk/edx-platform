(function(requirejs) {
    requirejs.config({
        paths: {
            "moment": "xmodule/include/common_static/js/vendor/moment.min",
            "modernizr": "xmodule/include/common_static/js/vendor/afontgarde/modernizr.fontface-generatedcontent",
            "afontgarde": "xmodule/include/common_static/js/vendor/afontgarde/afontgarde",
            "edxicons": "xmodule/include/common_static/js/vendor/afontgarde/edx-icons",
            "draggabilly": "xmodule/include/common_static/js/vendor/draggabilly"
        },
        "moment": {
            exports: "moment"
        },
        "modernizr": {
            exports: "Modernizr"
        },
        "afontgarde": {
            deps: ["jquery", "modernizr"],
            exports: "AFontGarde"
        },
        "edxicons": {
            deps: ["jquery", "modernizr", "afontgarde"],
            exports: "edxicons"
        },
        "draggabilly": {
            deps: ["jquery"],
            exports: "Draggabilly"
        }
    });

}).call(this, RequireJS.requirejs);
