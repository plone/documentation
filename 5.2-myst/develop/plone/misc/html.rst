=====================================
HTML manipulation and transformations
=====================================

.. admonition:: Description

    How to programmatically rewrite HTML in Plone.


Introduction
============

It is recommended to use the `lxml <http://lxml.de/>`_ library
for all HTML DOM manipulation in Python.

Plone is no exception.

Converting HTML to plain text
=============================

The most common use case is to override ``SearchableText()`` to return
HTML content for portal_catalog for indexing.

* http://stackoverflow.com/questions/6956326/custom-searchabletext-and-html-fields-in-plone

Converting plain text to HTML
=============================

You can use ``portal_transforms`` to do plain text -> HTML conversion.

Below is an example how to create a Description field rendered with new line support.


Register the view in ``configure.zcml``:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.dexterityforms">

        ...

        <browser:page
            name="description-helper"
            for="*"
            class=".description.DescriptionHelper"
            permission="zope2.View"
            />

    </configure>


Create a file ``description.py`` and add the following code::

      from plone import api
      from zope.interface import Interface
      from Products.Five.browser import BrowserView


      class DescriptionHelper(BrowserView):
          """
          A helper view which exports dublin core description w/new line support
          allowing several paragraphs in Plone's description field.
          """

          def render(self):
              """
              Get a content item description w/new line support.

              Transform hard lines to breaks in HTML.
              """

              # Call archetypes accessor
              text = self.context.Description()

              # Transform plain text description with ASCII newlines
              # to one with
              portal_transforms = api.portal.get_tool(name='portal_transforms')

              # Output here is a single <p> which contains <br /> for newline
              data = portal_transforms.convertTo('text/html', text, mimetype='text/x-web-intelligent')
              html = data.getData()
              return html

Now you can do in your page template

.. code-block:: html

    <metal:main-macro define-macro="main">

        <div tal:replace="structure provider:plone.abovecontenttitle" />

        <h1 metal:use-macro="here/kss_generic_macros/macros/generic_title_view">
            Title or id
        </h1>

        <div tal:replace="structure provider:plone.belowcontenttitle" />

        <div class="documentDescription">
           <tal:desc replace="structure context/@@description-helper" />
        </div>

        ...


More info

* https://github.com/plone/plone.intelligenttext/tree/master/plone/intelligenttext

Rewriting relative links
==========================

Below is an example which:

* rewrites all relative links of Page content as absolute;
* removes some nasty tags from Page content;
* outputs the folder content and subcontent as one continuous page;

This is suitable for e.g. printing the whole folder in one pass.

Register the view in ``configure.zcml``:

.. code-block:: xml

    <configure
          xmlns="http://namespaces.zope.org/zope"
          xmlns:browser="http://namespaces.zope.org/browser"
          >

        <browser:page
              for="Products.CMFCore.interfaces.IFolderish"
              name="help"
              permission="zope2.View"
              class=".help.Help"
              />

    </configure>

Add the file ``help.py``::

    from lxml import etree
    from StringIO import StringIO
    import urlparse
    from lxml import html

    import zope.interface
    from Products.Five.browser import BrowserView


    def fix_links(content, absolute_prefix):
        """
        Rewrite relative links to be absolute links based on certain URL.

        @param html: HTML snippet as a string
        """

        if type(content) == str:
            content = content.decode("utf-8")

        parser = etree.HTMLParser()

        content = content.strip()

        tree  = html.fragment_fromstring(content, create_parent=True)

        def join(base, url):
            """
            Join relative URL
            """
            if not (url.startswith("/") or "://" in url):
                return urlparse.urljoin(base, url)
            else:
                # Already absolute
                return url

        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            url = join(absolute_prefix, url)
            node.set('src', url)
        for node in tree.xpath('//*[@href]'):
            href = node.get('href')
            url = join(absolute_prefix, href)
            node.set('href', url)

        data =  etree.tostring(tree, pretty_print=False, encoding="utf-8")

        return data

    def remove_bad_tags(content):
        """ Filter out HTML nodes which would prevent continuous printing """


        if type(content) == str:
            content = content.decode("utf-8")

        tree  = html.fragment_fromstring(content, create_parent=True)

        # Title tag in the middle of page causes Firefox to choke and
        # aborts page rendering
        for node in tree.xpath('//title'):
            node.getparent().remove(node)

        data =  etree.tostring(tree, pretty_print=False, encoding="utf-8")

        return data

    class Help(BrowserView):
        """ Render all folder pages and subpages as continuous printable document """


        def update(self):

            objects = []
            # Walk through all objects recursively

            def walk(folder, level):

                for id, object in folder.contentItems():

                    if object.portal_type == "Image":
                        continue

                    # Output pages which have text payload
                    if hasattr(object, "getText"):
                        text = object.getText()
                    else:
                        text = ""

                    objects.append({
                        "object":object,
                        "level":level,
                        # We need to re-map relative links or
                        # they are incorrect in rendered HTML output
                        "text" : remove_bad_tags(fix_links(text, object.absolute_url()))
                    })

                    if object.portal_type == "Folder":
                        walk(object,level+1)


            walk(self.context, 1)

            self.objects = objects

Add the ``help.pt`` template:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          metal:use-macro="context/main_template/macros/master">
    <body>

    <metal:slot metal:fill-slot="content-title" i18n:domain="cmf_default">
      <h1>Site help</h1>

      <p class="discreet">
        Printable versions
      </p>
    </metal:slot>

    <metal:block fill-slot="top_slot" tal:define="dummy python:request.set('disable_border',1)" />

    <metal:slot metal:fill-slot="content-core" i18n:domain="cmf_default">

        <div class="help-all">
            <tal:rep repeat="page view/objects">
                <tal:def define="body page/text|nothing;title page/object/Title;level page/level">

                    <div tal:condition="python:level==1" style="page-break-before:always"><!-- --></div>
                    <h1 tal:condition="python:level==1" tal:content="title" />
                    <h2 tal:condition="python:level==2" tal:content="title" />
                    <h3 tal:condition="python:level>2" tal:content="title" />

                    <div class="help-body">
                        <tal:body tal:replace="structure body" />
                    </div>

                    <div style="clear: both"><!-- --></div>


                </tal:def>
            </tal:rep>
        </div>
    </metal:slot>
    </body>
    </html>
