===========
Expressions
===========

.. admonition:: Description

    Expressions are string templates or Python expressions which are used in various places in Plone for templates,
    action conditions and URL generation.


Introduction
============

Expressions are part of :term:`TAL`, the Template Attribute Language.
They are used in Zope Page Templates (:term:`ZPT`) and as part of workflow definitions, among other things.

You might want to use expressions in your own add-on product to provide user-written conditions for viewlet visibility,
portlets, dynamic text, etc.

The authoritative reference is `Appendix C: Zope Page Templates Reference <http://docs.zope.org/zope2/zope2book/AppendixC.html>`_
of the `Zope 2 Book <http://docs.zope.org/zope2/zope2book/index.html>`_

Expressions are used in:

* the ``tal:condition``, ``tal:content``, ``tal:replace``,
  ``tal:attribute``, ``tal:define`` :term:`TAL` directives;

* ``portal_css``, ``portal_javascript`` and other resource managers, to
  express when a resource should be included or not;

* ``portal_actions`` to define when content, site and user actions are
  visible.

Expression types
================

There are three main categories of expressions.

Expression can contain an optional ``protocol:`` prefix
to determine the expression type.

path expression (default)
--------------------------

Unless you specify an expression type using ``python:`` or ``string:``
notation,
a `path expression <http://docs.zope.org/zope2/zope2book/AppendixC.html#tales-path-expressions>`_
is assumed.

Path expressions use slashes for traversal
(:doc:`traversing <../serving/traversing>`),
and will implicitly call callables.

Example: call the ``Title()`` method on the ``context`` object
(finding it by :term:`acquisition` if necessary)
and return its value::

    context/Title

Variables can be included using ``?``.
Example: access a folder using the id stored in the ``myItemId`` variable,
and return its title::

    context/?myItemId/Title

.. Note::

    With this kind of usage, if the variable you're dereferencing isn't
    sanitized, there could be security ramifications. Use
    ``python:restrictedTraverse()`` instead if you need to use
    variables in your path parts.

__call__() and nocall: behavior in TAL path traversing
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The TAL path expression will call Python callable objects by default.

If you try to get a hold of a :doc:`helper view </develop/plone/views/browserviews>` like this::

     tal:define="commentsView context/@@comments_view"

You might get this exception::

      Module zope.tales.expressions, line 217, in __call__
      Module Products.PageTemplates.Expressions, line 155, in _eval
      Module Products.PageTemplates.Expressions, line 117, in render
      Module Products.Five.browser.metaconfigure, line 476, in __call__
    AttributeError: 'coments_view' object has no attribute 'index'

It basically means that your view does not have a template assigned
and the traversing logic tries to render that template.

This happens because

1) `` context/@@comments_view`` creates a view instance

2) then calls its ``__call__()`` method

3) the default ``BrowserView.__call__()``  behavior  to render a template by doing::

    def __call__(self):
        return self.index()

4) Because your view does not have a template assigned it also lacks self.index attribute

The workaround for cases like this is to use ``nocall::`` traversing::

     tal:define="commentsView nocall:context/@@comments_view"


``string:`` expressions
-------------------------

Do string replace operation.

Example::

        string:${context/portal_url}/@@my_view_name

``python:`` expression
------------------------

Evaluate as Python code.

Example::

    python:object.myFunction() == False


Expression variables
==============================

Available expression variables are defined in ``CMFCore/Expressions.py``::

    data = {
        'object_url':   object_url,
        'folder_url':   folder.absolute_url(),
        'portal_url':   portal.absolute_url(),
        'object':       object,
        'folder':       folder,
        'portal':       portal,
        'nothing':      None,
        'request':      getattr(portal, 'REQUEST', None),
        'modules':      SecureModuleImporter,
        'member':       member,
        'here':         object,
        }

You can also access :doc:`helper views </develop/plone/misc/context>` directly by name.

Using expressions in your own code
===================================

Expressions are persistent objects. You usually
want to attach them to something, but this is not necessary.

Example::

    from Products.CMFCore.Expression import Expression, getExprContext

    # Create a sample expression - usually this is taken from
    # the user input
    expression = Expression("python:context.Title() == 'foo')

    expression_context = getExprContext(self.context)

    # Evaluate expression by calling
    # Expression.__call__(). This
    # will return whatever value expression evaluation gives
    value = expression(expression_context)

    if value.strip() == "":
        # Usually empty expression field means that
        # expression should be True
        value = True

    if value:
        # Expression succeeded
        pass
    else:
        pass


Custom expression using a helper view
=====================================

If you need to add complex Python code to your expression conditions
it is best to put this code in a BrowserView
and expose it as a method.

Then you can call the method on a view from a TALES expression::

    object/@@my_view_name/my_method

Your view code would look like::

    class MyViewName(BrowserView):
        """ Exposes methods for expression conditions """

        def my_method(self):
            """ Funky condition

            self.context = object for which this view was traversed
            """
            if self.context.Title().startswith("a"):
                return True
            else:
                return False

Register the view as "my_view_name", using ``configure.zcml`` as usual.

You can use context interfaces like

* ``Products.CMFCore.interfaces.IContentish``

*  ``zope.interface.Interface`` (or ``*``)

to make sure that this view is available on all content objects,
as TALES will be evaluated on every page,
depending on what kind of content the page will present.

Expression examples
===================

Get current language
--------------------

Use :doc:`IPortalState context helper </develop/plone/misc/context>` view.

Example how to generate a multilingual-aware RSS feed link::

    string:${object/@@plone_portal_state/portal_url}/site-feed/RSS?set_language=${object/@@plone_portal_state/language}

... or you can use a Python expression for comparison::

    python:object.restrictedTraverse('@@plone_portal_state').language() == 'fi'

Check current language in TAL page template
----------------------------------------------

For example, in case you need to generate HTML such as links
conditionally, depending on the current language:

Example:

.. code-block:: html

    <a tal:define="language context/@@plone_portal_state/language" tal:condition="python: language == 'fi'"
           href="http://www.fi">Finnish link</a>

Example to have different footers (or something similar)
for different languages:

.. code-block:: html

    <div tal:replace="structure context/footertext"
        tal:condition="python:context.restrictedTraverse('@@plone_portal_state').language() == 'no'" />
    <div tal:replace="structure context/footertexteng"
        tal:condition="python:context.restrictedTraverse('@@plone_portal_state').language() == 'en'" />


Check if object implements an interface
--------------------------------------------

Example::

    python:context.restrictedTraverse('@@plone_interface_info').provides('Products.CMFCore.interfaces.IFolderish')

Returns ``True`` or ``False``. Useful for actions.

Check if a certain hostname was used for HTTP request
--------------------------------------------------------

Example::

    python:"localhost" in request.environ.get("HTTP_HOST", "")


Check if the object is a certain content type
----------------------------------------------

Example::

    python:getattr(object, "portal_type", "") == "Custom GeoLocation"


Get portal description
----------------------

Example::

    tal:define="
            portal context/portal_url/getPortalObject;
            portal_description portal/Description"

Doing <input CHECKED> and boolean like HTML attributes in TAL
------------------------------------------------------------------------------------

To have a value appear in TAL or not you can do::

   <input type="checkbox" tal:attributes="checked python:'checked' if MYCONDITION else ''" />

We execute a Python snippet which

* We will dynamically create a *checked* attribute on `<input>` based on Python evaluation

* Return "checked" string if some condition we check in Python evaluates to True

* Otherwise we return an empty string and TAL won't output this attribute (TODO: has TAL some special support for
  CHECKED and SELECTED attributes)

.. note::

    Python 2.6, Plone 4+ syntax



Through-the-web scripts
========================

.. todo::

   Move TTW script info to its own chapter.

The Management Interface allows one to create, edit and execute :doc:`RestrictedPython sandboxed scripts </develop/plone/security/sandboxing>`
directly through the web management interface.
This functionality is generally discouraged nowadays in the favor of :doc:`view classes </develop/plone/views/browserviews>`.

Creating a TTW Python script in an add-on installer
-----------------------------------------------------

Here is an example of how one can pre-seed a Python script in
an add-on installer :doc:`GenericSetup profile </develop/addons/components/genericsetup>`.

``setuphandlers.py``::

    from Products.PythonScripts.PythonScript import manage_addPythonScript

    DEFAULT_REDIRECT_PY_CONTENT = """
    if port not in (80, 443):
        # Don't kick in HTTP/HTTPS redirects if the site
        # is directly being accessed from a Zope front-end port
        return None
    """

    def runCustomInstallerCode(site):
        """ Run custom add-on product installation code to modify Plone site object and others

        Python scripts can be created by Products.PythonScripts.PythonScript.manage_addPythonScript

        http://svn.zope.org/Products.PythonScripts/trunk/src/Products/PythonScripts/PythonScript.py?rev=114513&view=auto

        @param site: Plone site
        """

        # Create the script in the site root
        id = "redirect_handler"

        # Don't override the existing installation
        if not id in site.objectIds():
            manage_addPythonScript(site, id)
            script = site[id]

            # Define the script parameters
            parameters = "url, port"

            script.ZPythonScript_edit(parameters, DEFAULT_REDIRECT_PY_CONTENT)


    def setupVarious(context):
        """
        @param context: Products.GenericSetup.context.DirectoryImportContext instance
        """

        # We check from our GenericSetup context whether we are running
        # add-on installation for your product or any other proudct
        if context.readDataFile('collective.scriptedredirect.marker.txt') is None:
            # Not our add-on
            return

        portal = context.getSite()

        runCustomInstallerCode(portal)

See `the full example <https://github.com/collective/collective.scriptedredirect/>`_.

Dynamically hiding content menu items
----------------------------------------

* http://blog.affinitic.be/2013/03/04/filter-menu-using-a-grok-view/

