==============================
 Python Imaging Library (PIL)
==============================

Plone uses internally  Python Imaging Library (PIL)
for low level image manipulation and decoding.

Installing PIL
--------------

This concerns only UNIXes as Windows installer comes with
PIL binaries.

* http://www.koansys.com/tech/install-plone-with-zopeskel-buildout-needs-pil

* http://blog.twinapex.fi/2009/11/19/installing-python-imaging-library-pil-under-virtualenv-or-buildout/

* http://destefano.wordpress.com/2008/03/18/zope-buildouts-for-plone-on-os-x-heaven-or-hell/

* PIL has libjpeg as a dependency and you need to install it using
  your operating system package manager. On OSX
  you can use `macports <http://www.macports.org/>`_.

* Make sure that you don't have PIL without libjpeg
  support in your system-wide Python setup

Installing libjpeg on OS X
^^^^^^^^^^^^^^^^^^^^^^^^^^

Get http://www.ijg.org/files/jpegsrc.v7.tar.gz, and then::

    tar zxvf jpegsrc.v7.tar.gz
    cd jpeg-7
    cp /usr/share/libtool/config.sub .
    cp /usr/share/libtool/config.guess .
    ./configure --enable-shared --enable-static
    sudo make

Then you can install PIL with JPEG support.

Pillow
------

In late 2010, a packaging fork called `Pillow`_ was created to offer better multi-OS installation support. Specifically it offers:

- Setuptools compatibility
- Hosting (and mirroring) by PyPI (vs. off site)
- Windows eggs
- Bug fixes (many of which simply add vendor-specific library directories to the compiler's search path.)

As a result, PIL can now be installed on many more systems simply by using the "Pillow" package name. E.g.::

  $ easy_install Pillow

Or::

  $ pip install Pillow

Or add to the list of eggs in your Buildout.

.. _`Pillow`: http://pypi.python.org/pypi/Pillow

