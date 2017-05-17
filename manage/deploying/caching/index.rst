================
Guide to Caching
================

.. admonition:: Description

   Caching strategies to improve performance.

   This guide particularly focuses on `Unix-like <https://en.wikipedia.org/wiki/Unix-like>`_ environments,
   though the stack discussion may be useful to everyone.


Any dynamically generated website with a non-trivial number of visitors, will benefit from ``caching``.
Resources (like text, images, CSS, JavaScript) that are used for multiple visitors are stored in a way that
is fast to retrieve, so that the (often complicated) back-end server doesn't have to generate those resources for every visitor.

Plone is no exception to that.
Caching in Plone is a two-step process for most larger sites.

There is an add-on called ``plone.app.caching`` that is shipped with Plone.
On its own, it will already speed up response time quite dramatically.

It is not enabled by default. You must enable it to use it. You can use the default values provided, and you will have a faster site without much effort.

You can also tweak the settings to get better performance. There is always a little trade-off to be made here. So-called "strong" caching will be faster, but it may mean that visitors get older content.

It is usually best to set up "strong" caching for things that don't change often, like CSS and javascript files, and "weak" caching for actual texts.

You can also "invalidate" content automatically when you update a piece of content, so that the front-end server knows it has to get a fresh copy when you edit a piece of content.

But ``plone.app.caching`` works even better together with a dedicated front-end cache, a program that is specialized in doing this work.
These days, the favorite and recommended program for that is called Varnish.



.. toctree::
    :maxdepth: 2

    caching
    varnish4
