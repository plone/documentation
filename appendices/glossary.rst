========
Glossary
========

This is a glossary for some definitions used in this documentation and still under construction.


.. glossary:: :sorted:

    Egg
        See :term:`Python egg`.

    reStructuredText
        The standard plaintext markup language used for Python
        documentation: http://docutils.sourceforge.net/rst.html

        `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ is an
        easy-to-read plaintext markup syntax and parser system. It is useful
        for in-line program documentation (such as Python docstrings), for
        quickly creating simple web pages, and for standalone documents.
        reStructuredText is designed to be extensible for specific
        application domains. The reStructuredText parser is a component of
        `Docutils <http://docutils.sourceforge.net/index.html>`_.

        reStructuredText is a revision and reinterpretation of the :term:`StructuredText` and `Setext <http://docutils.sourceforge.net/mirror/setext.html>`_ lightweight markup systems.

    slug
        A :term:`ZCML` *slug* is a one-line file created in a Zope instance's
        ``etc/package-includes`` directory, with a name like
        ``my.package-configure.zcml``. The contents of the file would be
        something like:
        ``<include package="my.package" file="configure.zcml" />``

        This is the Zope 3 way to load a particular package.

    VirtualHostMonster
        A Zope technology that supports virtual hosting. See
        `VirtualHostMonster URL rewriting mechanism
        <http://docs.zope.org/zope2/zope2book/VirtualHosting.html>`_

    Workflow
        Workflow is a very powerful way of mimicking business processes - it
        is also the way security settings are handled in Plone.

    ZODB
        The Zope Object Database is where your content is normally stored
        when you are using Plone. The default storage backend of the ZODB is
        *filestorage*, which stores the database on the file system in the
        file(s) such as ``Data.fs``, normally located in the ``var``
        directory.

    STX
    StructuredText
        Structured Text is a simple markup technique that is useful when you
        don't want to resort to HTML for creating web content. It uses
        indenting for structure, and other markup for formatting. It has
        been superseded by :term:`reStructuredText`, but some people still
        prefer the old version, as it's simpler.

    Catalog
        The catalog is an internal index of the content inside Plone so that
        it can be searched. The catalog object is accessible through the
        :term:`ZMI` as the ``portal_catalog`` object.

    DTML
        Document Template Markup Language. DTML is a server-side templating
        language used to produce dynamic pieces of content, but is now
        superseded by :term:`ZPT` for HTML and XML content. It is still used
        sparingly for non-XML content like SQL and mail/CSS.

    Document
        A document is a page of content, usually a self-contained piece of
        text. Documents can be written in several different formats, plain
        text, HTML or (re)Structured Text. The default home page for a Plone
        site is one example of a document.

    Expiration Date
        The last day an item should show up in searches, news listings etc.
        Please note that this doesn't actually remove or disable the item,
        it merely makes it not show up in searches.

        This is part of the Dublin Core metadata that is present on all
        Plone objects.

    Dublin Core
        Dublin Core is a standard set of metadata which enables the
        description of resources for the purposes of discovery. See
        https://en.wikipedia.org/wiki/Dublin_Core

    Layer
        A layer is a set of templates and scripts that get presented to the
        user. By combining these layers, you create what is referred to as a
        :term:`skin`. The order of layers is important, the topmost layers
        will be examined first when rendering a page. Each layer is an entry
        in ``portal_skins`` -> 'Contents', and is usually a Filesystem
        Directory View or a Folder.

    Skin
        A collection of template layers (see :term:`layer`) is used as the
        search path when a page is rendered and the different parts look up
        template fragments.  Skins are defined in the :term:`ZMI` in
        ``portal_skins`` tool. Used for both presentation and code
        customizations.

    ZMI
        The *Management Interface*.
        A Management Interface that is accessible through the web.
        Accessing it is as simple as appending ``/manage`` to your URL, for example:
        ``http://localhost/manage`` - or visiting Plone Setup and clicking
        the *Management Interface* link (Click 'View' to go back to the
        Plone site).
        Be careful in there, though - it's the "geek view" of
        things, and is not straightforward, nor does it protect you from
        doing stupid things. :)

    ZPL
        Zope Public License, a BSD-style license that Zope is licensed
        under.

    ZPT
        *Zope Page Templates* is the templating language that is used to
        render the Plone pages. It is implemented as two XML namespaces,
        making it possible to create templates that look like normal
        HTML/XML to editors. See
        http://docs.zope.org/zope2/zope2book/AppendixC.html

    i18n
        i18n is shorthand for "internationalization" (the letter I, 18
        letters, the letter N) - and refers to the process of preparing a
        program so that it can be used in multiple languages without further
        altering the source. Plone is fully internationalized.

    l10n
        Localization is the actual preparing of data for a particular
        language. For example Plone is i18n aware and has localization for
        several languages. The term l10n is formed by the first and last
        letter of the word and the number of letters in between.

    Request
        Each page view by a client generates a request to Plone. This
        incoming request is encapsulated in a *request* object in Zope,
        usually called REQUEST (or lowercase "request" in the case of ZPT).

    CSS
        Cascading Style Sheets is a way to separate content from
        presentation. Plone uses this extensively, and it is a web standard
        `documented at the W3C web site <http://www.w3.org/Style/CSS/>`_. If
        you want to learn CSS, we recommend `the W3Schools CSS Resources
        <http://www.w3schools.com/Css/default.asp>`_
        and the `SitePoint CSS Reference
        <http://reference.sitepoint.com/css>`_.

    LDAP
        Lightweight Directory Access Protocol. An internet protocol which
        provides a specification for user-directory access by wire,
        attribute syntax, representation of distinguished names, search
        filters, an URL format, a schema for user-centric information,
        authentication methods, and transport layer security. Example: an
        email client might connect to an LDAP server in order to look up an
        email address for a person by a person's name.

    Manager
        The *Manager* Security role is a standard role in Zope. A user with
        the Manager role has ALL permissions except the Take Ownership
        permission. Also commonly known as Administrator or root in other
        systems.

    Syndication
        Syndication shows you the several most recently updated objects in a
        folder in RSS format. This format is designed to be read by other
        programs.

    TTW
        This is a general term meaning an action can be performed
        "Through The Web," as opposed to, say, being done programmatically.

    TTP
        Actions done TTP are performed "Through the Plone" interface. It is
        normally a lazy way of telling you that you should not add things
        from the ZMI, as is the case for adding content, for example.

    PAS
        The Pluggable Authentication Service (PAS) is a framework for
        handling authentication in Zope 2. PAS is a Zope ``acl_users``
        folder object that uses "plugins" that can implement various
        authentication interfaces (for example :term:`LDAP` and
        :term:`OpenID`) that plug into the PAS framework .  Zope 3 also uses
        a design inspired by PAS. PAS was integrated into Plone at the 2005
        San Jose Sprint.

    Acquisition
        Simply put, any Zope object can acquire any object or property from
        any of its parents. That is, if you have a folder called *A*,
        containing two resources (a document called *homepage* and another
        folder called *B*), then an URL pointing at `http://.../A/B/homepage`
        would work even though *B* is empty. This is because Zope starts to
        look for *homepage* in *B*, doesn't find it, and goes back up to
        *A*, where it's found. The reality, inevitably, is more complex than
        this. For the whole story, see the `Acquisition chapter in the Zope
        Book <https://zope.readthedocs.io/en/latest/zope2book/Acquisition.html>`_.

    Kupu
        Kupu was the user-friendly graphical HTML editor component that used
        to be bundled with Plone, starting with version 2.1. It has since
        been replaced by :term:`TinyMCE`.

    TinyMCE
        A graphical HTML editor bundled with Plone.

    UML
        The *Unified Modeling Language* is a general-purpose modeling
        language that includes a standardized graphical notation used to
        create an abstract model of a system, referred to as a *UML model*.
        With the use of :term:`ArchGenXML`, this can be used to generate
        code for CMF/Plone applications (a :term:`Product`) based on the
        Archetypes framework.

    Product
        A Plone-specific module that extends Plone functionality and can be
        managed via the Plone Control Panel. Plone Products often integrate
        non-Plone-specific modules for use within the Plone context.

    Archetypes
        Archetypes is a framework designed to facilitate the building of
        applications for Plone and :term:`CMF`. Its main purpose is to
        provide a common method for building content objects, based on
        schema definitions. Fields can be grouped for editing, making it
        very simple to create wizard-like forms. Archetypes is able to do
        all the heavy lifting needed to bootstrap a content type, allowing
        the developer to focus on other things such as business rules,
        planning, scaling and designing. It provides features such as
        auto-generation of editing and presentation views. Archetypes code
        can be generated from :term:`UML` using :term:`ArchGenXML`.

    CMF
        The *Content Management Framework* is a framework for building
        content-oriented applications within Zope. It as formed the basis
        of Plone content from the start.

    OpenID
        A distributed identity system. Using a single URI provider an
        individual is able to login to any web site that accepts OpenID
        using the URI and a password. Plone implements OpenID as a
        :term:`PAS` plug-in.

    KSS
        *Kinetic Style Sheets* is a client-side framework for implementing
        rich user interfaces with AJAX functionality. It allows attaching
        actions to elements using a CSS-like rule syntax. KSS was added to Plone
        in Plone 3 and removed in Plone 4.3, because JQuery made it obsolete.

    Traceback
        A Python "traceback" is a detailed error message generated when an
        error occurs in executing Python code. Since Plone, running atop
        Zope, is a Python application, most Plone errors will generate a
        Python traceback. If you are filing an issue report regarding a
        Plone or Plone-product error, you should try to include a traceback
        log entry with the report.

        To find the traceback, check your
        ``event.log`` log file. Alternatively, use the ZMI to check the
        ``error_log`` object in your Plone folder. Note that your Zope must
        be running in *debug* mode in order to log tracebacks.

        A traceback will be included with nearly all error entries. A
        traceback will look something like this: "Traceback (innermost
        last): ...  AttributeError: adapters" They can be very long. The
        most useful information is generally at the end.

    PLIP
        *PLone Improvement Proposal* (just like Python's PEPs: Python
        Enhancement Proposals). These are documents written to structure and
        organise proposals for the improvement of Plone.

        Motivation, deliverables, risks and a list of people willing to do
        the work must be included. This document is submitted to the
        `Framework Team <https://plone.org/team/FrameworkTeam>`_, who reviews
        the proposal and decides if it's suitable to be included in the next
        Plone release or not.

        See more info about how to write a
        `PLIP <https://dev.plone.org/plone/wiki/PLIP>`_.

    ATCT
        ATContentTypes - the Plone content types written with Archetypes which
        replaces the default CMF content types in Plone 2.1 onwards.

    ResourceRegistries
        A piece of Plone infrastructure that allows CSS/JavaScript
        declarations to be contained in separate, logical files before
        ultimately being appended to the existing Plone CSS/JavaScript files
        on page delivery. Primarily enables Product authors to "register"
        new CSS/JavaScript without needing to touch Plone's templates, but
        also allows for selective inclusion of CSS/JavaScript files and
        reduces page load by minimizing individual calls to separate blocks
        of CSS/JavaScript files. Found in the :term:`ZMI` under
        ``portal_css`` and ``portal_javascript``.

    Collective
        The *Collective* is a community code repository for Plone Products
        and other add-ons, and is a useful place to find the very latest
        code for hundreds of add-ons to Plone. Developers of new Plone
        Products are encouraged to share their code via the Collective so
        that others can find it, use it, and contribute fixes and
        improvements.

    Sprint
        Based on ideas from the extreme programming (XP) community. A sprint
        is a three to five day focused development session, in which
        developers pair in a room and focus on building a particular
        subsystem. See https://plone.org/events/sprints

    RAD
        Rapid Application Development - A term applied to development tools
        to refer to any number of features that make programming easier.
        :term:`Archetypes` and :term:`ArchGenXML` are examples of these from
        the Plone universe.

    XXX
        XXX is a marker in the comments of the source code that should only
        be used during development to note things that need to be taken care
        of before a final (trunk) commit. Ideally, one should not expect to
        see XXXs in released software. XXX shall not be used to record new
        features, non-critical optimization, design changes, etc. If you
        want to record things like that, use TODO comments instead. People
        making a release shouldn't care about TODOs, but they ought to be
        annoyed to find XXXs.

    BBB
        When adding (or leaving) a piece of code for backward compatibility,
        we use a BBB comment marker with a date.

    TODO
        The TODO marker in source code records new features, non-critical
        optimization notes, design changes, etc.

    Monkey patch
        A monkey patch is a way to modify the behavior of Zope or a Product
        without altering the original code. Useful for fixes that have to
        live alongside the original code for a while, like security
        hotfixes, behavioral changes, etc.

        The term "monkey patch" seems to have originated as follows: First
        it was "guerrilla patch", referring to code that sneakily changes
        other code at runtime without any rules. In Zope 2, sometimes these
        patches conflict. This term went around Zope Corporation for a
        while. People heard it as "gorilla patch", though, since the two
        words sound very much alike, and the word gorilla is heard more
        often. So, when someone created a guerrilla patch very carefully and
        tried to avoid any battles, they tried to make it sound less
        forceful by calling it a monkey patch. The term stuck.

    ArchGenXML
        ArchGenXML is a code-generator for CMF/Plone applications
        (a :term:`Product`) based on the :term:`Archetypes` framework. It
        parses UML models in XMI-Format (``.xmi``, ``.zargo``, ``.zuml``),
        created with applications such as ArgoUML, Poseidon or ObjectDomain.
        A brief tutorial for ArchGenXML is present on the plone.org site.

    AGX
        AGX is short for :term:`ArchGenXML`.

    TAL
        Template Attribute Language. See :term:`ZPT`.

    METAL
        Macro Expansion Template Attribute Language. See :term:`ZPT`.

    TALES
        :term:`TAL` Expression Syntax. The syntax of the expressions used in
        TAL attributes.

    Software home
        The directory inside the Zope installation (on the filesystem) that
        contains all the Python code that makes up the core of the Zope
        application server. The various Zope packages are distributed here.
        Also referred to as the ``SOFTWARE_HOME`` environment variable. It
        varies from one system to the next, depending where you or your
        packaging system installed Zope. You can find the value of this in
        the *ZMI > Control Panel*.

    Zope instance
        An operating system process that handles HTTP interaction with a
        Zope database (:term:`ZODB`). In other words, the Zope web server
        process.  Alternatively, the Python code and other configuration
        files necessary for running this process.

        One Zope installation can support multiple instances. Use the
        buildout recipe ``plone.recipe.zope2instance`` to create new Zope
        instances in a buildout environment.

        Several Zope instances may serve data from a single ZODB using a
        ZEO server on the back-end.

    ZEO server
        ZEO (Zope Enterprise Objects) is a scaling solution used with Zope.
        The ZEO server is a storage server that allows multiple Zope
        instances, called ZEO clients, to connect to a single database.  ZEO
        clients may be distributed across multiple machines.  For additional
        info, see `the related chapter in The Zope Book
        <http://docs.zope.org/zope2/zope2book/ZEO.html>`_.

    Python path
        The order and location of folders in which the Python interpreter
        will look for modules. It's available in python via ``sys.path``.
        When Zope is running, this typically includes the global Python
        modules making up the standard library, the interpreter's
        site-packages directory, where third party "global" modules and eggs
        are installed, the Zope software home, and the ``lib/python``
        directory inside the instance home. It is possible for python
        scripts to include additional paths in the Python path during
        runtime. This ability is used by ``zc.buildout``.

    Python package
        A general term describing a redistributable Python module. At the
        most basic level, a package is a directory with an ``__init__.py``
        file, which can be blank.

    Zope product
        A special kind of Python package used to extend Zope. In old
        versions of Zope, all products were directories inside the special
        *Products* directory of a Zope instance; these would have a Python
        module name beginning with ``Products``. For example, the core of
        Plone is a product called *CMFPlone*, known in Python as
        ``Products.CMFPlone``.

    Python egg
        A widely used Python packaging format which consists of a zip or
        ``.tar.gz`` archive with some metadata information. It was
        introduced by
        `setuptools <https://pypi.python.org/pypi/setuptools>`_

        A way to package and distribute Python packages. Each egg contains a
        ``setup.py`` file with metadata (such as the author's name and email
        address and licensing information), as well as information about
        dependencies. ``setuptools``, the Python library that powers the egg
        mechanism, is able to automatically find and download dependencies
        for eggs that you install. It is even possible for two different
        eggs to concurrently use different versions of the same dependency.
        Eggs also support a feature called *entry points*, a kind of generic
        plug-in mechanism.

    Python Package Index
        The Python community's index of thousands of downloadable Python
        packages. It is available as a website to browse, with the ability
        to search for a particular package. More importantly,
        setuptools-based packaging tools (most notably, ``buildout`` and
        ``easy_install``) can query this index to download and install eggs
        automatically. Also known as the Cheese Shop or PyPI.

    easy_install
        A command-line tool for automatic discovery and installation of
        packages into a Python environment. The ``easy_install`` script is
        part of the ``setuptools`` package, which uses the
        :term:`Python Package Index` as its source for packages.

    Namespace package
        A feature of setuptools which makes it possible to distribute
        multiple, separate packages sharing a single top-level namespace.
        For example, the packages ``plone.theme`` and ``plone.portlets``
        both share the top-level ``plone`` namespace, but they are
        distributed as separate eggs. When installed, each egg's source code
        has its own directory (or possibly a compressed archive of that
        directory).  Namespace packages eliminate the need to distribute one
        giant plone package, with a top-level plone directory containing all
        possible children.

    ZCML
        Zope Configuration Markup Language. Zope 3 separates policy from the
        actual code and moves it out to separate configuration files,
        typically a ``configure.zcml`` file in a buildout. This file
        configures the Zope instance. 'Configuration' might be a bit
        misleading here and should be thought or more as wiring. ZCML, the
        XML-based configuration language that is used for this, is tailored
        to do component registration and security declarations, for the most
        part. By enabling or disabling certain components in ZCML, you can
        configure certain policies of the overall application. In Zope 2,
        enabling and disabling components means to drop in or remove a
        certain Zope 2 product. When it's there, it's automatically imported
        and loaded. This is not the case in Zope 3. If you don't enable it
        explicitly, it will not be found.



    .po
        The file format used by the :term:`gettext` translation system.
        http://www.gnu.org/software/hello/manual/gettext/PO-Files.html

    gettext
        UNIX standard software translation tool. See
        http://www.gnu.org/software/gettext/

    i18ndude
        Support tool to create and update message catalogs from instrumented
        source code.

    traversal
        Publishing an object from the ZODB by traversing its parent objects,
        resolving security and names in scope. See the `Acquisition chapter
        in the Zope 2 book
        <http://docs.zope.org/zope2/zope2book/ZEO.html>`_.
        http://docs.zope.org/zope2/zope2book/Acquisition.html

    GenericSetup
        An XML-based configuration system for Zope and Plone applications.

        .. todo:: Add reference.

    virtualenv
        ``virtualenv`` is a tool for creating a project directory with a
        Python interpreter that is isolated from the rest of the system.
        Modules that you install in such an environment remain local to it,
        and do not impact your system Python or other projects.

        .. todo:: Add reference.

    JSON
        JavaScript Object Notation. JSON is a lightweight text-based open
        standard designed for human-readable data interchange. In short,
        it's a string that looks like a JavaScript array, but is constrained
        to 6 simple data types. It can be parsed by many languages.

    ZCA
        The Zope Component Architecture (ZCA) is a Python framework for
        supporting component-based design and programming. It is very well
        suited to developing large Python software systems. The ZCA is not
        specific to the Zope web application server: it can be used for
        developing any Python application.
        From `A Comprehensive Guide to Zope Component Architecture
        <http://www.muthukadan.net/docs/zca.html>`_.

    Plonista
        A Plonista is a member of the Plone community.
        It can be somebody who loves Plone, or uses Plone, or someone who spreads Plone and Plone knowledge.
        It can also be someone who is a Plone developer, or it can be all of the above.

    control panel
        The Control Panel is the place where many parameters of a Plone site can be set.
        Here add-ons can be enabled, users and groups created, the workflow and permissions can be set and settings for language, caching and many other can be found.
        If you have "Site Admin" permissions, you can find it under "Site -> Site Setup" in your personal tools.

    Dexterity
        Dexterity is an alternative to :term:`Archetypes`, Plone's venerable content type framework. Being more recent, Dexterity has been able to learn from some of the mistakes that were made Archetypes, and - more importantly - leverage some of the technologies that did not exist when Archetypes was first conceived. Dexterity is built from the ground up to support through-the-web type creation. Dexterity also allows types to be developed jointly through-the-web and on the filesystem. For example, a schema can be written in Python and then extended through the web.

    Buildout
        Buildout is a Python-based build system for creating, assembling and deploying applications from multiple parts, some of which may be non-Python-based. It lets you create a buildout configuration and reproduce the same software later. See `buildout.org <http://www.buildout.org/en/latest/>`_

    browserview
         Plone uses a view pattern to output dynamically generated HTML pages. Views are the basic elements of modern Python web frameworks. A view runs code to setup Python variables for a rendering template. Output is not limited to HTML pages and snippets, but may contain JSON, file download payloads, or other data formats. See :doc:`views </develop/plone/views/browserviews>`

    toolbar
         Plone uses a toolbar to have quick access to the content management functions. On a standard instance, this will appear on the left of your screen. However, your site administrator might change this to have a horizontal layout, and it will appear hidden at first when using a smaller-screen device like a phone or tablet.

    Diazo
          The standard way to theme Plone sites from Plone 5 onwards. It consists in essence of a static 'theme' mockup of your website, with HTML, CSS and JavaScript files, and a set of rules that will 'switch in' the dynamic content from Plone into the theme.
