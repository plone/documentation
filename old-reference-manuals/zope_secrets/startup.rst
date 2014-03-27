==================================
Startup and product initialisation
==================================

.. admonition:: Description

        What happens on Zope startup, and how do Zope 2 products and
        constructors work?

.. contents :: :local:

What happens on Zope startup?
=============================

A startup script (e.g. ``bin/instance fg``) calls Zope 2's ``run.py`` in an
appropriate interpreter context (i.e. one that has the necessary packages on
``sys.path``). This invokes a subclass of ``ZopeStarter`` from
``Zope2.Startup``:

.. code-block:: python

    import Zope2.Startup
    starter = Zope2.Startup.get_starter()
    opts = _setconfig()
    starter.setConfiguration(opts.configroot)
    starter.prepare()
    starter.run()

There are various variants that allow different ways to supply configuration.

There are two versions of the starter, one for Unix and one for Windows. It
performs a number of actions during the ``prepare()`` phase:

.. code-block:: python

    def prepare(self):
        self.setupInitialLogging()
        self.setupLocale()
        self.setupSecurityOptions()
        self.setupPublisher()
        # Start ZServer servers before we drop privileges so we can bind to
        # "low" ports:
        self.setupZServer()
        self.setupServers()
        # drop privileges after setting up servers
        self.dropPrivileges()
        self.setupFinalLogging()
        self.makeLockFile()
        self.makePidFile()
        self.setupInterpreter()
        self.startZope()
        self.serverListen()
        from App.config import getConfiguration
        config = getConfiguration()
        self.registerSignals()
        # emit a "ready" message in order to prevent the kinds of emails
        # to the Zope maillist in which people claim that Zope has "frozen"
        # after it has emitted ZServer messages.

        logger.info('Ready to handle requests')
        self.sendEvents()

Mostly, this is about using information from the configuration (which is read using
``ZConfig`` from a configuration file, or taken from the global defaults) to
set various module-level variables and options.

The ``startZope()`` call ends up in ``Zope2.App.startup.startup()``, which
performs a number of startup tasks:

* Importing products (``OFS.Application.import_products()``)
* Creating a ZODB for the chosen storage (as set in the ``ZConfig``
  configuration). This is stored in both ``Globals.DB`` and ``Zope2.DB``, and is
  configured using a ``dbtab`` (mount points specification) read from the configuration file.
  When this is done, the event ``zope.processlifetime.DatabaseOpened`` is
  notified.
* Setting the ``ClassFactory`` on the ZODB instance to
  ``Zope2.App.ClassFactory.ClassFactory``. This is a function that will attempt
  to import a class, and will return ``OFS.Uninstalled.Broken`` if the class
  cannot be imported for whatever reason. This allows for somewhat graceful
  recovery if symbols that are persistently referenced in the ZODB disappear.
* Loading ZCML configuration from ``site.zcml``. This in turn loads ZCML for all
  installed products in the ``Products.*`` namespace, and ZCML slugs. The
  ``load_zcml()`` call also sets up a ``Zope2VocabularyRegistry``.
* Creating the ``app`` object, an instance of
  ``App.ZApplication.ZApplicationWrapper`` that wraps a
  ``OFS.Application.Application``. The purpose of the wrapper is to:

  * Create an instance of the application object at the root of the ZODB on
    ``__init__()`` if it is not there already. The name by default is ``Application``.
  * Implement traversal over this wrapper (``__bobo_traverse__``) to open a ZODB
    connection before continuing traversal, and closing it at the end of the
    request.
  * Return the persistent instance of the true application root object when
    called.

  The wrapper is set as ``Zope2.bobo_application``, which is used when the
  publisher publishes the ``Zope2`` module |---| more on publication later.
* Initialising the application object using ``OFS.Application.initialize()``.
  This defensively creates a number of items:

  .. code-block:: python

        def initialize(self):
            # make sure to preserve relative ordering of calls below.
            self.install_cp_and_products()
            self.install_tempfolder_and_sdc()
            self.install_session_data_manager()
            self.install_browser_id_manager()
            self.install_required_roles()
            self.install_inituser()
            self.install_errorlog()
            self.install_products()
            self.install_standards()
            self.install_virtual_hosting()

* Notfiying the event ``zope.processlifetime.DatabaseOpenedWithRoot``
* Setting a number of ZPublisher hooks:

  .. code-block:: python

    Zope2.zpublisher_transactions_manager = TransactionsManager()
    Zope2.zpublisher_exception_hook = zpublisher_exception_hook
    Zope2.zpublisher_validated_hook = validated_hook
    Zope2.__bobo_before__ = noSecurityManager

The ``run()`` method of the ``ZopeStarter`` then runs the main startup loop
(note: this is not applicable for WSGI startup using ``make_wsgi_app()`` in
``run.py``, where the WSGI server is responsible for the event loop):

.. code-block:: python

    def run(self):
        # the mainloop.
        try:
            from App.config import getConfiguration
            config = getConfiguration()
            import ZServer
            import Lifetime
            Lifetime.loop()
            sys.exit(ZServer.exit_code)
        finally:
            self.shutdown()

The ``Lifetime`` module uses ``asyncore`` to poll for connected sockets until
shutdown is initiated, either through a signal or an explicit changing of the
flag ``Lifetime._shutdown_phase``, which is checked for each iteraton of the
loop.

Sockets are created when new connections are received on a defined server. When
using the built-in ZServer (i.e. not WSGI), the default HTTP server is defined
in ``ZServer.HTTPServer.zhttp_server``, which derives from
``ZServer.medusa.http_server``, which in turn is an ``asyncore.dispatcher``.

Servers are created in ``ZopeStarter.setupServers()``, which loops over the
``ZConfig``-defined server factories and call their ``create()`` metohod. The
server factories are defined in ``ZServer.datatypes``. (The word ``datatypes``
refers to ``ZConfig`` data types.)

Note also that some of the configuration data is mutated in the ``prepare()``
method of the server instance, which is called from
``Zope2.startup.handlers.root_handler()`` during the configuration phase. These
handlers are registered with a call to ``Zope2.startup.handlers.handleConfig()``
during the ``_setconfig()`` call in ``run.py``.

How are products installed?
===========================

During application initialisation, the method ``install_products()`` will call
the method ``OFS.Application.install_products()``. This will record products
in the ``Control_Panel`` if this is enabled in ``zope.conf``, and call the
``initialize()`` function for any product that has one with a *product context*
that allows the product to register constructors for the Zope runtime.

``install_products()`` loops over all product directories (configured via
``zope.conf`` and kept in ``Products.__path___`` by
``Zope2.startup.handlers.root_handler()``) and scans these for product
directories with an ``__init__.py``. For each, it calls
``OFS.Application.install_product``. This will:

* Import the product as a Python package
* Look for an attribute ``misc_`` at the product root, which is used to store
  things like icons. If it is a dictionary, wrap it in an ``OFS.misc_.Misc_`` object,
  which is just a simple, security-aware class. Then store a copy of it as an
  attribute on the object ``Application.misc_``. The attribute name is the
  product name. This allows traversal to the ``misc_`` resources.

  As an example of the use of the use of ``misc_``, consider this dictionary set up
  in ``Products/CMFPlone/__init__.py``:

  .. code-block:: python

    misc_ = {'plone_icon': ImageFile(
              os.path.join('skins', 'plone_images', 'logoIcon.png'),
              cmfplone_globals)}

  This can now be traversed to as ``/misc_/CMFPlone/plone_icon`` by virtue
  of the ``misc_`` attribute on the application root.
* Next, create an ``App.ProductContext.ProductContext`` to be used during
  product initialisation. This is passed a ``product`` object, a handle to the
  application root, and the product's package.

  There are two ways to obtain the ``product`` object:

  * If persistent product installation (in the ``Control_Panel``) is enabled
    in ``zope.conf``, call ``App.Product.initializeProduct``. This will
    create a ``App.Product.Product`` object and save it persistently in
    ``App.Control_Panel.Products``. It also reads the file ``version.txt`` from
    the product to determine a version number, and will change the persistent
    object (at Zope startup) if the version has changed. The ``product`` object is
    initialised with a product name and title and is used to store basic
    information about the product. The ``product`` object is then returned.

  * If persistent product installation is disabled (the default), simply
    instantiate a ``FactoryDispatcher.Product`` object (which is a simpler,
    duck-typing-equivalent of ``App.Product.Product``) with the product name.

* If the product has an ``initialize()`` method at its root, call it with the
  product context as an argument.

Once old-style products are initialised, any packages outside the ``Products.*``
namespace that want to be initialised are processed. The
``<five:registerProduct />`` ZCML directive stores a list of packages to be
processed and any referenced ``initialize()`` method in the variable
``OFS.metaconfigure._packages_to_initialize``, accessible via the function
``get_packages_to_initialize()`` in the same module. ``install_products()``
loops over this list, calling ``install_package()`` for each. This works very
much like ``install_product()``. When it is done, it calls the function
``OFS.metaconfigure.package_initialized()`` to remove the package from the
list of packages to initalise.

How do Zope 2 product constructors work?
========================================

Products can make constructors available to the Zope runtime. This is what
powers the ``Add`` drop-down in the ZMI, for instance. They do so by calling
``registerClass()`` on the product context passed to the ``initialize()``
function. This takes the following main arguments:

``instance_class``
  The class of the object that will be created.
``meta_type``
  A unique string representing kind of object being created, which appears in
  add lists. If not specified, then the class ``meta_type`` will be used.
``permission``
  The permission name for the constructors. If not specified, a permission name
  generated from the meta type (``"Add <meta_type>"``) will be used.
``constructors``
  A list of constructor methods. An element in the list can be a callable object
  with a ``__name__`` attribute giving the name the method should have in the
  product, or the a tuple consisting of a name and a callable
  object. The first method will be used as the initial method called
  when creating an object through the web (in the ZMI).

  It is quite common to pass in two constructor callables: one that is a
  ``DTMLMethod`` or ``PageTemplateFile`` that renders an add form and one that
  is a method that actually creates and adds an instance. A typical example from
  ``Products.MailHost`` is:

  .. code-block:: python

    manage_addMailHostForm = DTMLFile('dtml/addMailHost_form', globals())

    def manage_addMailHost(self,
                           id,
                           title='',
                           smtp_host='localhost',
                           localhost='localhost',
                           smtp_port=25,
                           timeout=1.0,
                           REQUEST=None,
                          ):
        """ Add a MailHost into the system.
        """
        i = MailHost(id, title, smtp_host, smtp_port)
        self._setObject(id, i)

        if REQUEST is not None:
            REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')

  These are then referenced in ``initialize()``:

  .. code-block:: python

    def initialize(context):
      context.registerClass(
          MailHost.MailHost,
          permission='Add MailHost objects',
          constructors=(MailHost.manage_addMailHostForm,
                        MailHost.manage_addMailHost),
          icon='www/MailHost_icon.gif',
      )

  The form will be called with a path like
  ``/<container>/manage_addProduct/MailHost/manage_addMailHostForm``. The
  ``<form />`` on this page has a relative URL ``action="manage_addMailHost"``,
  which means that when the form is submitted, the ``manage_addMailHost()``
  function is called. ``id``, ``title`` and the other variables are passed as
  request parameters and marshalled (by ``mapply()`` |---| see below) into function
  arguments, and the ``REQUEST`` is implicitly passed (again by ``mapply()``).
``icon``
  The name of an image file in the package to be used for instances. The class
  ``icon`` attribute will be set automagically if an icon is provided.
``permissions``
  Additional permissions to be registered.
``visibility``
  The string ``"Global"`` if the object is globally visible, or ``None``
  otherwise.
``interfaces``
  A list of the interfaces the object supports. These can be used to filter
  addable meta-types later.
``container_filter``
  A function that is called with an ``ObjectManager`` object as the only
  parameter, which should return a truth value if the object is happy to be
  created in that container. The filter is called before showing
  ``ObjectManager``'s ``Add`` list, and before pasting (after object copy or
  cut), but not before calling an object's constructor.

The main aims of this method are to register some new permissions, store
some information about the class in the variable ``Products.meta_types``, and
create a ``FactoryDispatcher`` that allow traversal to the constructor method.

* If an ``icon`` and ``instance_class`` are supplied, set an ``icon`` attribute
  on ``instance_class`` to a path like ``misc_/<productname>/<iconfilename>``.
* Register any ``permissions`` by calling
  ``AccessControl.Permission.registerPermissions()`` (described later).
* If there is no ``permission`` provided, generate a permission name as the
  string "Add <meta_type>", defaulting to being granted to ``Manager`` only.
  Register this permission as well.
* Grab the name of the first constructor passed in the ``constructors`` tuple.
  This can either be the function's ``__name__``, or a name can be provided
  explicitly by passing as the first list element a tuple of
  ``(name, function)``.
* Try to obtain the value of the symbol ``__FactoryDispatcher__`` in the
  package root (``__init__.py``) if set. If not, create a class on the fly with
  this name  by deriving from ``App.FactoryDispatcher.FactoryDispatcher`` and
  set this onto the product package as an attribute named
  ``__FactoryDispatcher__``.
* Set an attribute ``_m`` in the package root if it does not exist to an
  instance of ``AttrDict`` wrapped around the factory dispatcher. This is a
  bizzarre construction best described by its implementation:

  .. code-block:: python

    class AttrDict:

      def __init__(self, ob):
          self.ob = ob

      def __setitem__(self, name, v):
          setattr(self.ob, name, v)

* If no ``interfaces`` were passed in explicitly, obtain the interfaces
  implemented by the ``instance_class``, if provided.
* Record information about the primary constructor in the tuple
  ``Products.meta_types`` by appending a dictionary with keys:

  ``name``
    The ``meta_type`` passed in or obtained from the ``instance_class``.
  ``action``
    A path segment like ``manage_addProduct/<productname>/<constructorname>``.
    for the initial (first) constructor. More on ``manage_addProduct`` below.
  ``product``
    The name of the product, without the ``Product.`` prefix.
  ``permission``
    The add permission passed in or generated.
  ``visibility``
    Either ``"Global"`` or ``None`` as passed in to the method.
  ``interfaces``
    The list of interfaces passed in or obtained from ``instance_class``.
  ``instance``
    The ``instance_class`` as passed in to the method.
  ``container_filter``
    The ``container_filter`` as passed in to the method.
* Next, put the initial constructor and any further constructors passed in onto
  the ``_m`` pseudo-dictionary (which really just means setting them as
  attributes on the ``FactoryDispatcher``-subclass). The appropriate
  ``<methodname>__roles__`` attribute is set to a ``PermissionRole`` describing
  the add permission as well.
* If an ``icon`` filename was passed in, construct an ``ImageFile`` to read the
  icon file from the package and stash it in the ``OFS.misc_.misc_`` class so
  that it can be traversed to later.

Note that previously, the approach taken was to inject factory methods into
the class ``OFS.ObjectManager.ObjectManager``, which is the base class for most
folderish types in Zope. This is still supported for backwards compatibility,
by providing a ``legacy`` tuple of function objects, but is deprecated.

``Products.meta_types`` is used in various places, most notably in
``OFS.ObjectManager.ObjectManager`` in the methods ``all_meta_types()`` and
``filtered_meta_types()``.

The former returns all of ``Products.meta_types`` (plus possibly some legacy
entries in ``_product_meta_types`` on the application root object, used to
support through-the-web defined products via
``App.ProductRegistry.ProductRegistry``), applying the ``container_filter`` if
available and optionally filtering by ``interfaces``.

The latter is used to power the ``Add`` widget in the ZMI by creating a
``<select />`` box for all ``meta_types`` the user is allowed to add by checking
the add permission of each of the items returned by ``all_meta_types()``. The
``action`` stored in the ``meta_types`` list is then used to traverse to and
invoke a constructor.

Note that subclasses of ``ObjectManager`` may sometimes override
``all_meta_types()`` to set a more restrictive list of addable types. They may
also add to the list of the default implementation by setting a ``meta_types``
class or instance variable containing further entries in the same format as
``Products.meta_types``.

Finally, let us consider the ``manage_addProduct`` method seen in the ``action``
used to traverse to a registered constructor callable (e.g. an add form) using
a path such as ``/<container>/manage_addProduct/<productname>/<constructname>``.
It is set on ``OFS.ObjectManager.ObjectManager``, and is actually an instance of
``App.FactoryDispatcher.ProductDispatcher``. This is an
implicit-acquisition-capable object that implements ``__bobo_traverse__`` as
follows:

* Attempt to obtain a ``__FactoryDispatcher__`` attribute from the product
  package (from the name being traversed to), defaulting to the standard
  ``FactoryDispatcher`` class in the same module.
* Find a persistent ``App.Product.Product`` if there is one, or create a
  simple ``App.FactoryDispatcher.Product`` wrapper if persistent product
  installation has not taken place.
* Create an instance of the factory dispatcher on the fly, passing in the
  product descriptor and the parent object (i.e. the container).
* Return this, acquisition-wrapped in ``self``, to allow traversal to continue.

Traversal then continues over the ``FactoryDispatcher``. In the version of
this created by ``registerClass()``, each constructor is set as an attribute
on the product-specific dispatcher, with appropriate roles, so traversal will be
able to obtain the constructor callable.

There is also a fallback ``__getattr__()`` implementation in the base
``FactoryDispatcher`` class, which will inspect the ``_m`` attribute on the
product package for an appropriate constructor, and is also able to obtain
constructor information from a persistent ``Product`` instance (from
``Control_Panel`` if there was one). This supports a (legacy) approach where
instead of calling ``registerClass()`` to register constructors, constructors
are set in a dict called ``_m`` at the root of the product.

.. |---| unicode:: U+02014 .. em dash
