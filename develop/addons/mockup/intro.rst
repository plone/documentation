Introduction
============

Mockup is the new frontend library for Javascript development, which is going
to be used by plone.app.widgets and Plone 5.


Background
----------

Mockup grew out from searching for a solution to get all JavaScript within Plone into
a manageable, reproducible, stable and testable state.

Until now, JavaScript in Plone was added here and there by core modules and
addons to the Resource Registry of Plone. It was only possible to define 
the order in which JavaScript resources should be loaded. The order could 
be defined relative to another JavaScript resource. Same is valid for CSS
resources. It was not possible to declare dependencies to other JavaScript
resources. Either they were available because they were loaded beforehand into
the global namespace, or the script threw an error. None - or rarely any - of
the JavaScript within Plone was tested. Developers needed to know a fair amount
of Plone developing to contribute JavaScript or CSS resources to it, such as 
defining resources, registering those in the registry, or at least knowledge 
about the (now deprecated) portal_skins machinery. Therefore, mainly Python 
developers were contributing JavaScript code. It was too hard and boring for 
Frontend developers to help out here.

Plone's new theming engine ``Diazo`` solved some of the problems. But still,
JavaScript code was untested, and without a defined set of dependencies, it
did or did not work, often only by accident.

Mockup gives us an elegant solution to all of the problems outlined above: By
using RequireJS modules (as well as the Common JS based node modules for the
build infrastructure), we now have to declare every JavaScript dependency
explicitly. RequireJS resolves the dependency chains and loads all resources in
the correct order. Clubbering the global namespace is normally not necessary
anymore. Mockup encourages us to also test all JavaScript code, and it does it
by using well known testing frameworks which allows us to easily write unit and
integration tests. All patterns are encapsulated and can be easily reused.
Reusability is possible, because dependencies from JavaScript code on a
specific DOM structure is gone. Patterns are only loaded and configured via
HTML class names and data attributes only. Paradise.

`TODO: difference to patternslib` Around 2012, Mockup came to the stage. Rok
Garbas, always aware about the power behind JavaScript, developed Mockup out of
frustration with JavaScript. Mockup started as a fork of split-off
`Patternslib` - at least it took its idea of a Pattern registry. `Patternslib`
was developed by Cornelis Kolbach, Wichert Akkerman and fellows, including
Florian Friesdorf with whom Rok was in intense debate about ways of joining
efforts.

Mockup stayed a separate project, was accepted for inclusion in the Plone core
by the Framework Team in 2013 and is one big part of the upcoming Plone 5.

This documentation should help developers to better understand Mockup,
effectively quickstart projects and use Mockup in production.


Why mockup?
-----------

But wait, despite all of the well sounding hymns to mockup from above, aren't
there more established alternatives?

Well ... yes, there are. Mockup grew up in a world where none of these
alternatives were in sight. Now we have at least an upcoming Web Components W3C
standards draft with concrete implementations (X-Tags, Polymer) and Angular JS
Directives. Both of them could be used instead of Mockup.

And you can, if you want. Since mockup is so encapsulated, you can just switch
over and use something else. Or only small parts of Mockup. It's up to you and
your requirements.

But Mockup is only a small layer, which is loading others' JavaScript. The
bigger payload is the JavaScript loaded by mockup. E.g. TinyMCE, Select2, ACE
Editor and more. OK, Web components are doing the same and Angular JS also. Web
Components, a very promising approach which solves exactly the same problems as
Mockup does, is a W3C draft and its implementations only work for the most
modern browsers. So no IE<11 support with that. Angular JS is also a very
interesting framework, but it changes the way you work with JavaScript quite a
bit. Angular forces you to use all of their concepts. What
sense would it make to only use Angular Directives without controllers,
services, etc.?

I expect Mockup to stay relevant for Plone until Web Components are
standardized and stable and ECMAScript 6 is implemented by all Browsers we want
to support. That will happen, hopefully, in the near future. Then Mockup could
be changed to be a Web Components implementation, which again uses other top
notch, well established Frameworks to satisfy the needs of frontend developers.


The Goals of Mockup
-------------------

1. Standardize configuration of patterns implemented in js to use HTML data
   attributes, so they can be developed without running a backend server.

2. Use modern AMD approach to declaring dependencies on other js libs.

3. Full unit testing of js.


Technologies used with Mockup
-----------------------------

Mockup is much about JavaScript, and so it uses a JavaScript toolset, which is
quite common among JavaScript developers. This toolset includes:

- `Bower <http://bower.io/>`_ (`Github <https://github.com/bower/bower>`_,
  `Wikipedia <http://en.wikipedia.org/wiki/Bower_(software)>`_) for package
  management.

- `Grunt <http://gruntjs.com/>`_ (`Github <https://github.com/gruntjs/grunt>`_)
  for running repetitive tasks like combining files, minifying JavaScript,
  creating bundles and more.

- `RequireJS <http://requirejs.org/>`_ (`Github <https://github.com/jrburke/requirejs>`_)
  for defining dependencies between JavaScript modules. It uses the
  `Asynchronous Module Definition <https://github.com/amdjs/amdjs-api/blob/master/AMD.md>`_
  approach, as opposed to the `CommonJS Module Definition <https://github.com/cmdjs/specification/blob/master/draft/module.md>`_ is defining.
  There is a document, `explaining the reason behind AMD <http://requirejs.org/docs/whyamd.html>`_, which is worth a read.
  With the upcoming ECMA Script 6 standard, we will get JavaScript module
  definitions and dependency declarations `built into the Language <http://www.2ality.com/2014/09/es6-modules-final.html>`_.

- `Yeoman <http://yeoman.io/>`_ (`Github <https://github.com/yeoman>`_,
  `Wikipedia <http://en.wikipedia.org/wiki/Yeoman_(computing)>`_) for
  generating pattern scaffolds.

- `LESS <http://lesscss.org/>`_ (`Github <https://github.com/less>`_,
  `Wikipedia <http://en.wikipedia.org/wiki/Less_(stylesheet_language)>`_) as
  CSS preprocessor.

- `Node JS <http://nodejs.org/>`_ (`Github <https://github.com/joyent/node>`_,
  `Wikipedia <http://en.wikipedia.org/wiki/Node.js>`_) as a requirement for
  Grunt.

- Mocha

- PhantomJS

- React JS


`<>`_ (`Github <>`_, `Wikipedia <>`_)

As always, some of these technologies can be discussed controversially. There
are other options for package management, build infrastructure, declaring
dependencies, preprocessing CSS - nearly for each aspect of Mockup. JavaScript
has an insanely fast moving ecosystem. Fortunately, many Frameworks are quite
excellent. In the final analysis, we had to decide for some of these Frameworks. 
Mockup is using well proven and widely used Frameworks. For sure, we will have 
to adapt Mockup to fit to changed conditions in the future, but we're well off 
with the technologies chosen.
