Resource directories 
=====================

**Exposing static resources such as CSS, JavaScript and image files.**

So far, we have seen how to create views and viewlets. Using views with
a custom *render()* method that sets the *Content-Type* header, we were
able to create files on the fly. We could even use this for binary data.

In may cases, however, we simply want to expose some static files, such
as CSS and JavaScript files, or images and use them in our dynamic
views. Luckily, *five.grok* makes this easy.

When a package is grokked, a grokker will look for a directory inside
the package with the name *static*. This is then available under the
prefix *++resource++<packagename>*, where *<packagename>* is the dotted
name to the package in which the *static* directory is located.

For example, let’s say we had a package called *example.messaging*. The
*static*directory would then be found in *example/messaging/static*,
alongside the Python modules and sub-packages in this package. If this
directory in turn contained a file called *messaging.css*, it would be
accessible on a URL like
*http://example.org/site/++resource++example.messaging/messaging.css.*

.. note::
    If you need to register additional directories, you can do so using the
    *<browser:resourceDirectory />* ZCML directive in *configure.zcml*. This
    requires two attributes: *name* is the name that appears after the
    *++resource++***namespace; *directory* is a relative path to the
    directory containing resources.

Importing CSS and JavaScript files in templates
-----------------------------------------------

One common use of static resources is to add a static CSS or JavaScript
file to a specific template. We can do this by filling the *style\_slot*
or *javascript\_slot* in Plone’s *main\_template* in our own view
template and using an appropriate resource link.

For example, we could add the following in a view using
*main\_template*. Note that this would go outside the block filling the
*master* macro.

::

    <html>

    ...

    <head>
        <metal:block fill-slot="style_slot">
            <link rel="stylesheet" type="text/css" 
                tal:define="navroot context/@@plone_portal_state/navigation_root_url"
                tal:attributes="href string:${navroot}/++resource++example.messaging/messaging.css"
                />
        </metal:block>
    </head>

    ...

    </html>

.. note::
    Always create the resource URL relative to the navigation root as shown
    here, so that the URL is the same for all content objects using this
    view. This allows for efficient resource caching.

Of course, we could use the same technique anywhere else in any other
page template, but the head slots are a good place for CSS and
JavaScript resources.

Registering resources with Plone’s resource registries
------------------------------------------------------

Sometimes it is more appropriate to register a stylesheet with Plone’s
*portal\_css* registry (or a JavaScript file with
*portal\_javascripts*), rather than add the registration on a
per-template basis. This ensures that the resource is available
site-wide.

.. note::
    It may seem wasteful to include a resource that is not be used on all
    pages in the global registry. Remember, however, that *portal\_css* and
    *portal\_javascripts* will merge and compress resources, and set caching
    headers such that browsers and caching proxies can cache resources well.
    It is often more effective to have one slightly larger file that caches
    well, than to have a variable number of files that may need to be loaded
    at different times.

To add a static resource file, you can use the GenericSetup
*cssregistry.xml* or *jsregistry.xml* import steps in the
*profiles/default* directory. For example, an import step to add the
*conference.css* file site-wide may involve a *cssregistry.xml* file
that looks like this:

::

    <?xml version="1.0"?>
    <object name="portal_css">
     <stylesheet id="++resource++example.conference/conference.css"
        title="" cacheable="True" compression="safe" cookable="True"
        enabled="1" expression="" media="screen" rel="stylesheet" rendering="import"
        />
    </object>

Similarly, a JavaScript resource could be imported with a
*jsregistry.xml* like:

::

    <?xml version="1.0"?>
    <object name="portal_javascripts">
     <javascript cacheable="True" compression="none" cookable="True"
        enabled="False" expression=""
        id="++resource++example.conference/conference.js" inline="False"/>
    </object>

Image resources
---------------

Images can be added to resource directories just like any other type of
resource. To use the image in a view, you can construct an *<img />* tag
like this:

::

    <img style="float: left; margin-right: 2px; margin-top: 2px"
         tal:define="navroot context/@@plone_portal_state/navigation_root_url"
         tal:attributes="src string:${navroot}/++resource++example.conference/program.gif"
         />


