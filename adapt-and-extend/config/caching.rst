=======
Caching
=======


.. figure:: ../../_static/caching-setup.png
   :align: center
   :alt: caching configuration


**Caching** is the process where information is kept in a temporary store, to deliver it to the visitor more quickly.

It is always a balancing act between the 'freshness' of the content, and speed of display.

Enabling caching here within Plone is highly recommended, but fine-tuning it can be more of an art than a science.

Plone comes with a fairly conservative, but highly effective set of defaults.
Importing those settings is your best course of action in almost all cases.

Plone's internal caching works even better when used together with an external cache, such as `Varnish <https://varnish-cache.org/>`_.

See the :doc:`Guide to caching </manage/deploying/caching/index>` for more information.
