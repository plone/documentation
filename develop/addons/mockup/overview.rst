Overview of Mockup
==================

There is also a basic minimal pattern with comments all over the source
code, which explains the structure of a Mockup project. You can find it here:
https://github.com/collective/mockup-minimalpattern


Mockup Nomenclature
-------------------

Pattern
    Patterns are units of JavaScript, defined by a RequireJS/AMD style module.
    Patterns may require other patterns to operate, and may also require third
    party libraries.  Think of a pattern as a module -- encapsulated and
    separate, and providing a widget or tool to be used by other patterns or in
    html.

Bundle
    Bundles are defined in a similar way to *Patterns* -- they are encapsulated
    bits of JavaScript that define requirements for a bundle and have some
    extra code in them that's useful for integrating the required patterns into
    Plone products.


RequireJS vs Common JS modules
------------------------------

Mockup is using RequireJS and Common JS modules at the same time. For all
frontend related stuff, RequireJS with its configuration in `js/config.js` and
`define` method is used. For all build infrastructure related stuff, CommonJS
modules, with its `module.exports` declarations are used.

If you are aware about this distinction, you can avoid some head wrangling
moments.


Mockup Core Project Structure
-----------------------------

Mockup Core defines the basic infrastructure for Mockup: the base Grunt tasks,
a base pattern, the pattern registry and the documentation building framework.
You can reuse these components for mockup projects.

``bower.json``: All frontend related, bower managed dependencies.

``bower_components/``: Here, all bower managed dependencies are installed.

``Gruntfile.js``: Defines the tasks for running jshint and the tests.

``js/config.js``: RequireJS configuration. This is the file, where all
JavaScript dependencies are defined, so that RequireJS is able to find them via
a name.

``js/docs/``: Infrastructure for creating mockup's documentation from
comment-sections in pattern files, following a specific convention.

``js/grunt.js``: Mockup Core's grunt infrastructure.

``js/pattern.js``: Base Pattern.

``js/registry.js``: Mockup pattern registry.

``Makefile``: ``GNU make`` Makefile, which defines common actions for
developing with mockup-core. It uses Grunt to a large extend.

``node_modules/``: Node / npm managed dependencies are in here. These are all
not-frontend related JavaScript dependencies for running grunt, bower, tests
and the like.

``package.json``: Node / npm package dependencies and metadata for Mockup Core's
infrastructure. The dependencies defined in here land in ``node_modules``.

``tests/``: Contains all tests, including general setup and configuration code.


Mockup Project Structure
------------------------

``bower.json``: All frontend related, bower managed dependencies.

``bower_components/``: Here, all bower managed dependencies are installed.

``build/``: Contains the builded bundles. This are combined, optimized, and
minimized JavaScript code, as well as the compiled CSS (Less) and media files
from a bundle's dependencies.

``docs/``: Mockup documentation files and examples built with ``make docs``.

``Gruntfile.js``: Defines the tasks for creating bundles, documentation and
running the tests. It depends on mockup-core's `grunt base file
<https://github.com/plone/mockup-core/blob/87d58d984d5ab193e23f6b6fcd5883a159113b10/js/grunt.js#L53>`_.

``index.html``: Documentation index.html file. This is the entry file when
viewing the documentation via ``http://localhost:8000`` after starting ``python
-m SimpleHTTPServer`` in mockup root.

``js/bundles/``: The directory, where Mockup's bundles are defined.

``js/config.js``: RequireJS configuration. This is the file where all
JavaScript dependencies are defined, so that RequireJS is able to find them via
a name.

``js/i18n.js``: Fork of `jarn.jsi18n <https://github.com/collective/jarn.jsi18n>`_,
a JavaScript i18n framework and integration layer for Plone message catalogs.

``js/router.js``: Framework to add routing capabilities, execute callbacks on
routing, and manipulating the browser history on routing.

``js/ui/``: Mockup UI components for reuse in patterns (Buttons, Toolbars, etc).

``js/utils.js``: Generic reusable utilities for patterns. Current available
utilities include: ``generateId``, ``Loading`` animation, ``QueryHelper`` for
generating request query strings and more.

``less/``: All LESS style files, which are needed for bundles or patterns.
Grunt's less task default behavior is to compile a CSS file from the less
file with the same name as the bundle name. For more information se the `grunt.js
<https://github.com/plone/mockup-core/blob/87d58d984d5ab193e23f6b6fcd5883a159113b10/js/grunt.js#L53>`_
file in ``mockup-core``.

``lib/``: Extra frontend libraries, which are not available via bower. In our
case it's the `jquery.event.drag.js <http://threedubmedia.com/code/event/drag>`_
and `jquery.event.drop.js <http://threedubmedia.com/code/event/drop>`_ files,
which provide drag and drop events for jQuery.

``Makefile``: ``GNU make`` Makefile, which defines common actions for
developing with mockup. It uses Grunt to a large extent. E.g. ``make
bootstrap``, ``make test``, ``make docs`` and ``make bundles``. For more
information see: :ref:`makefile-commands`.

``mockup/``: Files for integrating ``mockup`` in Plone, e.g. in
``plone.app.widgets``. This is only for development purposes, so that the task
of copying bundle files to ``plone.app.widgets`` isn't necessary. Still, you
have to do a ``make bundle-BUNDLENAME`` for compiling the files, which are
accessed by ``plone.app.widgets``.

``node_modules/``: Node / npm managed dependencies are in here. These are all
not-frontend related JavaScript dependencies for running grunt, bower, tests
and the like.

``package.json``: Node / npm package dependencies and metadata for Mockup's
infrastructure. The dependencies defined in here land in ``node_modules``.

``patterns/``: Here, the actual patterns are defined. For each pattern, one
directory. Some patterns include LESS resource files, templates and submodules.

``setup.py``: Setuptools based Python package infrastructure. This file is
needed to include Mockup in Plone for development, e.g. in
``plone.app.widgets``.

``tests/``: Contains all tests for patterns and bundles, including general
setup and configuration code.
