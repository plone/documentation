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
    The [Zope Configuration Mark-up Language](https://docs.plone.org/develop/addons/components/zcml.html).

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

Project (Volto)
    The product of running the package `@plone/generator-volto`, resulting in a customizable instance of Volto.

Add-on (Volto)
    A JavaScript package that integrates with Volto's configuration registry and is able to enhance, extend, and customize it.

Add-on configuration loader (Volto)
    A function with signature `config => config`.
    It gets the Volto Configuration registry, and it must return it back after mutating it.
    It is similar to Generic Setup profiles in Plone Backend.
    An add-on must provide a default configuration loader that is always loaded when Volto runs.
    An add-on can have multiple configuration loaders, and they can be loaded optionally from the Volto configuration.

Configuration registry (Volto)
    A singleton object modeled using JavaScript modules.
    It is accessible from the Volto project by importing the module `@plone/volto/config` with `import registry from '@plone/volto/config'`.
    It contains the configuration of the Volto app.

Shadowing (Volto)
    Webpack provides an "alias" mechanism, where the path for a module can be aliased to another module.
    By using this mechanism Volto enables customization (file overrides), similar to `z3c.jbot.`

Razzle
    A tool that simplifies SPA and SSR configuration for React projects.

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

Server-Side Rendering (SSR)
    When first loading any Plone page, users will get HTML markup that closely matches the final DOM structure of the React components used to render that page.

Single Page Application (SPA)
    A type of JavaScript application that aims to provide a better user experience by avoiding unnecessary reloading of the browser page, instead using AJAX to load backend information.

Hot Module Replacement (HMR)
    A development feature provided by Webpack that automatically reloads, in the browser, the JavaScript modules that have changed on disk.

Yeoman
    A popular scaffolding tool similar to Plone's `mr.bob` or `ZopeSkel`.

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
    [Yarn](https://classic.yarnpkg.com/) is a JavaScript package manager.

Hydration (SSR)
    After loading an HTML page generated with SSR in the browser, React can "populate" the existing DOM elements, recreate and attach their coresponding components.

JSX
    A dialect of JavaScript that resembles XML, it is transpiled by Babel to JavaScript functions.
    React uses JSX as its component templating.

Scoped packages
    Namespace for JavaScript packages, they provide a way to avoid naming conflicts for common package names.

middleware (Redux)
    Custom wrappers for the Redux store dispatch methods.
    They allow customizing the behavior of the data flow inside the redux store.

hooks (React)
    Hooks are a React API that allow function components to use React features such as lifecycle methods, states, and so on.

hoisting (Yarn)
    An optimization provided by Yarn.
    By default JavaScript packages will directly include dependencies inside their local node_modules.
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

Make
make
    [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

    Make gets its knowledge of how to build your program from a file called the _makefile_, which lists each of the non-source files and how to compute it from other files.
    When you write a program, you should write a makefile for it, so that it is possible to use Make to build and install the program.

REST
    REST stands for [Representational State Transfer](https://en.wikipedia.org/wiki/Representational_state_transfer). It is a software architectural principle to create loosely coupled web APIs.

workflow
    A concept in Plone (and other CMS's) whereby a content object can be in a number of states (private, public, etcetera) and uses transitions to change between them (e.g. "publish", "approve", "reject", "retract"). See the [Plone docs on Workflow](https://docs.plone.org/working-with-content/collaboration-and-workflow/)

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
```
