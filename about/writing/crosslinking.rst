====================================================================
 Embedded external manuals
====================================================================

.. admonition:: Description

    How to get your Plone package documentation into
    collective-docs.

.. highlight:: console

Introduction
=======================

The audience of this documentation are Plone developers
who are writing Plone core Python packages.

collective.developermanual has a section *Reference manuals*

* You can pull in manuals to this section from external packages

* Then these manuals can be cross-references in the other documentation

* All documentation is one place to be found for the fellow peer developers

* Manuals will be hosted under *developer.plone.org* domain

Benefits of having the documentation in developer.plone.org
================================================================

The main benefit of having your manual in *developer.plone.org*
instead of a custom readthedocs.org account include

* Better co-developer user experience (all manuals in one place searchable).
  Your manual can be cross-referenced from collective-docs.

* Unified documentation theme with usability features like
  edit backlinks

* Documentation team can keep an eye on you:
  *#plone-docs* IRC channel will get Travis CI notifications on Sphinx
  syntax failures (please join in on the channel)

* *Plone AI team* has shared rtd.org account in the case we have a person
  missing-in-action

Disadvantages include

* *readthedocs.org* does not notice changes in your documentation and
  thus builds must be triggered manualy. However collective-docs
  is build frequently so the lag should be maximum of 24 hours or so

* More complex Sphinx ``conf.py`` with all sort of trickery to pull this
  all together

Steps to embed a reference manual in collective-docs
=======================================================

Add your egg to ``[sources]`` and ``auto-checkout`` in ``buildout.cfg``.

Add directory mapping the Sphinx documentation inside that egg at the top of ``conf.py``.

Add a reference in ``source/index.rst`` to point your master ``index.rst``.

Then run Sphinx::

    bin/buildout
    make html

See Sphinx ouput for warnings and errors.

See that your manual gets correctly added in the index::

    open build/html/index.html

``conf.py`` creates symlinks in ``source/reference_manuals/external``. If you manage
to mess them reset the situation with the command::

    rm source/reference_manuals/external/*

developer.plone.org builds
================================================

``developer.plone.org`` documentation builds are
done on *deus2.plone.org* machine in ``/var/www/developer.plone.org``
folder. They are done by running
`doc-holliday.sh update script <https://github.com/collective/collective.developermanual/blob/master/doc-holliday.sh>`_ in a crontab created by *deployment.cfg*.

Update
-------

Do run the build by hand and see what's going wrong::

    ssh deus2.plone.org
    cd /var/www/developer.plone.org
    sudo -u apache bin/buildout -c deployment.cfg
    sudo -u apache ./doc-holliday.sh --force

Something like this is occasionally needed to clear up things changed in external packages::

    cd src/diazo/
    sudo -u apache git pull

Setup
------

The deployment is done as following::

    sudo -i
    mkdir /var/www/developer.plone.org
    chown apache:apache
    /var/www/developer.plone.org
    cd /var/www
    sudo -u apache git clone git://github.com/collective/collective.developermanual.git developer.plone.org
    cd developer.plone.org
    sudo -u apache virtualenv venv
    sudo -u apache venv/bin/python bootstrap.py
    sudo -u apache bin/buildout -c deployment.cfg

The folder where final static HTML files lie is ``/var/www/developer.plone.org/var/public_html``.






