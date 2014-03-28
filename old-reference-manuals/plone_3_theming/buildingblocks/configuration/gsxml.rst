Generic Setup XML
=================

The language used to define profiles.

The XML used for profile files is straightforward. There's no DTD
available, but there are plenty of examples to reuse or adapt for your
purposes. If all of this seems too much, the good news is that you can
get Generic Setup to write the files for you by exporting the
configuration from an existing site. There's more information on how to
do this on the Generic Setup Tool page.

The root node of an XML profile is usually an object:

::

    <object name="portal_javascripts" meta_type="JavaScripts Registry">
         .......
    </object>

which corresponds to a particular site tool (in this case the
JavaScripts registry). Sub-nodes represent sub-objects and XML
attributes correspond to the attributes of those classes.

::

    <javascript cacheable="True" compression="none" cookable="True"
                enabled="True" expression="" id="jquery.js" inline="False"/>

So, in this case, the sub-node represents an entry in the JavaScripts
registry and its tick boxes.

.. figure:: /old-reference-manuals/plone_3_theming/images/portal_js_snippet.gif
   :align: center
   :alt: screenshot of the javascripts registry in the ZMI

   screenshot of the javascripts registry in the ZMI

In the very unlikely event that you need to work out for yourself what
attributes to use, you'll need to investigate the API (or the interfaces
and classes) of the tool in question. Use
`http://api.plone.org <http://api.plone.org>`_ or dig into the source
code.
