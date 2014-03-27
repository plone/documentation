Global Template Variables
=========================

Plone defines a few useful global variables to use them in your
templates

Note: This page covers the methods for referencing variables for Plone
3. It has changed slightly for Plone 4 (see
https://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/no-more-global-definitions-in-templates/)

While writing templates for Plone, you will notice a set of variables
you use more often, like the URL of the portal or the currently
authenticated member.

For your convenience, Plone defines a few global template variables that
are pulled into main\_template via global\_defines. Some of the most
useful ones are:

portal
    The portal object.
portal\_url
    The url of the portal.
member
    The current user (``None`` if user is anonymous)
checkPermission
    A function to check if the current user has a certain permission in
    the current context, e.g.
    ``checkPermission('View portal content', context)``.
isAnon
    True if the current user is not logged in.
is\_editable
    True if the current user has edit permissions in the context.
default\_language
    The default language of the portal.
here\_url
    The URL of the current object.

To see the full list list of these variables, see `the docstring for
``globalize()`` in the interface
``Products.CMFPlone.browser.interfaces.IPlone`` <http://dev.plone.org/plone/browser/Plone/branches/3.2/Products/CMFPlone/browser/interfaces.py#L199>`_.
