===
ZCML
====

.. admonition:: Description

    What Plone programmers should know about ZCML.



Introduction
============

:term:`ZCML` stands for the *Zope Configuration Mark-up Language*.  It is an
XML-based language used to extend and plug into systems based on the Zope
Component Architecture (:term:`ZCA`).

It provides:

* conflict resolution (e.g. two plug-ins cannot overlap);
* extensible syntax based on namespaces.

Downsides of ZCML are:

* it is cumbersome to write by hand;
* lack of end-user documentation.

Plone uses ZCML to:

* register components with various places in the system, both core and
  add-ons.

.. note::

    Everything you can do in ZCML can also be done in Python code.


More info:

* `ZCML reference <http://docs.zope.org/zope3/ZCML/@@staticmenu.html>`_ (does not include Plone specific directives)

* http://docs.zope.org/zopetoolkit/codingstyle/zcml-style.html

ZCML workflow
==============

Each Plone component (core, add-on) has a base ``configure.zcml`` in the
package root.  This :term:`ZCML` file can include additional nested
configuration files using the ``<include>`` directive.

* ZCML is always interpreted during Plone start-up.

* Your :doc:`unit test </develop/testing/unit_testing>` may need to
  manually include ZCML.

* :doc:`Funny exception error messages occur if Plone is started in the
  production mode and ZCML was not properly read for all the packages
  </manage/troubleshooting/exceptions>`

When Plone is started all ZCML files are read.

* New way: Python egg ``setup.py`` file contains a
  `autoinclude <https://plone.org/products/plone/roadmap/247>`_
  hint and is picked up automatically when all the packages are scanned.

* Old way: ZCML reference must be manually added to the ``zcml = section``
  in ``buildout.cfg``

If ZCML contains errors
:doc:`Plone does not start up in the foreground </manage/troubleshooting/basic>`

Overrides
==========

Besides layer overrides, ZCML provides more hardcore
ways to override things in buildout.
These overrides can also override utilities etc. and overrides take effect
during ZCML parsing, not when site is run.

* Create ``overrides.zcml`` file in your egg to the same folder as ``configure.zcml``

* Syntax is 100% same as in ``configure.zcml``

* Restart Plone.

.. Note::

    Before Plone 3.3, ZCML directives could not be automatically picked up from
    eggs. To make Plone pick up the directions in ``overrides.zcml``, you'd
    have to add this line in ``buildout.cfg``::

      zcml =
          ...
          myegg-overrides

    Since Plone 3.3, the ``z3c.autoinclude`` plugin can do this
    (https://plone.org/products/plone/roadmap/247/).


Specify files and code from another package
===========================================

If you ever find yourself needing to use a template
from another package, you can do so with using the
configure tag which will then run the block of :term:`ZCML`
in the context of that package.

Here's an example of overriding the :term:`BrowserView` 'folder_contents'. It
is defined in package ``plone.app.content`` in directory ``browser`` with this
:term:`ZCML` statement::

    <browser:page
        for="Products.CMFCore.interfaces._content.IFolderish"
        class=".folder.FolderContentsView"
        name="folder_contents"
        template="templates/folder_contents.pt"
        permission="cmf.ListFolderContents"
    />

In your own package ``my.package``, you want to override the class, but keep the
template. Assuming you created a class ``MyFolderContentsView`` inside
``foldercontents.py`` in the ``browser`` directory of your package, add this
:term:`ZCML` statement::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="my.package">

      <!-- override folder_contents -->
      <configure package="plone.app.content.browser">
          <browser:page
              for="Products.CMFCore.interfaces._content.IFolderish"
              class="my.package.browser.foldercontents.MyFolderContentsView"
              name="folder_contents"
              template="folder_contents.pt"
              layer="my.package.interfaces.IMyPackageLayer"
              permission="cmf.ListFolderContents"
          />
      </configure>
    </configure>

Basically, you re-define the :term:`BrowserView` in the context of its original
package, so that the relative path to the template stays valid.
But using the full path in dotted notation, you can let it point to your
own class.


Conditionally run ZCML
======================

You can conditionally run :term:`ZCML` if a certain package or feature is
installed.

First, include the namespace at the top of the :term:`ZCML` file::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:zcml="http://namespaces.zope.org/zcml"
        i18n_domain="my.package">
    ....

Examples
--------

Conditionally run ZCML based upon the installation status of a package::

    <include zcml:condition="installed some.package" package=".package" />
    <include zcml:condition="not-installed some.package" package=".otherpackage" />

Conditionally run ZCML based upon the presence of a feature::

    <include zcml:condition="have plone-4" package=".package" />
    <include zcml:condition="not-have plone-4" package=".otherpackage" />

Registering features
--------------------

To register that a feature is present, include the ``xmlns:meta`` namespace at
the top of your :term:`ZCML` file (typically ``meta.zcml`` in a package), and
define a ``<meta:provides>`` element with your feature's name, like so::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:zcml="http://namespaces.zope.org/zcml"
        xmlns:meta="http://namespaces.zope.org/meta">
        ...
        <meta:provides feature="my-feature-name" />
        ...
    </configure>

Once registered, you can now use ``zcml:condition="have my-feature-name"`` to
register ZCML configuration that is requires this feature be available.
