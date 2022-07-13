===============================
Sandboxing and RestrictedPython
===============================

.. admonition:: Description

   Legacy Plone code uses RestrictedPython sandboxing to secure each module and class functions.

Introduction
-------------

Plone has two sandboxing modes

* Unrestricted: Python code is executed normally and the code can access the full Zope application server environment.
  This includes other site instances too.
  This is generally what happens when you write your own add-on and add views for it.

* Restricted (RestrictedPython): scripts and evalutions are specially compiled, have limited Python
  language functionality and every function call is checked against the security manager.
  This is what happens when you try to add Python code or customize page templates through the Management Interface.

Restricted execution is enabled only for **through-the-web** scripts and **legacy code**:

* Old style TAL page templates: everything you put inside page template
  tal:content, tal:condition, etc. These templates are .pt templates
  **without** accomppaning BrowserView

* Script (Python) code is executed (plone_skins layer Python scripts and old style form management)

.. note::

   RestrictedPython was bad idea and mostly causes headache.
   Avoid through-the-web Zope scripts if possible.

For further information, read

* http://plone.293351.n2.nabble.com/Update-was-Plone-4-Chameleon-compatibility-tp5612838p5614466.html

Whitelisting modules for RestrictedPython import
---------------------------------------------------

* https://plone.org/documentation/kb/using-unauthorized-modules-in-scripts

Traversing special cases
-------------------------

Old style Zope object traversing mechanism does not expose

* Functions without docstring (the """ comment at the beginning of the function)

* Functions whose name begins with underscore ("_"-character)

Unit testing RestrictedPython code
-----------------------------------

RestrictedPython_ code is problematic, because RestrictedPython hardening is done on Abstract Syntax Tree level and
effectively means all evaluated code must be available in the source code form. This makes testing RestrictedPython
code little difficult.

Below are few useful unit test functions::

    # Zope security imports
    from AccessControl import getSecurityManager
    from AccessControl.SecurityManagement import newSecurityManager
    from AccessControl.SecurityManagement import noSecurityManager
    from AccessControl.SecurityManager import setSecurityPolicy
    from AccessControl import ZopeGuards
    from AccessControl.ZopeGuards import guarded_getattr, get_safe_globals, safe_builtins
    from AccessControl.ImplPython import ZopeSecurityPolicy
    from AccessControl import Unauthorized

    # Restricted Python imports
    from RestrictedPython import compile_restricted
    from RestrictedPython.SafeMapping import SafeMapping

    def _execUntrusted(self, debug, function_body, **kwargs):
        """ Sets up a sandboxed Python environment with Zope security in place.

        Calls func() in an sandboxed environment. The security mechanism
        should catch all unauthorized function calls (declared
        with a class SecurityManager).

        Security is effective only inside the function itself -
        The function security declarations themselves are ignored.

        @param func: Function object
        @param args: Parameters delivered to func
        @param kwargs: Parameters delivered to func
        @param debug: If True, break into pdb debugger just before evaluation
        @return: Function return value
        """

        # Create global variable environment for the sandbox
        globals = get_safe_globals()
        globals['__builtins__'] = safe_builtins

        # Zope seems to have some hacks with guaded_getattr.
        # guarded_getattr is used to check the permission when the
        # object is being traversed in the restricted code.
        # E.g. this controls function call permissions.
        from AccessControl.ImplPython import guarded_getattr as guarded_getattr_safe
        globals['_getattr_'] = guarded_getattr_safe
        #globals['getattr'] = guarded_getattr_safe
        #globals['guarded_getattr'] = guarded_getattr_safe


        globals.update(kwargs)

        # Our magic code

        # The following will compile the parsed Python code
        # and applies a special AST mutator
        # which will proxy __getattr__ and function calls
        # through guarded_getattr
        code = compile_restricted(function_body, "<string>", "eval")

        # Here is a good place to break in
        # if you need to do some ugly permission debugging
        if debug:
            pass # go pdb here

        return eval(code, globals)

    def execUntrusted(self, func, **kwargs):
        """ Sets up a sandboxed Python environment with Zope security in place. """
        return self._execUntrusted(False, func, **kwargs)

    def execUntrustedDebug(self, func, **kwargs):
        """ Sets up a sandboxed Python debug environment with Zope security in place. """
        return self._execUntrusted(True, func, **kwargs)

    def assertUnauthorized(self, func, **kwargs):
        """ Check that calling func with currently effective roles will raise Unauthroized error. """
        try:
            self.execUntrusted(func, **kwargs)
        except Unauthorized, e:
            return

        raise AssertionError, 'Unauthorized exception was expected'

    def test_xxx(self):
        # Run RestrictedPython in unit test code
        # myCustomUserCreationFunction() is view/Python script/method you must call in the restricted mode
        self.execUntrusted('portal.myCustomUserCreationFunction(username="national_coordinator", email="nationalcoordinator@redinnovation.com")', portal=self.portal)

Other references
----------------

* `zope.security <https://pypi.python.org/pypi/zope.security>`_

.. _AccessControl: http://svn.zope.org/Zope/trunk/src/AccessControl

.. _RestrictedPython: https://pypi.python.org/pypi/RestrictedPython

