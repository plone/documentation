Adding five.grok as a dependency
==================================

**How to install the five.grok package safely**

Assuming you already have a suitable package and a :doc:`buildout </old-reference-manuals/buildout/index>`, using
*five.grok* should be as simple as depending on it in your *setup.py*
file:

::

    install_requires = [
        ...
        'five.grok',
        ]

As shown on the previous page, you probably also want this as a minimum
in your *configure.zcml*:

.. code-block:: xml

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:grok="http://namespaces.zope.org/grok"
               i18n_domain="my.package">

        <include package="five.grok" />
        <grok:grok package="." />

    </configure>

However, if you are using Zope 2.10, you may also need to pin certain
eggs in your *buildout.cfg*. If you are using Dexterity, there are
already part of the “known good set” of packages. Otherwise, see the
`five.grok installation instructions`_ for details.

Naturally, you will need to re-run buildout after editing *setup.py*
and/or *buildout.cfg*.


.. _five.grok installation instructions: https://pypi.python.org/pypi/five.grok
