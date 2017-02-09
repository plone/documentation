======================
Breadcrumbs (path bar)
======================

.. admonition:: Description

    Breadcrumbs is visual element showing where the user is on the site.
    This document shows some example code how to create breadcrumbs
    programmatically.


Navigation level sensitive breadcrumbs
=======================================

Below is a breadcrumbs viewlet displayed only on 3rd navigation level
downwards.  Drop this in `your add-on template
<https://github.com/miohtama/sane_plone_addon_template>`_.
Tune the ``visible()`` function for further functionality.

Python code to be dropped in ``viewlets.py``::

    from plone.app.layout.viewlets.interfaces import IAboveContent


    class Breadcrumbs(grok.Viewlet):
        """ Breadcrumbs override which are only displayed on 2nd level and forward (not on Home screen)
        """

        # Override standard Plone breadcrumbs
        grok.name("plone.path_bar")
        grok.viewletmanager(IAboveContent)

        def visible(self):
            """ Called by template condition. """

            # Note that "Home" does not count as a crumb
            return len(self.breadcrumbs) >= 1

        def update(self):
            context= self.context.aq_inner

            self.portal_state = getMultiAdapter((context, self.request), name="plone_portal_state")
            self.site_url = self.portal_state.portal_url()
            self.navigation_root_url = self.portal_state.navigation_root_url()

            breadcrumbs_view = getMultiAdapter((context, self.request), name='breadcrumbs_view')
            self.breadcrumbs = breadcrumbs_view.breadcrumbs()

            # right-to-left reading order
            self.is_rtl = self.portal_state.is_rtl()

Template code ``templates/breadcrumbs.pt``:

.. code-block:: html

    <div id="portal-breadcrumbs"
         i18n:domain="plone"
         tal:condition="viewlet/visible"
         tal:define="breadcrumbs viewlet/breadcrumbs;
                     is_rtl viewlet/is_rtl">

        <span id="breadcrumbs-home">
            <a i18n:translate="tabs_home"
               tal:attributes="href viewlet/navigation_root_url">Home</a>
            <span tal:condition="breadcrumbs" class="breadcrumbSeparator">
                <tal:ltr condition="not: is_rtl">|</tal:ltr>
                <tal:rtl condition="is_rtl">|</tal:rtl>
            </span>
        </span>
        <span tal:repeat="crumb breadcrumbs"
              tal:attributes="dir python:is_rtl and 'rtl' or 'ltr';
                              id string:breadcrumbs-${repeat/crumb/number}">
            <tal:item tal:define="is_last repeat/crumb/end;
                                  url crumb/absolute_url;
                                  title crumb/Title">
                <a href="#"
                   tal:omit-tag="not: url"
                   tal:condition="python:not is_last"
                   tal:attributes="href url"
                   tal:content="title">
                    crumb
                </a>
                <span class="breadcrumbSeparator" tal:condition="not: is_last">
                    <tal:ltr condition="not: is_rtl">|</tal:ltr>
                    <tal:rtl condition="is_rtl">|</tal:rtl>
                </span>
                <span id="breadcrumbs-current"
                      tal:condition="is_last"
                      tal:content="title">crumb</span>
             </tal:item>
        </span>

    </div>


Back button
============

Below is an example how we have extracted information like the parent
container and such from breadcrumbs.

.. Note::

    We need special dealing for "default view" of objects... that's
    the canonical part.

.. code-block:: python

    class Back(grok.Viewlet):
        """ Back button
        """

        def update(self):
            context= aq_inner(self.context)

            context_helper = getMultiAdapter((context, self.request), name="plone_context_state")

            portal_helper = getMultiAdapter((context, self.request), name="plone_portal_state")

            canonical = context_helper.canonical_object()

            parent = aq_parent(canonical)

            breadcrumbs_view = getView(self.context, self.request, 'breadcrumbs_view')
            breadcrumbs = breadcrumbs_view.breadcrumbs()

            if (len(breadcrumbs)==1):
                self.backTitle = _(u"Home")
            else:
                if hasattr(parent, "Title"):
                    self.backTitle = parent.Title()
                else:
                    self.backTitle = _(u"Back")

            if hasattr(parent, "absolute_url"):
                self.backUrl = parent.absolute_url()
            else:
                self.backUrl = portal_helper.portal_url()

            self.isHome = len(breadcrumbs)==0


More info

* http://code.google.com/p/plonegomobile/source/browse/gomobiletheme.basic/trunk/gomobiletheme/basic/viewlets.py#281
