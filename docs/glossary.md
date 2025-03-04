---
myst:
  html_meta:
    "description": "Terms and definitions used throughout the Plone Documentation."
    "property=og:description": "Terms and definitions used throughout the Plone Documentation."
    "property=og:title": "Glossary"
    "keywords": "Plone, documentation, glossary, term, definition"
---

(glossary-label)=

# Glossary

```{glossary}
:sorted: true

AWS
    [Amazon Web Services](https://aws.amazon.com/) offers reliable, scalable, and inexpensive cloud computing services.
    Free to join, pay only for what you use.

Barceloneta
    The default theme for Plone 5.

Buildout
    [Buildout](https://github.com/buildout/buildout/) is a Python-based tool for building and assembling applications from multiple parts, based on a configuration file.
    It was the most common way of installing Plone 3, 4, and 5, and can still be used with Plone 6.

CMS
    Content Management System

Cookiecutter
    A command-line utility that creates projects from cookiecutters (project templates), for example, creating a Python package project from a Python package project template.
    [See Cookiecutter's documentation](https://cookiecutter.readthedocs.io/en/stable/).

Cookieplone
    ```{versionadded} Volto 18.0.0-alpha.43
    ```

    [Cookieplone](https://github.com/plone/cookieplone) is the method to create a Plone project.
    You can use Cookieplone to build a backend add-on, a new Volto add-on, or a full project with both backend and frontend.
    Cookieplone simplifies the process using robust Cookiecutter templates from {term}`cookieplone-templates`.

cookieplone-templates
    [`cookieplone-templates`](https://github.com/plone/cookieplone-templates) is a collection of templates used by {term}`Cookieplone`.

plone/generator-volto
@plone/generator-volto
    ```{deprecated} Volto 18.0.0-alpha.43
    ```

    [`@plone/generator-volto`](https://www.npmjs.com/package/@plone/generator-volto) is deprecated in favor of {term}`Cookieplone` since Volto 18.0.0-alpha.43.
    See {ref}`upgrade-18-cookieplone-label`.

cookiecutter-plone-starter
    [cookiecutter-plone-starter](https://github.com/collective/cookiecutter-plone-starter/) creates a Plone project that you can install using {term}`Make`.
    It generates files for installing and configuring both the frontend and backend.
    For the backend, it uses {term}`cookiecutter-zope-instance` to generate configuration files for a {term}`Zope instance`.

cookiecutter-zope-instance
    [cookiecutter-zope-instance](https://github.com/plone/cookiecutter-zope-instance) is a cookiecutter template to create a full and complex configuration of a {term}`Zope instance`.

CSRF
Cross-Site Request Forgery
    Cross-Site Request Forgery (CSRF or XSRF) is a type of web attack that allows an attacker to send malicious requests to a web application on behalf of a legitimate user.
    The attack works by tricking the user's web browser into sending a request to the web application that the user did not intentionally make.
    This can allow an attacker to perform actions on the web application without the user's knowledge or consent.
    In Plone, CSRF protection is done almost transparently by [`plone.protect`](https://pypi.org/project/plone.protect/).

CSS
    Cascading Style Sheets (CSS) is a stylesheet language used for describing the (most of the times visual) representation of web pages.

DigitalOcean
    [DigitalOcean, Inc.](https://www.digitalocean.com/) is an American cloud infrastructure provider headquartered in New York City with data centers worldwide.

Grunt
    The JavaScript Task Runner.
    Automates the creation and manipulation of static assets for the theme.

Less
    A dynamic stylesheet language that can be compiled into {term}`CSS` (Cascading Style Sheets).

mxdev
    [mxdev](https://github.com/mxstack/mxdev) [mɪks dɛv] is a utility that makes it easy to work with Python projects containing lots of packages, and you want to develop only some of those packages.
    It is designed for developers who use stable version constraints, then layer their customizations on top of that base while using a version control system.
    This design allows developers to override their base package constraints with a customized or newer version.

NFS
    [Network File System](https://en.wikipedia.org/wiki/Network_File_System).


NPM
    npm is a package manager for the JavaScript programming language.
    It is the default package manager for the JavaScript runtime environment Node.js.
    Also a registry of JavaScript packages, similar to PyPI.

pip
    pip is the package installer for Python.
    See [tool recommendations](https://packaging.python.org/en/latest/guides/tool-recommendations/) for more information.

pipx
    [pipx](https://pypi.org/project/pipx/) allows you to install and run Python applications in isolated environments.

pyenv
    Python version management.
    [pyenv](https://github.com/pyenv/pyenv) lets you easily switch between multiple versions of Python.

pm2
    [PM2](https://pm2.keymetrics.io/) is a daemon process manager.

REST API
    A REST API (also called a RESTful API or RESTful web API) is an application programming interface (API) that conforms to the design principles of the representational state transfer (REST) architectural style.
    REST APIs provide a flexible, lightweight way to integrate applications and to connect components in microservices architectures.
    Plone uses [`plone.restapi`](https://github.com/plone/plone.restapi/) for its REST API.

S3
    [Amazon Web Services S3](https://aws.amazon.com/s3/).
    Object storage built to store and retrieve any amount of data from anywhere.

TTW
    Through-The-Web allows editing or customizing a Plone site through a web browser.

Ansible
    [Ansible](https://www.redhat.com/en/ansible-collaborative) is an open source automation platform.
    Ansible can help you with configuration management, application deployment, task automation.

Archetypes
    The deprecated framework for building content types in Plone.

Chef
    [A configuration management tool written in Ruby and Erlang](https://www.chef.io/products/chef-infra/).

CloudFormation
    [AWS CloudFormation](https://aws.amazon.com/cloudformation/) gives developers and systems administrators an way to create and manage a collection of related AWS resources, provisioning and updating them in an orderly and predictable fashion.

Solr
    [Solr](https://solr.apache.org/) is a popular, blazing-fast, open source enterprise search platform built on Apache Lucene.

ZCML
    The [Zope Configuration Mark-up Language](https://5.docs.plone.org/develop/addons/components/zcml.html).

Diazo
    [Diazo theme engine guide](https://docs.diazo.org/en/latest/).
    Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology.

Dexterity
    [Dexterity](https://github.com/plone/plone.dexterity) is the base framework for building content types, both through-the-web and as filesystem code.
     It is aimed at Plone, although this package should work with plain {term}`Zope` + CMF systems.

Dublin Core
    The Dublin Core Schema is a small set of vocabulary terms that can be used to describe web resources (video, images, web pages, etc.), as well as physical resources such as books or CDs, and objects like artworks.

ZMI
    The {term}`Zope` Management Interface.
    The ZMI is a direct interface into the backend software stack of Plone.
    While it can still serve as a valuable tool for Plone specialists to fix problems or accomplish certain tasks, it is not recommended as a regular tool for Plone maintenance.

TALES
    TAL Expression Syntax (TALES) expression, which by default expects a path.
    Python and string expressions are also allowed.

XML
    The Extensible Markup Language.

XSLT
    The Extensible Stylesheet Language Transformations.
    A language which defines elements to describe transformations to be applied on a document.

XPath
    XPath (XML Path Language) is a query language for selecting nodes from an XML document.

Rapido application
    It contains the features you implement.
    It is a folder containing templates, Python code, and YAML files.

blocks
    Blocks are the fundamental components of a page layout in {term}`Volto`.

element
    Elements are the dynamic components of your {term}`blocks`.
    They can be input fields, buttons, or computed HTML.
    They can also return JSON if you call them from a JavaScript app.

record
    A Rapido app is able to store data as records.
    Records are basic dictionaries.

Add-on
    An add-on in Plone extends its functionality.
    It is code that is released as a package to make it easier to install.

    In Volto, an add-on is a JavaScript package.

    In Plone core, an add-on is a Python package.

    -   [Plone core add-ons](https://github.com/collective/awesome-plone#readme)
    -   [Volto add-ons](https://github.com/collective/awesome-volto#readme)
    -   [Add-ons tagged with the trove classifier `Framework :: Plone` on PyPI](https://pypi.org/search/?c=Framework+%3A%3A+Plone)

Volto configuration loader
    A function with signature `config => config`.
    It gets the Volto configuration registry, and it must return it back after mutating it.
    It is similar to `GenericSetup` profiles in the Plone backend.
    An add-on must provide a default configuration loader that is always loaded when Volto runs.
    An add-on can have multiple configuration loaders, and they can be loaded optionally from the Volto configuration.

Configuration registry
    In Plone and in general, the configuration registry is where resources are registered for an application.

    In Volto, it is a singleton object modeled using JavaScript modules.
    It is accessible from the Volto project by importing the module `@plone/volto/config` with `import registry from '@plone/volto/config'`.
    It contains the configuration of the Volto app.

    In Plone core, [`plone.app.registry`](https://pypi.org/project/plone.app.registry/) provides Plone UI and `GenericSetup` integration for [`plone.registry`](https://pypi.org/project/plone.registry/), which in turn implements a configuration registry for {term}`Zope` applications.

component shadowing
shadowing
    Volto uses a technique called component shadowing to override an existing Volto component with our local custom version, without having to modify Volto's source code.

    Volto's source components are located in the filepath stem of `omelette/src/components/`.
    Custom components that shadow Volto's source would be located in the filepath stem of `src/customizations/components/`.
    Shadow components would have the same filepath as Volto's source compenents, excluding the stem.
    Thus `omelette/src/components/theme/Header/Header.jsx` would be shadowed by `src/customizations/components/theme/Header/Header.jsx`.

    Webpack provides an alias mechanism that allows component shadowing in Volto, where the path for a module can be aliased to another module.
    By using this mechanism of file overrides, or component shadowing, Volto enables customization, similar to `z3c.jbot.`

Razzle
    A tool that simplifies {term}`SPA` and {term}`SSR` configuration for React projects.

Webpack
    A tool that loads and bundles code and web resources using loaders.

Webpack entrypoint
    The main files generated by webpack as a result.
    They typically contain the application source code based on modules bundled together, but it can also include other resources, such as static resources.
    It can contain code to automatically trigger the load of other JavaScript code files called "chunks".

Babel
    A JavaScript compiler that "transpiles" newer standards JavaScript to something that any browser can load.

Express
    A JavaScript HTTP server with a simple API to build custom applications.
    Volto uses it as its server.

SSR
server-side rendering
    When a web browser or other HTTP client sends a request, the HTML markup for the page is created on the server, which sends a response consisting of HTML markup back to the client.

    In Volto, SSR returns HTML markup that closely matches the final {term}`DOM` structure of the React components used to render that page, but it is not the complete page.
    After the client loads the initial response, then the {term}`hydration` mechanism performs additional rendering on the client side, populating the DOM with additional HTML markup.

    In Classic UI, SSR returns the complete page back to the client in the response.
    In some rare cases, additional HTML snippets may be loaded, such as in overlays or dialogs.

    SSR enables a developer to customize a website per request and per user.
    In addition, SSR can improve performance and search engine optimization (SEO) for a website.

DOM
Document Object Model
    The Document Object Model (DOM) is a programming interface for web documents.
    It represents the page so that programs can change the document structure, style, and content.
    The DOM represents the document as nodes and objects; that way, programming languages, such as JavaScript and React, can interact with the page.

SPA
single page application
    A type of JavaScript application that aims to provide a better user experience by avoiding unnecessary reloading of the browser page, instead using {term}`AJAX` to load backend information.

HMR
hot module replacement
    [Hot module replacement](https://webpack.js.org/guides/hot-module-replacement/) (HMR) is a development feature provided by Webpack that automatically reloads, in the browser, the JavaScript modules that have changed on disk.

Ajax
AJAX
Asynchronous JavaScript and XML
    AJAX allows web applications to change parts of the page dynamically without reloading the entire page.
    In Plone, after a page with JavaScript is loaded, the JavaScript will send an asynchronous request to the server.
    The server will send a response back to the client, which is then rendered on the client side.

Yeoman
    [Yeoman](https://yeoman.io/) is a popular scaffolding tool similar to Plone's `mr.bob` or `ZopeSkel`.

CommonJS
    A JavaScript package standard, the equivalent of a Python wheel or egg.
    Enables JavaScript modules.

Transpilation
    The transformation of JavaScript code that uses advanced language features, unavailable for some browsers, to code rewritten to support them.

ECMAScript
    ECMAScript is a standard for scripting languages, including JavaScript, JScript, and ActionScript.
    It is best known as a JavaScript standard intended to ensure the interoperability of web pages across different web browsers.
    It is standardized by [Ecma International](https://ecma-international.org/) in the document [ECMA-262](https://ecma-international.org/publications-and-standards/standards/ecma-262/).

TC39
    Ecma International's [TC39](https://tc39.es/) is a group of JavaScript developers, implementers, academics, and more, collaborating with the community to maintain and evolve the definition of JavaScript.
    They established a [process](https://tc39.es/process-document/) where the proposals are discussed, developed, and eventually approved (or dropped).
    The process has five Stages (0 to 4) where reaching the Stage 4 means the proposal is finished, and it becomes part of the JavaScript specification.

`mr.developer`
    [`mr.developer`](https://pypi.org/project/mr.developer/) is a {term}`Buildout` extension that makes it easy to work with buildouts containing lots of packages, where you only want to develop a few of them.

`mrs-developer`
    Also called "missdev", a tool similar to buildout's `mr.developer`.
    It automatically downloads and keeps up to date copies of software and add-ons under development based on definitions stored in `mrs.developer.json`.
    As a byproduct of its update operations, it also automatically adjusts `jsconfig.json`, which is used by Volto to configure webpack aliases.

Yarn
    [Yarn](https://yarnpkg.com/) is both a JavaScript package manager and project manager.

Corepack
    [Corepack](https://github.com/nodejs/corepack) is a zero-runtime-dependency Node.js script that acts as a bridge between Node.js projects and the package managers they are intended to be used with during development.
    In practical terms, Corepack lets you use {term}`Yarn`, {term}`npm`, and {term}`pnpm` without having to install them.

    Corepack is distributed by default with all recent Node.js versions.

Git
    [Git](https://git-scm.com/) is a free and open source distributed version control system.

Hydration
    After loading an HTML page generated with {term}`SSR` in the browser, React can populate the existing {term}`DOM` elements, and recreate and attach their coresponding components.

JSX
    A dialect of JavaScript that resembles XML, it is transpiled by Babel to JavaScript functions.
    React uses JSX as its component templating.

Scoped packages
    Namespace for JavaScript packages, they provide a way to avoid naming conflicts for common package names.

Redux
Redux middleware
    Custom wrappers for the [Redux](https://redux.js.org/) store dispatch methods.
    They allow customizing the behavior of the data flow inside the Redux store.

hook
hooks
    In general, a hook in programming is a place in code that allows you to tap in to a module to either provide different behavior or to react when something happens.

    **React [Hooks](https://react.dev/reference/react)** are a React API that allow function components to use React features, such as lifecycle methods, states, and so on.

hoisting
    [Hoisting](https://yarnpkg.com/advanced/lexicon#hoisting) is an optimization provided by Yarn.
    By default JavaScript packages will directly include dependencies inside their local `node_modules`.
    By hoisting we're "lifting" these inner dependencies to the top level `node_modules` directory, and thus optimize the generated bundles.
    In case two dependencies have conflicting version dependencies of the same library, the hoisting will not be possible (for that conflicting dependency) and you'll see multiple instances of the same library in the bundle, or you'll see that the add-on receives its own `node_modules` folder.

React
    [React](https://www.reactjs.dev/) is a JavaScript library for building user interfaces.
    Volto, the frontend for Plone 6, uses React.

Sphinx
    [Sphinx](https://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation.
    It was originally created for Python documentation, and it has excellent facilities for the documentation of software projects in a range of languages.
    Sphinx uses {term}`reStructuredText` as its markup language, and many of its strengths come from the power and straightforwardness of reStructuredText and its parsing and translating suite, {term}`Docutils`.

Docutils
    [Docutils](https://docutils.sourceforge.io/) is an open-source text processing system for processing plaintext documentation into useful formats, such as HTML, LaTeX, man-pages, OpenDocument, or XML.
    It includes {term}`reStructuredText`, the easy to read, easy to use, what-you-see-is-what-you-get plaintext markup language.

reStructuredText
    [reStructuredText (rST)](https://docutils.sourceforge.io/rst.html) is an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax and parser system.
    The Plone 6 Documentation was written in reStructuredText originally, then converted to {term}`MyST` in 2022.

MyST
    [Markedly Structured Text (MyST)](https://myst-parser.readthedocs.io/en/latest/) is a rich and extensible flavor of Markdown, for authoring Plone Documentation.

Markdown
    [Markdown](https://daringfireball.net/projects/markdown/) is a text-to-HTML conversion tool for web writers.

fence
    A method to extend basic MyST syntax.
    You can define a directive with backticks (`` ` ``) followed by a reStructuredText directive in curly brackets (`{}`), and a matching number of closing backticks.
    You can also nest fences by increasing the number of backticks.

    `````{example}
    ````{warning}
    There be dragons!
    ```{important}
    Dragons have feelings, too!
    ```
    ````
    `````

Open Graph
    The [Open Graph protocol](https://ogp.me/) enables any web page to become a rich object in a social graph.
    For instance, this is used on Facebook to allow any web page to have the same functionality as any other object on Facebook.

srcset
    The [`HTMLImageElement`](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement) property `srcset` is a string which identifies one or more image candidate strings, separated using commas `,`.
    Each image candidate string specifies image resources to display in web pages under given circumstances.

    ```{seealso}
    https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/srcset
    ```

dots per inch
DPI
    Represents the number of [dots per inch](https://en.wikipedia.org/wiki/Dots_per_inch).
    Screens typically contain 72 or 96 dots per inch.

    ```{seealso}
    https://developer.mozilla.org/en-US/docs/Web/CSS/resolution#dpi
    ```

Docker
    [Docker](https://www.docker.com/) is an open platform for developing, shipping, and running applications using containers.

Docker Compose
    [Docker Compose](https://docs.docker.com/compose/) is a tool for defining and running multi-container Docker applications.

RelStorage
    [RelStorage](https://relstorage.readthedocs.io/en/latest/) is a storage implementation for ZODB that stores pickles in a relational database.

PostgreSQL
    [PostgreSQL](https://www.postgresql.org/) is a powerful, open source object-relational database.

HAProxy
    [HAProxy](https://www.haproxy.org/) is a free, very fast and reliable reverse-proxy offering high availability, load balancing, and proxying for TCP and HTTP-based applications.

nginx
    [nginx](https://docs.nginx.com/nginx/) (pronounced "engine x") is an HTTP and reverse proxy server, a mail proxy server, and a generic TCP/UDP proxy server, originally written by Igor Sysoev.

Traefik Proxy
    [Traefik Proxy](https://traefik.io/traefik/) is an open-source reverse proxy and load balancer, suitable for containerized architectures.

Volto
    [Volto](https://github.com/plone/volto) is a React-based frontend for Plone.
    It is one of two supported user interfaces, or frontends, for Plone 6.

    ````{seealso}
    {doc}`/conceptual-guides/choose-user-interface`
    ````

Classic UI
    Classic UI is a frontend for Plone 6 that is based on {term}`ZPT` and {term}`Mockup`.
    It is one of two supported user interfaces, or frontends, for Plone 6.

    ````{seealso}
    {doc}`/conceptual-guides/choose-user-interface`
    ````

Mockup
    [Mockup](https://github.com/plone/mockup/) is a package that, together with {term}`Patternslib`, builds the UI toolkit for {term}`Classic UI`, a frontend for Plone.
    Mockup provides the JavaScript stack for Classic UI.
    [View Mockup's patterns](https://plone.github.io/mockup/), based on Patternslib.

bobtemplate
bobtemplates
bobtemplates.plone
    `bobtemplates.plone` provides {term}`mr.bob` templates to generate packages for Plone projects.
    The {term}`plonecli` command line client provides a developer-friendly interface to `bobtemplates.plone`.

mr.bob
    [`mr.bob`](https://mrbob.readthedocs.io/en/latest/) is a tool that takes a directory skeleton, copies over its directory structure to a target folder, and can use the Jinja2 (or some other) templating engine to dynamically generate the files.
    Additionally, it can ask you questions needed to render the structure, or provide a configuration file to answer them.

Pattern
Patterns
Patternslib
    [Patterns](https://patternslib.com/), or Patternslib, is a toolkit that enables designers to build rich interactive prototypes without the need for writing any JavaScript.
    All functionality is triggered by classes and other attributes in the HTML, without abusing the HTML as a programming language.
    Accessibility, SEO, and well-structured HTML are core values of Patterns.

Slate
    [Slate.js](https://docs.slatejs.org/) is a highly customizable platform for creating rich-text editors, also known as {term}`WYSIWYG` editors.
    It enables you to create powerful, intuitive editors similar to those you've probably used in Medium, Dropbox Paper, or Google Docs.

`volto-slate`
    `volto-slate` is an interactive default text editor for Volto, developed on top of {term}`Slate`, offering enhanced {term}`WYSIWYG` functionality and behavior.

WYSIWYG
    WYSIWYG is an acronym for "what you see is what you get", referring to software that allows content to be edited in a form that resembles its appearance when printed or displayed as a finished product.    

TinyMCE
    The rich text {term}`WYSIWYG` editor used in {term}`Classic UI`.

elementEditor
    A generic {term}`volto-slate` plugin architecture that can be used to create other editor interactions that follow the pattern of having a button that toggles a format (an inline element).
    It also creates a separate edit form for advanced customization of the data attached to the element.

i18n
internationalization
Internationalization
    Internationalization is the process of preparing an application for displaying content in languages and formats specifically to the audience.
    Developers and template authors usually internationalize the application.
    "i18n" is shorthand for "internationalization" (the letter "I", 18 letters, the letter "N").
    Plone is fully internationalized.

    ```{seealso}
    {term}`localization`
    ```

l10n
localization
Localization
    Localization is the process of writing the translations of text and local formats for an application that has already been internationalized.
    Formats include dates, times, numbers, time zones, and currency.
    Translators usually localize the application.
    "l10n" is shorthand for "localization" (the letter "L", 10 letters, the letter "N").
    Plone is fully localized.

    ```{seealso}
    {term}`internationalization`
    ```

locale
    A locale is an identifier, such as a {term}`language tag`, for a specific set of cultural preferences for some country, together with all associated translations targeted to the same native language.

language tag
    A language tag is a string used as an identifier for a language.
    A language tag may have one or more subtags.
    The basic form of a language tag is `LANGUAGE-[SUBTAG]`.

    ```{seealso}
    -   W3C article [Language tags in HTML and XML](https://www.w3.org/International/articles/language-tags/)
    -   W3C Working Draft [Language Tags and Locale Identifiers for the World Wide Web](https://www.w3.org/TR/ltli/)
    ```

lxml
    A library used for processing XML and HTML with Python. It is a binding for the libxml2 and libxslt C libraries.
    See https://lxml.de/

gettext
    UNIX standard software translation tool.
    See https://www.gnu.org/software/gettext/.

LRF
Language Root Folder
    A content-type that contains the translated content for a specified language.
    For example, an LRF located at your site root for English would be `www.domain.com/en`, where `en` represents the LRF.

LIF
Language Independent Folder
    A folder containing static assets, such as images and files, for a given language.

PO file
`.po`
    Portable Object (PO) file.
    The file format used by the {term}`gettext` translation system.
    See https://www.gnu.org/savannah-checkouts/gnu/gettext/manual/html_node/PO-Files.html.

PO template file
`.pot`
    Portable Object (PO) template file, not yet oriented towards any particular language.

MO file
`.mo`
    Machine Object file.
    The binary message file compiled from the {term}`.po` message file.

i18ndude
    Support tool to create and update message catalogs from instrumented source code.

manual `.po` entries
    Entries which cannot be detected by an automatic code scan.

react-intl
    [`react-intl`](https://formatjs.github.io/docs/react-intl) is a library that is part of [Format.JS](https://formatjs.github.io/) which helps developers set up their applications for internationalization.

WSGI
    The Web Server Gateway Interface (WSGI, pronounced _WIZ-ghee_) is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.

ZEO
    [ZEO](https://zeo.readthedocs.io/en/latest/) is a client-server storage for ZODB for sharing a single storage among many clients.

ZODB
    [A native object database for Python](https://zodb.org/en/latest/).

Zope
    [Zope](https://zope.readthedocs.io/en/latest/) is a Python-based application server for building secure and highly scalable web applications.

Zope instance
    A Zope instance is a particular set of configuration for running {term}`Zope`.
    A new Zope instance can be created using {term}`cookiecutter-zope-instance`.

ZPT
    Zope Page Template is a template language for Python.

plonecli
    The [`plonecli`](https://pypi.org/project/plonecli/) helps developers to create Plone add-ons in a modular and reproducible way.

ZCA
Zope Component Architecture
    Zope Component Architecture (ZCA) is a Python framework for supporting component based design and programming.
    It uses the design patterns of interface, adapter, factory, and subscriber.
    It is very well suited to developing large Python software systems.
    The ZCA is not specific to the {term}`Zope` web application server.
    It can be used for developing any Python application.
    Maybe it should be called Python Component Architecture.

    ```{seealso}
    https://zopecomponent.readthedocs.io/en/latest/index.html
    ```

browser layer
Layer
    A layer—also called "browser layer"—is a marker interface and used in ZCML configurations.
    Layers allow you to enable and disable views and other site functionality based on installed add-ons and themes.

JSON
    JSON (JavaScript Object Notation, pronounced /ˈdʒeɪsən/; also /ˈdʒeɪˌsɒn/) is an open standard file format and data interchange format that uses human-readable text to store and transmit data objects consisting of attribute-value pairs and arrays (or other serializable values).

    ```{seealso}
    See also https://en.wikipedia.org/wiki/JSON.
    ```

`HTTPRequest`
    The `HTTPRequest` object contains information about the current request, which also includes browser layers.

interface
    An interface is a mechanism for labeling objects as conforming to a given API or contract.
    Interfaces define what methods an object provides.
    Plone extensively uses interfaces to define APIs between different subsystems.

    ```{seealso}
    See also https://zopeinterface.readthedocs.io/en/latest/.
    ```

Make
make
GNU make
    [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

    Make gets its knowledge of how to build your program from a file called the _makefile_, which lists each of the non-source files and how to compute it from other files.
    When you write a program, you should write a makefile for it, so that it is possible to use Make to build and install the program.

PLIP
    PLIPs are **PL**one **I**mprovement **P**roposals.
    These are about larger changes to Plone, discussed beforehand by the community.
    PLIPs are tracked in the GitHub issue tracker for [`Products.CMFPlone`](https://github.com/plone/Products.CMFPlone/issues?q=label%3A%2203+type%3A+feature+%28plip%29%22+).

REST
    REST stands for [Representational State Transfer](https://en.wikipedia.org/wiki/Representational_state_transfer). It is a software architectural principle to create loosely coupled web APIs.

workflow
    A concept in Plone (and other CMS's) whereby a content object can be in a number of states (private, public, etcetera) and uses transitions to change between them (e.g. "publish", "approve", "reject", "retract"). See the [Plone docs on Workflow](https://5.docs.plone.org/working-with-content/collaboration-and-workflow/)

HTTP-Request
HTTP Request
Request
Requests
    The initial action performed by a web client to communicate with a server. The {term}`Request` is usually followed by a {term}`Response` by the server, either synchronous or asynchronous (which is more complex to handle on the user side)

HTTP-Response
HTTP Response
Response
    Answer of or action by the server that is executed or send to the client after the {term}`Request` is processed.

HTTP-Header
HTTP Header
Header
    The part of the communication of the client with the server that provides the initialisation of the communication of a {term}`Request`.

HTTP-Verb
HTTP Verb
Verb
    One of the basic actions that can be requested to be executed by the server (on an object) based on the {term}`Request`.

Object URL
    The target object of the {term}`Request`.

Authorization Header
    Part of the {term}`Request` that is responsible for the authentication related to the right user or service to ask for a {term}`Response`.

Accept Header
    Part of the {term}`Request` that is responsible to define the expected type of data to be accepted by the client in the {term}`Response`.

Authentication Method
    Access restriction provided by the connection chain to the server exposed to the client.

Basic Auth
    A simple {term}`Authentication Method` referenced in the {term}`Authorization Header` that needs to be provided by the server.

content rule
    A content rule will automatically perform an action when a certain event, known as a {term}`trigger`, takes place.

trigger
    A trigger is an event in Plone that causes the execution of defined actions.
    Example triggers include object modified, user logged in, and workflow state changed.

DSL
    Domain Specific Language

navigation root
    An object marked as a navigation root provides a way to root catalog queries, searches, breadcrumbs, and so on, into that object.

FTI
Factory Type Information
    Factory type information (FTI) is responsible for content creation in the portal.
    FTI is responsible for the following:

    -   Which function is called when new content type is added.
    -   Icons available for content types.
    -   Creation views for content types.
    -   Permission and security.
    -   Whether discussion is enabled.
    -   Providing the `factory_type_information` dictionary.
        This is used elsewhere in the code (often in `__init__.py` of a product) to set the initial values for a ZODB Factory Type Information object (an object in the `portal_types` tool).

    ```{seealso}
    [`FactoryTypeInformation` class source code](https://github.com/zopefoundation/Products.CMFCore/blob/361a30e0c72a15a21f88433b8d5fc49331f36728/src/Products/CMFCore/TypesTool.py#L431)
    ```

`nvm`
Node Version Manager
    [`nvm`](https://github.com/nvm-sh/nvm/blob/master/README.md) allows you to quickly install and use different versions of node via the command line.

Node.js
    [Node.js®](https://nodejs.org/en) is an open-source, cross-platform JavaScript runtime environment.

view
    A view is the basic element of modern Python web frameworks.
    A view runs code to set up Python variables for a rendering template.
    The output is not limited to HTML pages and snippets, but may contain {term}`JSON`, file download payloads, or other data formats.

traversal
    Traversal is the process of determining the object that is the target of a request by examining the URL path of the request or in code, and looking up objects in the object hierarchy.

acquisition
    Acquisition is a mechanism that allows objects to inherit attributes from their parent objects in the object hierarchy.

Varnish
    [Varnish](https://varnish-cache.org) is a popular open source web accelerator that is used to implement HTTP caching.

Content Delivery Network
CDN
    A Content Delivery Network (CDN) is a network of servers located in various geographic regions that work together to deliver web content to users quickly and efficiently.

unique identifier
UID
   UID is an acronym meaning "unique identifier".
   A UID is an identifier that is guaranteed to be unique among all identifiers used for those objects and for a specific purpose.

pdb
    The Python Debugger module is an interactive source code debugger for Python programs. See https://docs.python.org/3/library/pdb.html

integer identifier
intid
    In Plone, an integer identifier, or intid, is used to uniquely identify content objects within a Plone site.
    Each content item in a Plone site is given a unique intid, which the system uses internally to reference content, keep track of link integrity, link translations, and other related purposes.

WSL
Windows Subsystem for Linux
    The [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) lets developers install a Linux distribution (such as Ubuntu, OpenSUSE, Kali, Debian, or Arch Linux) and use Linux applications, utilities, and Bash command-line tools directly on Windows, unmodified, without the overhead of a traditional virtual machine or dualboot setup.

pnpm
    [pnpm](https://pnpm.io/) is a fast, disk space efficient package manager.

predicate
predicates
    In programming, a predicate is a test which returns `true` or `false`.

pnpm workspace
workspace
    pnpm has built-in support for monorepositories (also known as multi-package repositories, multi-project repositories, or monolithic repositories).
    Workspaces provide support to manage multiple packages from your local file system from within a singular top-level, root package.

    When you run `pnpm install` at the root of the repository, pnpm installs dependencies for all workspaces, ensuring consistency across the entire project.
    This centralized approach streamlines development, facilitates code sharing, and simplifies the maintenance of complex projects.

ESLint
    [ESLint](https://eslint.org/) statically analyzes your code to quickly find problems.
    It is built into most text editors and you can run ESLint as part of your continuous integration pipeline.

Stylelint
    [Stylelint](https://stylelint.io/) is a CSS linter that helps you avoid errors and enforce conventions.

Prettier
    [Prettier](https://prettier.io/) is an opinionated code formatter.

GitHub workflow
GitHub workflows
    A [GitHub workflow](https://docs.github.com/en/actions/writing-workflows) is a configurable automated process that will run one or more jobs.

husky
    [Husky](https://typicode.github.io/husky/) automatically lints your commit messages, code, and runs tests upon committing or pushing commits to a remote repository.

Jest
    [Jest](https://jestjs.io/) is a JavaScript testing framework.
    Volto uses Jest for unit tests.

Cypress
    [Cypress](https://www.cypress.io/) is a JavaScript testing framework that runs your app in the browser for visually debugging it.
    Volto uses Cypress for acceptance tests.

Plone
    Plone is an open-source content management system (CMS) with over 20 years of stability and security wrapped in a modern, powerful, user-centric package.
    It continues to set the standard for content management systems by offering the most functionality and customization out of the box.

backend
Plone backend
    Plone's backend includes a content management system, a REST API, and {term}`Classic UI` as a {term}`frontend`.

frontend
Plone frontend
    A frontend consists of the user interface elements of a web application.
    Beginning with Plone 6, the default frontend is {term}`Volto`.
    {term}`Classic UI` is a secondary frontend that is part of the {term}`Plone backend`.

TLS
Transport Layer Security
    Transport Layer Security (TLS) is a cryptographic protocol designed to provide communications security over a computer network.

    ```{seealso}
    [Transport Layer Security](https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security) article from MDN.
    ```

TLS termination proxy
    A {term}`TLS` termination proxy is a proxy server that acts as an intermediary point between client and server applications.
    It is used to terminate or establish TLS tunnels by decrypting or encrypting communications.

Load balancer
    A load balancer acts as a traffic proxy and distributes network or application traffic across endpoints on a number of servers.

CI
continuous integration
    Continuous integration (CI) is the practice of integrating all your code changes into the main branch of a shared source code repository early and often, automatically testing each change when you commit or merge them, and automatically kicking off a build.

    Read about Plone's {doc}`/contributing/core/continuous-integration`.

CD
continuous deployment
continuous delivery
    Continuous deployment or continuous delivery is a software development practice that works in conjunction with {term}`CI` to automate the infrastructure provisioning and application release process.

lazy load
lazy loading
lazy loaded
    Lazy loading is a strategy to identify resources as non-blocking (non-critical) and load these only when needed.
    It's a way to shorten the length of the [critical rendering path](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Critical_rendering_path), which translates into reduced page load times.

reference implementation
    A reference implementation is a program that implements all requirements from a corresponding specification.
    The reference implementation often accompanies a technical standard, and demonstrates what should be considered the "correct" behavior of any other implementation of it.

distribution
distributions
    A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations.
    It is a convenient way to get a specific type of website up and running quickly, as the distribution includes everything needed to run that type of site.

    ```{seealso}
    -   {doc}`/conceptual-guides/distributions`
    -   {doc}`/developer-guide/create-a-distribution`
    ```

JSON Schema
    [JSON Schema](https://json-schema.org/) is the vocabulary that enables JSON data consistency, validity, and interoperability at scale.

portlets
    Portlets are widgets that can be inserted in predefined locations in pages in {term}`Classic UI`.
    Portlets are most commonly used to add sidebars to the left or right of the main page content.

Diátaxis framework
    Plone Documentation uses the [Diátaxis framework](https://www.diataxis.fr/), a systematic approach to technical documentation authoring.

Vale
    [Vale](https://vale.sh/) is an open-source, command-line tool that helps maintain a consistent and on-brand voice in documentation.
    Plone Documentation uses it to check spelling, English grammar and syntax, and style guides.

schema enhancer
    A schema enhancer uses the `schemaEnhancer` function, which can modify the schema used by the `InlineForm` component.
    Any registered extension plugin can provide a `schemaEnhancer` function.
    This function receives an object with `formData`, which is the block data; `schema`, which is the original schema to modify; and the injected `intl`, which aids with internationalization.

variation
    A variation is a common development pattern that provides alternative views for the same data.
    For example, a teaser block can present data as `title + link`, `title + description + link`, or `title + image + link`.
        
    An advanced variation can enhance the block by adding data fields to the block.
    For example, a listing block variation can show news items with `title + link`.
    Extending this example, a developer can add a boolean field to the block that toggles the display of the link.
    Thus an editor can select between `title + link` or just `title`.

HOC
Higher-Order Component
    A higher-order component (HOC) is an advanced technique in React for reusing component logic.
    HOCs are not part of the React API, per se.
    They are a pattern that emerges from React's compositional nature.
    Concretely, a higher-order component is a function that takes a component and returns a new component.
    
    ```{important}
    Higher-order components are not commonly used in modern React code.
    ```
    ```{seealso}
    https://legacy.reactjs.org/docs/higher-order-components.html
    ```

```
