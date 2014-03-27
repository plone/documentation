========
Security
========

.. admonition:: Description

        How does Zope handle permissions, roles and users?

Much of Zope security is implemented in C, for speed, but there is a Python
implementation in ``AccessControl.ImplPython``, which can be enabled by setting
``security-policy-implementation python`` in ``zope.conf``.

Note: We will not discuss RestrictedPython, used to apply security restrictions
to through-the-web python scripts and page templates, here.

.. contents :: :local:

Declaring object roles and attribute permissions
================================================

The permissions required to access a given attribute are stored on classes and
modules in a variable called ``__ac_permissions__``. This contains a tuple of
tuples that map a permission name to a list of attributes (e.g. methods)
protected by that permission, e.g.:

.. code-block:: python

    __ac_permissions__ = (
        ('View management screens', ['manage',
                                'manage_menu',
                                'manage_main',
                                'manage_copyright',
                                'manage_tabs',
                                'manage_propertiesForm',
                                'manage_UndoForm']),
        ('Undo changes',       ['manage_undo_transactions']),
        ('Change permissions', ['manage_access']),
        ('Add objects',        ['manage_addObject']),
        ('Delete objects',     ['manage_delObjects']),
        ('Add properties',     ['manage_addProperty']),
        ('Change properties',  ['manage_editProperties']),
        ('Delete properties',  ['manage_delProperties']),
        ('Default permission', ['']),
        )

The roles reuqired to access an object (e.g. a content object), are stored
in a class or instance variable ``__roles__``. This may contain a tuple or list
of role names, an ``AccessControl.PermissionRole.PermissionRole`` object, or one
of the following special variables:

``AccessControl.SecurityInfo.ACCESS_NONE``
  Inaccessible from any context.
``AccessControl.SecurityInfo.ACCESS_PRIVATE``
  Accessible only from Python code.
``AccessControl.SecurityInfo.ACCESS_PUBLIC``
  Accessible from restricted Python code and publishable through the web
  (provided the object has a docstring).

For attributes (including methods), the roles are stored on the parent class in
a variable called ``<name>__roles__``, where ``<name>`` is the attribute name.
Again, the special variables ``ACCESS_NONE``, ``ACCESS_PRIVATE`` and
``ACCESS_PUBLIC`` can be used.

These variables are rarely set manually. Instead, declarative security info
is typically used. For example:

.. code-block:: python

    from App.class_init import InitializeClass
    from AccessControl.SecurityInfo import ClassSecurityInfo
    from OFS.SimpleItem import Item

    class SomeClass(Item):

        ...

        security = ClassSecurityInfo()
        security.declareObjectPublic() # like __roles__ = ACCESS_PUBLIC

        security.declareProtected('Some permission, 'someMethod')
        def someMethod(self):
            ...

        InitializeClass(SomeClass)

There is also ``security.declareObjectProtected(<permission>)``,
``security.declareObjectPrivate()``, ``security.declarePrivate(<attribute>)``
and ``security.declarePublic(attribute)``, which do as their names suggest to
make an object or attribute protected, private or public.

Attribute security can be set in ZCML using the ``<class />`` directive with
one or more ``<require />`` sub-directives:

.. code-block:: xml

  <class class=".someclass.SomeClass">
    <require
      permission="some.permission"
      attributes="someMethod"
      />
  </class>

Behind the scenes, this simply creates a ``ClassSecurityInfo`` instance and invokes it
on the attributes listed as applicable. This will also call ``InitializeClass``
on the given class.

Note that the ``<require />`` directive, in common with all ZCML directives,
uses ZTK-style permission names, not Zope 2-style permission strings. A ZTK
permission is a named utility providing
``zope.security.interfaces.IPermission``, with an ``id`` that is the short
(usually dotted) name that is also the utility name, and a ``title`` that
matches the Zope 2 name. New permissions can be registered using the
``<permission />`` directive:

.. code-block:: xml

  <permission
    id="some.permission"
    title="Some permission"
    />

Zope 2-style permission names spring into existence whenever used in a security
declaration, which makes them susceptible to typos (ZTK-style ``IPermission``
utilities must be explicitly registered before they can be used).

Permissions are also represented by "mangled" permission names, which simply
turn the arbitrary string name of a permission into a valid Python identifier.
For example, the permission ``"Access contents information"`` becomes
``_Access_contents_information_Permission``. The mangling is done by the
function ``AccessControl.Permission.pname``.

``ClassSecurityInfo`` does little except record information until the
``InitializeClass()`` call is made with the class as an arugment. This will:

* Loop over all attributes and assign a ``__name__`` attribute to the value of
  any attribute in the class's ``__dict__`` that has the ``_need__name__``
  marker set (this is used by through-the-web DTML and Zope Page Template
  objects that may not have a name until they are assigned to their parent).
* Look for any function with the name ``manage()`` or a name starting with
  ``manage_``. If this does not have a corresponding ``<name>__roles__``
  attribute, one is created with the roles ``('Manager',)``, as a way to
  automatically protect such methods.
* Look for any security info object (i.e. an attribute that has an attribute
  ``__security_info__``). If one is found, call its ``apply()`` method with the
  class as an argument, and then delete it.

  The ``apply()`` method of ``ClassSecurityInfo`` does this:

  * Collect any explicitly set ``__ac_permissions__`` tuple and turn it into
    internal state, as if the ``ClassSecurityInfo`` had been used to set it,
    so that it is not lost.
  * For any attribute declared with ``declarePublic()`` or ``declarePrivate()``,
    set ``<name>__roles__`` to ``ACCESS_PUBLIC`` or ``ACCESS_PRIVATE`` as
    appropriate.
  * Build an ``__ac_permissions__`` tuple from the saved declarations of any
    protected attributes.

    As a special case, a call to
    ``security.declareObjectProtected(<permission>)`` will result in a value
    stored with an empty attribute name, which later translates as setting
    ``__roles__`` directly on the class.

* Find any ``__ac_permissions__`` on the class (probably created by the
  security info ``apply()`` call) and call
  ``AccessControl.Permission.registerPermissions`` with it as an argument.
  This will register the permission in a global list of known permissions with
  their default roles (usually ``('Manager',)``) held in that module under the
  variable ``_ac_permissions``. The mangled permission name (see above) will
  also be set as a class attribute on the class
  ``AccessControl.Permission.ApplicationDefaultPermissions``, which is a base
  class of the application root (``OFS.Application.Application``), hence making
  the mangled permission names available as (acquirable) class attributes on
  the application root. The value of this class variable is a tuple with the
  default roles for that permission.
* For all permissions in ``__ac_permissions__`` and for all attribute (method)
  names assigned to each permission, set a class attribute ``<name>__roles__``
  to a ``PermissionRole`` object. If a default list/tuple of roles was supplied,
  record this in the ``PermissionRole``, otherwise default to ``('Manager',)``.

Determining which roles have a given permission
===============================================

To perform security checks, it is necessary to compare the roles a user has
with the roles required for a given permission. The method to determine the
roles of a permission on a given object is called ``rolesForPermissionOn()``.
It is found in ``AccessControl.ImplPython``, though a C implementation may
also be in use.

``rolesForPermissionOn()`` can be called directly, but it should be imported
from ``AccessControl.PermissionRole`` to ensure the correct implementation (C
or Python) is used. Alternatively, the correct implementation can be accessed
by using the ``rolesForPermissionOn()`` method of a ``PermissionRole`` object,
which will supply the correct permission name and default roles.

The default ``rolesForPermissionOn()`` does the following:

* Mangle the permission name (see above).
* Traverse from the object up the inner (containment) acquisition chain to find an
  object with the mangled permission name as an attribute. Then:

  * If the attribute is ``None``, this is actually the ``ACCESS_PUBLIC`` marker.
    Return ``('Anonymous',)``.
  * If the sequence of roles is a tuple, this is a signal to not acquire roles
    from parent objects. Stop and return any roles collected by walking the
    acquisition chain so far plus the roles at the current object.
  * If the sequence of roles is a list, this is a signal to acquire roles from
    parent objects. Hence, collect the roles at the current object and continue
    the walk up the acquisition chain.
  * If roles is a string, assumed to be a different mangled permission name,
    this is a signal to delegate to another permission. Continue acquisition
    from the parent, but discard any roles acquired so far.

* If no object with the managled permission attribute is found, return the
  default roles. Applicable default roles are stored in each ``PermissionRole``
  object, but for other types of roles, use ``('Manager',)``.
* In all cases, if the global variable ``_embed_permission_in_roles`` is true,
  include the mangled permission name in the list of roles returned (even if
  an empty list). This is used as a debugging aid.

Checking a permission in a context
==================================

The most basic permission check can be done using:

.. code-block:: python

    from AccessControl import getSecurityManager
    sm = getSecurityManager()
    sm.checkPermission('Some permission', someObject)

This returns either ``1`` or ``None`` to indicate whether the current user
has such a permission.

The call to ``getSecurityManager()`` returns a security manager instance for the
current request. A security manager is created using ``newSecurityManager()`` in
the ``validated_hook`` at the end of traversal (hence note that it is *not* set
during traversal itself; specifically it is not set when a view adapter is being
looked up and instantiated and so there is no security information available in
the ``__init__()`` of a view), which creates a new security manager with a
context that is aware of the current authenticated user (or ``Anonymous`` if
there is none).

Again, the security manager may use a C implementation, but the default one
is defined in ``AccessControl.ImplPython``. The two most important methods on
this object are ``checkPermission()`` (seen above) and ``validate()``, which
is used during traversal to validate access to an object and will throw an
``Unauthorized`` exception if not valid. Both of these delegate to a security
policy, which will invariably be the ``ZopeSecurityPolicy`` also found in
``ImplPython`` (or C code) and instantiated once with a module-level call to
``setDefaultBehaviors()``.

The ``checkPermission()`` implementation in ``ZopeSecurityPolicy`` is relatively
simple. It uses ``rolesForPermissionOn()`` to discover the roles on the object,
and then obtains the current user from the security context (passed as a
parameter to its version of ``checkPermission()``) and calls the user object's
``allowed()`` method with the object and its roles.

Additionally, if the security policy allows for it (which it will by default),
checks are made to ensure that if the "execution context" has an owner (e.g. it
is a through-the-web Python script or template owned by a particular user), the
owner as well as the current user has the appropriate roles, otherwise access is
disallowed. Also, if proxy roles are set (again applicable to through-the-web
scripts), these are allowed to be used in lieu of the user's actual roles.

There are various user implementations that can treat ``allowed()`` differently.
The most common use in Plone is the ``PropertiedUser`` from
``Products.PluggableAuthService`` (PAS), though there is also a basic
implementation in ``AccessControl.users.BasicUser``, and a class called
``SpecialUser`` in the same module that is used for the ``Anonymous`` user.

The PAS version is only marginally more complex than the ``BasicUser``
implementation (it deals with roles obtained from groups a user belongs to), so
we will describe the ``allowed()`` implementation from ``BasicUser`` here:

* If the object's required roles is the special variable
  ``_what_not_even_god_should_do``   (you couldn't make this up), which
  corresponds to the ``ACCESS_NONE`` security declaration (as used by
  ``declareObjectPrivate()``), immediately disallow access.
* If the object's required roles is ``None``, which corresponds to the
  ``ACCESS_PUBLIC`` security declaration (as used by ``declareObjectPublic()``),
  or if ``Anonymous`` is one of the roles (even if the user is not
  ``Anonymous``), immediately allow access.
* If ``Authenticated`` is one of the required roles and the user is not
  ``Anonymous``, immediately allow access unless the object does not share an
  acquisition parent with the user folder (this is to avoid users with the same
  id in different user folders trying to steal each other's access through
  acquisition tricks). This is referred to as the "context check" below.
* Check if the user's global roles intersect with the roles required to access
  the object, and allow access if the user passes the context check.
* Check if there are any local roles, as defined in the attribute
  ``__ac_local_roles__``, granted to the user and check these against the
  required roles (and perform the context check). ``__ac_local_roles__`` may be
  a dictionary or a callable that returns a dictionary, containing a mapping of user ids (or
  group ids, if PAS is used) to local roles granted. The local role check is
  performed iteratively by walking up the acquisition chain and checking the
  instances of bound methods, up to the root of the acquisition chain.
* If none of the above succeed, return ``None`` to indicate that the user is not
  allowed to access the object.

Validating access to an object
==============================

The second type of security operation provided by the ``SecurityManager`` is to
check whether the user should be able to access a particular context. This is
most commonly used during traversal, by way of the user folder's ``validate()``
method. The version in ``Products.PluggableAuthService.PluggableAuthService``
does this:

* Get all applicable user ids from the request. Most likely, there is only one,
  but PAS's modular nature means it is possible more than one plugin will supply
  a user id.
* Extract the following information from the published object
  (``REQUEST['published']``):

  * ``accessed``, the object the published object was accessed through, i.e.
    the first traversal parent (``request['PARENTS'][0]``).
  * ``container``, the physical container of the object, i.e. the inner
    acquisition parent. If the published object is a method, the container is
    also set to be the method, but stripped of any outer acquisition chains by
    a call to ``aq_inner()``. If the published object does not have an inner
    acquisition parent, the traversal parent is used in the same way as it is
    used to set ``accessed``.
  * ``name``, the name used to access the object, e.g. a traversal path element.
  * ``value``, the object we are validating access to, i.e. the published
    object.

* If this is the top-level user folder and the user is the emergency user,
  return the user immediately without further authorisation.
* Otherwise, attempt to authorise the user by creating a new security manager
  for this user and calling its ``validate()`` method with ``accessed``,
  ``container``, ``name``, and ``value`` as arguments.

The default security manager ``validate()`` method delegates to the equivalent
method on the ``ZopeSecurityPolicy``. This is a charming 200+ line bundle of
``if`` statements that does something like this:

* If the ``name`` is an ``aq_*`` attribute other than ``aq_parent``,
  ``aq_inner`` or ``aq_explicit``, raise ``Unauthorized``.
* Obtain the ``aq_base``'d version of ``container`` and ``accessed``. If the
  ``accessed`` parent was not acquisition-wrapped, treat the ``aq_base``'d
  container as the ``aq_base``'d ``accessed``.
* The caller may have passed in the required roles already as an optimisation.
  If not, attempt to get the required roles by calling
  ``getRoles(container, name, value)``. The Python version of this is defined in
  ``AccessControl.ZopeSecurityPolicy``. It does the following:

  * If the ``value`` has a ``__roles__`` attribute, and it is ``None``
    (``ACCESS_PUBLIC``) or a list or tuple of roles, return them. (This probably
    means the ``value`` is a content object or similar.)
  * If it is a ``PermissionRole`` object or another object with a
    ``rolesForPermissionOn()`` method (described above), call this with the
    ``value`` as an argument and return the results. (This probably means the
    value is a method.)
  * If there is no ``__roles__`` attribute, check if we have a ``name``. Return
    "no roles" if not.
  * Attempt to find a class for the ``value``'s ``container``. If ``value`` is a
    method, go via the ``im_self`` attribute to get an instance to use as the
    ``container``. Then look for a ``<name>__roles__`` attribute on the class.
    If this is a ``PermissionRole``, call ``rolesForPermissionOn()`` as above;
    if it is a list, tuple or one of the sentinel values (``ACCESS_PUBLIC``,
    ``ACCESS_PRIVATE`` or ``ACCESS_NONE``, return it directly.

* If we still have no roles, we may have a primitive or other simple object
   that is not directly security-aware. We can still try to get security
   information from the ``container``:

  * If there is no ``container`` passed in, we have no way of inferring one, so
    all bets are off. Raise ``Unauthorized``.
  * Attempt to get a ``__roles__`` value from the ``container``. If it is
    acqusition-wrapped, also try to explicitly acquire ``__roles__`` if it does
    not have a ``__roles__`` attribute itself.

    If this fails, then we may still be able to get some security assertions
    from the container (see below), but we only allow this if the ``accessed``
    parent is the ``container``. If the ``value`` was accessed through a more
    convoluted acquisition chain, say, we cannot rely solely on container
    assertions, so we raise ``Unauthorized``.
  * At this point, there are two possibilities: we have some roles required to
    access the ``container``, or we have no roles at all, but we accessed the
    ``value`` directly from its parent ``container``. In both cases, we check
    container security assertions:

    * If the ``container`` is a tuple or string, and we have gotten this far, we
      consider access to be allowed and return true. (This can't really happen
      through URL traversal, but could occur with path traversal).
    * If the ``container`` is an object with an attribute
      ``__allow_access_to_unprotected_subobjects__``, obtain this. It can be
      of three things:

      An integer or boolean
        if set to a true value, allow access and return
        ``True``, otherwise raise ``Unauthorized``.
      A dictionary
        Attempt to look up a truth value in this dictionary by
        using the accessed ``name`` as a key. If not found or false, raise
        ``Unauthorized``, otherwise allow access and return ``True``. If the name
        is not found, default to allowing access.
      A callable
        Call it with the ``name`` and ``value`` as arguments, and
        use the return value to determine whether to allow access or raise
        ``Unauthorized``.

    * If there is no ``__allow_access_to_unprotected_subobjects__``, raise
      ``Unauthorized``.

  * If we did manage to get some roles from the container, we still check
    ``__allow_access_to_unprotected_subobjects__`` as above, but only as a
    negative: we raise ``Unauthorized`` if access is not allowed, and continue
    security checking against the roles we found otherwise. In this case, we
    use the ``container`` (probably a content object) as the ``value`` to check.
  * At this point, we have roles, and we know the container in theory allows
    access to the attribute that did not have its own security assertions. We
    set ``value`` to be the ``container`` so that we can check whether we are in
    fact allowed to access the container.
  * We can now check whether the user has the appropriate roles. This is
    essentially the same logic as in ``checkPermission()`` above, although
    stated slightly differently:

    * If ``__roles__`` is ``None`` (``ACCESS_PUBLIC``) or contains
      ``Anonymous``, allow access immediately.
    * If the execution context is something like a through-the-web Python script
      owned by a user, we raise ``Unauthorized`` if the owner does not have any
      of the required roles.
    * If the execution context has proxy roles, these are allowed to be used
      to validate access intead of the user's actual roles.
    * Otherwise, call ``user.allowed()`` to validate access and either return
      true or raise ``Unauthorized``.

The remainder of the logic in ``validate()`` concerns the case where
``verbose-security`` is enabled in ``zope.conf``. Various checks are made in
an attempt to raise ``Unauthorized`` exceptions with meaningful descriptions
about where in the validation logic access was denied.

Changing permissions
====================

The mapping of permissions to roles can be managed persistently at any object by
setting the mangled permission attribute (see the description of
``rolesForPermissionOn()`` above) to a list of roles as an instance variable.

The most basic API to do so is the class
``AccessControl.Permission.Permission``. This is a transient helper class
initialised with a (non-mangled) permission name (i.e. the first element in an
``__ac_permissions__`` tuple), a tuple of attributes the permission applies to
(i.e. the second element in an ``__ac_permissions__`` item) |---| referred to as
the variable ``data`` |---| and an object where the permission is being managed.

The methods ``getRoles()``, ``setRoles()`` and ``setRole()`` on the
``Permission`` class allow roles to be obtained and changed.

``getRoles()`` will first attempt to get the mangled permission name attribute
and return its value.

If it is not set, it will fall back to looping over all the listed attributes
(``data``) and obtaining the roles from the first one found, taking into account
the various ways in which ``__roles__`` can be stored. Note that an empty string
in the tuple of attributes means "check the object itself for a ``__roles__``
attribute". If ``__roles__`` is a list, it is returned, though if it contains
the legacy role ``Shared``, this is removed first. The sentinel ``None``
(``ACCESS_PUBLIC``) is turned into ``['Manager', 'Anonymous']``. If no roles are
set, the default return value is ``['Manager']``, though another default can be
supplied as the optional last parameter to ``getRoles()``.

``setRoles()`` will set the
mangled permission name as an instance variable on the object (or delete the
variable, if setting to an empty list of roles). Next, it will
ensure no other ``__roles__`` or ``<name>__roles__`` *instance* variables have
been set (class variables are left alone, of course), so that the managled
permission name attribute is the unambiguous statement of the permission-to-
role mapping.

Note that for both ``getRoles()`` and ``setRoles()``, the difference between
a tuple (don't acquire roles) and a list (do acquire) is significant, and
preserved.

``setRole()`` is used to manage a single role. It takes a role name and a
boolean to decide whether the role should be set or not. It simply builds the
appropriate list or tuple based on the current value of ``getRoles()`` and then
calls ``setRoles()``.

In most cases, it is easier to use the API provided by
``AccessControl.rolemanager.RoleManager`` to manipulate roles in a particular
context, rather than using ``Permission`` directly. This class, usually via the
more specific ``OFS.roles.RoleManager``, is a mixin to most persistent objects
in Zope. It contains a number of relevant methods:

.. In the following definition, s/inheritance/acquisition/ ?

``ac_inherited_permissions(all=0)``
  Returns a list of permissions applicable to this class, but not defined on
  this class directly, by walking the ``__bases__`` of the class. (Note that
  this is not inheritance in the persistent acquisition sense!). If ``all`` is set
  to a truth value, the permissions on this class are included as well. The
  return value is an ``__ac_permissions__``-like tuple of tuples. For inherited
  permissions, the attribute list of each permission entry will be an empty
  tuple.
``permission_settings(permission=None)``
  Returns the settings for a single permission or all permissions, returning a list of
  dicts. Used mainly by ZMI screens.
``manage_role(role, permissions=[])``
  Uses the ``Permission`` API to grant the role to the permissions passed in,
  and take it away from any other permissions where the role may be set.
``manage_acquiredPermissions(permissions=[])``
  Uses the ``Permission`` API to set the roles lists for each of the passed-in
  permissions to a list (acquire), and for all other permissions to a tuple
  (don't acquire).
``manage_permission(permission, roles=[], acquire=0)``
  Uses the ``Permission`` API to set roles for the given permission to either a
  tuple or list (it does not matter what type of sequence the ``roles``
  parameter contains, the ``acquire`` parameter is used), but only if the
  permission is known to this object.
``permissionsOfRole(role)``
  Uses the ``Permission`` API to get the permissions of the given role. Returns
  a list of dicts with keys ``name`` and ``selected`` (set to either an empty
  string or the string ``SELECTED``).
``rolesOfPermission(permission)``
  The inverse of ``permissionsOfRole()``, returning a similar data structure.
``acquiredRolesAreUsedBy(permission)``
  Returns either ``CHECKED`` or an empty string, depending on whether the roles
  sequence of the given permission is a list or tuple.

The use of the strings ``CHECKED`` or ``SELECTED`` as booleans is an unfortunate
side-effect of these methods being used quite literally by ZMI templates.

Global and local roles
======================

The list of known (valid) roles in any context is set in the attribute
``__ac_roles__``. On the initialisation of the application root during startup,
in ``install_required_roles()`` in ``OFS.Application.AppInitializer``, this is
made to include at least ``Owner`` and ``Authenticated``. The ``RoleManager``
base class sets it as a class variable with the value
``('Manager', 'Owner', 'Anonymous', 'Authenticated')``.

In ``AccessControl.rolemanager.RoleManager``, the method ``valid_roles()`` can
be used to obtain the list of valid roles in any given context. It will also
include roles from any parent objects referenced via a ``__parent__``
attribute.

User-defined roles can be set through the ZMI or the method ``_addRole()`` in
the ``OFS.roles.RoleManager`` specialisation, which simply manipulates the
``__ac_roles__`` tuple as an instance variable. There is also ``_delRoles()`` to
delete roles. The method ``userdefined_roles()`` on the base
``AccessControl.rolemanager.RoleManager`` class will return a list of all roles
that were set as instance variables rather than class variables.

The global roles of a given user is determined by the ``getRoles()`` function
on the user object (see the description of the ``allowed()`` method above).
The default ``ZODBRoleManager`` plugin for PAS stores a mapping of users and
roles persistently in the ZODB, though other implementations are possible, e.g.
querying an LDAP repository.

Users may also have local roles, granted in a particular container and its
children. These can be discovered for a given user most easily by calling the
``getRolesInContext()`` function on a user object, which takes a context object
as a parameter.

Local roles are stored in the instance variable ``__ac_local_roles__``. This may
be a dictionary or a callable that returns a dictionary, containing a mapping of user (or
group) ids to local roles granted. The local role check is performed iteratively
by walking up the acquisition chain and checking the instances of bound methods,
until the root of the acquisition chain is reached.

The API to manage local role assignments in a given context is found in
``AccessControl.rolemanager.RoleManager``, through the following methods:

``get_local_roles()``
  Return a tuple of local roles, each represented as a tuple of user ids and
  a tuple of local roles for that user id. With PAS, this may also include
  group ids.
``users_with_local_role(role)``
  Inspect ``__ac_local_roles__`` to get a list of all users with the given local
  role.
``get_local_roles_for_userid(userid)``
  Inspect ``__ac_local_roles__`` to get a tuple of all local roles for the given
  user id.
``manage_addLocalRoles(userid, roles)``
  Modify ``__ac_local_roles__`` to add the given roles to the given user id. Any
  existing roles are kept.
``manage_setLocalRoles(userid, roles)``
  Modify ``__ac_local_roles__`` to add the given roles to the given user id. Any
  existing roles are replaced.
``manage_delLocalRoles(userids)``
  Remove all local roles for the given user ids.

Emergency users
===============

On startup, at import time of ``AccessControl.users``, the function
``readUserAccessFile()`` is called to look for a file called ``accesss`` in the
Zope ``INSTANCE_HOME`` (an environment variable) directory. If found, it reads
the first line and parses it to return a tuple ``(name, password, domains,
remote_user_mode,)``.

If set, the module variable ``emergency_user`` is set to an
``UnrestrictedUser``, a special type of user where the ``allowed()`` method
always returns true. If not, it is set to a ``NullUnrestrictedUser``, which
acts in reverse and disallows everything.

The user folder implementations in ``AccessControl`` and PAS make specific
checks for this user during authentication and permission validation to ensure
this user can always log in and has virtually any permission, with the exception
of ``_what_not_even_god_should_do`` (``ACCESS_NONE``).

.. |---| unicode:: U+02014 .. em dash
