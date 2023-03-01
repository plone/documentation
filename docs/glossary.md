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

CMS
    Content Management System

Cookiecutter
    A command-line utility that creates projects from cookiecutters (project templates), for example, creating a Python package project from a Python package project template.
    [See Cookiecutter's documentation](https://cookiecutter.readthedocs.io/en/stable/).

cookiecutter-plone-starter
    [cookiecutter-plone-starter](https://github.com/collective/cookiecutter-plone-starter/) is a framework for jumpstarting Plone 6 projects quickly.

cookiecutter-zope-instance
    [cookiecutter-zope-instance](https://github.com/plone/cookiecutter-zope-instance) is a cookiecutter template to create a full and complex configuration of a Zope WSGI instance.

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

Linode
    [Linode.com](https://www.linode.com/) is an American privately owned virtual private server provider company based in Galloway, New Jersey, United States.

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

pm2
    [PM2](https://pm2.keymetrics.io/) is a daemon process manager.

REST API
    ```{todo}
    REST API in general. REST API of Plone.
    ```

S3
    [Amazon Web Services S3](https://aws.amazon.com/s3/).
    Object storage built to store and retrieve any amount of data from anywhere.

TTW
    Through-The-Web allows editing or customizing a Plone site through a web browser.

Amazon Opsworks
    [AWS OpsWorks](https://aws.amazon.com/opsworks/) is a configuration management service that uses Chef, an automation platform that treats server configurations as code.

Ansible
    [Ansible](https://www.ansible.com/) is an open source automation platform.
    Ansible can help you with configuration management, application deployment, task automation.

Archetypes
    The deprecated framework for building content types in Plone.

Chef
    [A configuration management tool written in Ruby and Erlang](https://www.chef.io/products/chef-infra/).

CloudFormation
    [AWS CloudFormation](https://aws.amazon.com/cloudformation/) gives developers and systems administrators an way to create and manage a collection of related AWS resources, provisioning and updating them in an orderly and predictable fashion.

Travis CI
    Travis CI is a hosted, distributed continuous integration service used to build and test software projects hosted at GitHub.
    Open source projects may be tested with limited runs via [travis-ci.com](https://www.travis-ci.com).

Solr
    [Solr](https://solr.apache.org/) is a popular, blazing-fast, open source enterprise search platform built on Apache Lucene.

ZCML
    The [Zope Configuration Mark-up Language](https://5.docs.plone.org/develop/addons/components/zcml.html).

Diazo
    [Diazo theme engine guide](https://docs.diazo.org/en/latest/).
    Diazo allows you to apply a theme contained in a static HTML web page to a dynamic website created using any server-side technology.

Dexterity
    [Dexterity](https://github.com/plone/plone.dexterity), the base framework for building content types, both through-the-web and as filesystem code for Zope.

Dublin Core
    The Dublin Core Schema is a small set of vocabulary terms that can be used to describe web resources (video, images, web pages, etc.), as well as physical resources such as books or CDs, and objects like artworks.

ZMI
    The Zope Management Interface.
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

block
    Blocks display a chunk of HTML which can be inserted in your Plone pages.

element
    Elements are the dynamic components of your blocks.
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

    In Plone core, [`plone.app.registry`](https://pypi.org/project/plone.app.registry/) provides Plone UI and `GenericSetup` integration for [`plone.registry`](https://pypi.org/project/plone.registry/), which in turn implements a configuration registry for Zope applications.

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

ES6
    ECMAScript 6, a newer version of the JavaScript language.

mrs-developer
    Also called "missdev", a tool similar to buildout's `mr.developer`.
    It automatically downloads and keeps up to date copies of software and add-ons under development based on definitions stored in `mrs.developer.json`.
    As a byproduct of its update operations, it also automatically adjusts `jsconfig.json`, which is used by Volto to configure webpack aliases.

Yarn
    [Yarn](https://yarnpkg.com/) is a JavaScript package manager.

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

    **React [Hooks](https://reactjs.org/docs/hooks-overview.html)** are a React API that allow function components to use React features, such as lifecycle methods, states, and so on.

hoisting
    [Hoisting](https://yarnpkg.com/advanced/lexicon#hoisting) is an optimization provided by Yarn.
    By default JavaScript packages will directly include dependencies inside their local `node_modules`.
    By hoisting we're "lifting" these inner dependencies to the top level `node_modules` directory, and thus optimize the generated bundles.
    In case two dependencies have conflicting version dependencies of the same library, the hoisting will not be possible (for that conflicting dependency) and you'll see multiple instances of the same library in the bundle, or you'll see that the add-on receives its own `node_modules` folder.

React
    [React](https://reactjs.org/) is a JavaScript library for building user interfaces.
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

    `````md
    ````{warning}
    There be dragons!
    ```{important}
    Dragons have feelings, too!
    ```
    ````
    `````

    ````{warning}
    There be dragons!
    ```{important}
    Dragons have feelings, too!
    ```
    ````

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

Volto
    [Volto](https://github.com/plone/volto) is a React-based frontend for the Plone CMS.
    It is the default user interface for Plone 6.

    The other frontend is {term}`Classic UI`.

Classic UI
    Classic UI is a secondary frontend for Plone 6.
    It is integrated with [Products.CMFPlone](https://github.com/plone/Products.CMFPlone/).
    Its theme is named [Barceloneta](https://github.com/plone/plonetheme.barceloneta/).
    It is based on Twitter Bootstrap 5.
    It uses [Mockup](https://github.com/plone/mockup/) as its JavaScript stack.
    [View Mockup's patterns](https://plone.github.io/mockup/dev/).

    The other frontend is {term}`Volto`.

Slate
    [Slate.js](https://docs.slatejs.org/) is a highly customizable platform for creating rich-text editors, also known as `WYSIWYG` editors.
    It enables you to create powerful, intuitive editors similar to those you've probably used in Medium, Dropbox Paper, or Google Docs.

`volto-slate`
    `volto-slate` is an interactive default text editor for Volto, developed on top of {term}`Slate`, offering enhanced WYSIWYG functionality and behavior.

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
    A library that is part of [Format.JS](https://formatjs.io/docs/getting-started/installation) which helps developers set up their applications for internationalization.

WSGI
    The Web Server Gateway Interface (WSGI, pronounced _WIZ-ghee_) is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.

ZEO
    [ZEO](https://zeo.readthedocs.io/en/latest/) is a client-server storage for ZODB for sharing a single storage among many clients.

ZODB
    [A native object database for Python](https://zodb.org/en/latest/).

Zope
    [Zope](https://zope.readthedocs.io/en/latest/) is a Python-based application server for building secure and highly scalable web applications.

ZPT
    Zope Page Template is a template language for Python.

plonecli
    The plonecli helps developers to create Plone add-ons in a modular and reproducible way.

ZCA
Zope Component Architecture
    Zope Component Architecture (ZCA) is a Python framework for supporting component based design and programming.
    It is very well suited to developing large Python software systems.
    The ZCA is not specific to the Zope web application server.
    It can be used for developing any Python application.
    Maybe it should be called Python Component Architecture.
    ```{seealso}
    See also https://muthukadan.net/docs/zca.html.
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
    The target object of the {term}`Request`

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
    [Node.js®](https://nodejs.org/en/) is an open-source, cross-platform JavaScript runtime environment.

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
```
