====================================
Javascript coding conventions
====================================

.. admonition:: Description

    Styleguides for writing Javascript for Plone

.. contents:: :local:

Introduction
------------

Here we have collected community best practices for writing Javascript for Plone.
These apply for Plone core and are suggested to be applied in your own add-on.

Progressive Enhancement
------------------------

Pages presented in Plone, including forms and form widgets, must be fully usable in situations where JavaScript is not available. The availability of JavaScript on the browser side should enhance the presentation of the page and its content. Additionally, the structured document delivered via HTML/XHTML should be semantically correct and complete in meaning.

The best way to accomplish these goals is to: first. compose complete and useful content in HTML; second, style its presentation with CSS; and third, make use of JavaScript behaviors to enhance presentation and interaction.

Unobtrusive JavaScript
------------------------

JavaScript should nearly never be present in the content area of a page. Typically, it will only appear via link and script elements in the head of the document (or at its very end when that improved rendering).
In particular, HTML tags should nearly never have event-handler (e.g., onclick or onsubmit) tag attributes or JavaScript in URLs. Coding JavaScript into HTML tags generally makes for code that is hard to maintain and nearly impossible to test.

Instead of coding event handlers in HTML attributes, use jQuery's "bind" and its various convenience aliases like "click" methods to attach event handlers to elements. Use "live" if installing behaviors that need to operate in AJAX-loaded HTML.

Coding Standards
-------------------

JSLint
=======

All JavaScript components that are incorporated into the Plone core must pass JSLint code quality tests. At some point in the 4.x series, this will become part of Plone's continuous integration testing.
JSLint has many options, and it is our goal that our code pass "The Good Parts" tests. A couple of acceptable deviations from the good parts settings are to::

    Assume a browser /*jslint browser: true */;
    Relax white-space requirements (removing "white: true") to allow for idiomatic composition of jQuery cascades.

    Assume availability of the globals jQuery, browser, window and location.

You may set these options by including at the top of your JavaScript file::

    /*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */

    /*global jQuery:false, document:false, window:false, location:false */

These settings are available as a file in Products/CMFPlone/skins/plone_ecmascript/js-standards.js. If you use those settings, you only need set the options for any deviations needed by the current file. Deviations like turning off the regular-expression "." prohibition, are perfectly reasonable when porting old code, but should be avoided in new code.

A common way to execute a command-line jslint test using these options would be to execute::

    cat js-standards.js accessibility.js | jslint

if you were testing the "accessibility.js" file. JSLint is also available as a plugin for most popular web code editors and can be set to test on save. An example of setting up TextMate to run jslint on save:
* JSLint on Save

Strict Mode
==============

Use strict in nested function scopy only::

    (function($) {
        "use strict";

    })

If you use "strict", you *must* test on a browser that supports it. Otherwise, your code may break when
it encounters such a browser.

Globals
==========

JavaScript components should create as few as possible global variables. If a component must create globals, it should only create one: a namespace object with a very distinctive name. Please document your new global at the top of the component file.

Platform Testing
-------------------

JavaScript for Plone core must be tested on

* IE 7, 8, 9

* Firefox, current release and most-recent beta or rc for the next release, if available

* Webkit browsers: Current

In general, degrade gracefully to no-js behavior when a platform cannot be supported. You need not support IE 6, but if you know that a feature works poorly on IE 6, simply turn it off::

    if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
        return;
    }

Testing
----------

As of this writing, the Plone community has not settled on standards for JavaScript unit and integration testing. QUnit is (as of this writing), the most common unit-testing mechanism. Selenium and Windmill are both in use for
unit testing.

Plone 4.2 is expected to include strong recommendations for both unit and integration testing, and these will be supported by our continuous integration testing.
