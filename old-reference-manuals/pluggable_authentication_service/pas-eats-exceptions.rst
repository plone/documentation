===================
PAS eats exceptions
===================

.. contents :: :local:

A broken user folder is one of the worst things that can happen in Zope: it can make it impossible to access any objects underneath the user folders level.

In order to secure itself against errors in plugins PAS ignores all exceptions of the common exception types: NameError, AttributeError, KeyError, TypeError and ValueError.

This can make debugging plugins hard: an error in a plugin can be silently ignored if its exception is swallowed by PAS.

Do not swallow
--------------

You can tell PAS not to swallow your exceptions by setting the
``_dont_swallow_my_exceptions`` attribute on the plugin class.

From ``Products/PluggableAuthService/PluggableAuthService.py`` line 86::

    # except if they tell us not to do so
    def reraise(plugin):
        try:
            doreraise = plugin._dont_swallow_my_exceptions
        except AttributeError:
            return
        if doreraise:
            raise

Which means to take advantage of this feature, do something like this in your
plugin class::

    class LoginOnlyOncePlugin(BasePlugin):
        """
        Class methods via Products/PluggableAuthService/interfaces/plugins.py
        """

        meta_type = 'Login Only Once Plugin'
        security = ClassSecurityInfo()
        _dont_swallow_my_exceptions = True

        def __init__(self, id, title=None):
            self._setId(id)
            self.title = title

        ...



