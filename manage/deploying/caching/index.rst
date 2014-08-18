================
Guide to Caching
================

.. admonition:: Description

    Caching strategies to improve performance.

    This guide particularly focuses on
    `Unix-like <https://en.wikipedia.org/wiki/Unix-like>`_ environments,
    though the stack discussion may be useful to everyone.


Any dynamicly generated website with a non-trivial number of visitors, will benefit from ``caching``, where resources (like text, images, CSS, javascripts) that are used for multiple visitors are stored in a way that is really fast to retrieve, so that the (often complicated) back-end server doesn't have to generate those resources for every visitor.

Plone is no exception to that. 
Caching in Plone is a two-step process for most larger sites.
There is an add-on called ``plone.app.caching`` that is shipped with Plone since version 4.1. 
On its own, it will already speed up response time quite dramatically.
You simply have to enable it, use the default values provided, and you will have a faster site.

But plone.app.caching works even better together with a dedicated front-end cache, a program that is specialized in doing this work.
These days, the favourite and recommended program for that is called "Varnish".

Here, you will find documentation on both. Remember, they work best together.

.. toctree::
    :maxdepth: 2

    /external/plone.app.caching/docs/index


    

.. toctree::
    :maxdepth: 2

    varnish