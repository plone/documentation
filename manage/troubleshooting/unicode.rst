================================
 Unicode encoding and decoding
================================


Introduction: Why unicode is difficult?
=========================================

Python 2.x does not make a clear distinction between:

* 8-bit strings (byte data)
* 16-bit unicode strings (character data)

Developers use these two formats interchangeably, because it is so easy and
Python does not warn you about this.

However, it will only work as long as the input does not encounter any
international, non-ASCII, characters.  When 8-bit encoded string data and
16-bit raw Unicode string data gets mixed up, by being run through encoding
first, really nasty things start to happen.

Read more:


* http://evanjones.ca/python-utf8.html

safe_unicode()
=====================

Plone's core contains a helper function which allows you
to safely decode strings to unicode without fear of UnicodeDecodeException.
Use this in your own code to decode unicode in the cases you are
not sure if the input is 8-bit bytestrings or real unicode strings.

https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/utils.py#L434

Example::

     # -*- coding: utf-8 -*-

     from Products.CMFPlone.utils import safe_unicode


     foobar = safe_unicode("Ärrinmurrin taas on Plonea joku jättänyt dokumentoimatta")


sys.setdefaultencoding()
=========================

Python has a **system-wide** setting to enforce encoding of all unicode
input automatically to utf-8 when used as 8-bit string.

.. warning::

    This is a wrong way to fix things and it will break other things.
    You have been warned.

* http://tarekziade.wordpress.com/2008/01/08/syssetdefaultencoding-is-evil/

There is also ``sitecustomization.py`` trick to set ``sys.setdefaultencoding("utf-8")`` on per-script basis

* http://stackoverflow.com/a/7892892/315168

UnicodeEncodeError
==================

``UnicodeEncodeError``: 'ascii' codec can't encode character u'\xe4' in position 4: ordinal not in range(128)

This is usually because you are trying to output/store unicode data using
outdated methods, e.g.

* printing,
* logging,
* using 7-bit ids ...

Instead of::

    print foo

do::

    print foo.encode("utf-8") # You are sure this is a unicode string

Filtering example::

    def safe_print(x):
        """ Do not die on bad input when doing debug prints """
        if type(x) == str:
            print x
        else:
            print x.decode("utf-8")


UnicodeDecodeError
==================

* http://wiki.python.org/moin/UnicodeDecodeError



* http://pyref.infogami.com/__unicode__

Infamous non-breaking Unicode space \\xa0
============================================

Press CTRL+space / AltGr space on Linux to accidentally create it.

**You can't see it.** But it breaks everything.

How to fix
----------

Example to how to fix non-breaking space characters which have ended up
in reStructuredText ``.txt`` files.  This is Unicode character code A0.

Example fix_wtf_space.py::

    # -*- coding: utf-8 -*-
    """ Fix non-breaking space characters which have ended up to reST
        .txt files.  This is Unicode character code A0.

        Press CTRL+space / AltGr space on Linux to accidentally create it.

        E.g. as a sympton the following exception is raised if you try
        to upload Python egg::

          File "/Library/Python/2.6/site-packages/docutils-0.6-py2.6.egg/docutils/parsers/rst/states.py", line 2621, in blank
            self.parent += self.literal_block()
          File "/Library/Python/2.6/site-packages/docutils-0.6-py2.6.egg/docutils/parsers/rst/states.py", line 2712, in literal_block
            literal_block = nodes.literal_block(data, data)
          File "/Library/Python/2.6/site-packages/docutils-0.6-py2.6.egg/docutils/nodes.py", line 810, in __init__
            TextElement.__init__(self, rawsource, text, *children, **attributes)
          File "/Library/Python/2.6/site-packages/docutils-0.6-py2.6.egg/docutils/nodes.py", line 798, in __init__
            textnode = Text(text)
          File "/Library/Python/2.6/site-packages/docutils-0.6-py2.6.egg/docutils/nodes.py", line 331, in __new__
            return reprunicode.__new__(cls, data)
        UnicodeDecodeError: 'ascii' codec can't decode byte 0xc2 in position 715: ordinal not in range(128)
    """

    import os

    def fix(name):
        """ Fix a single .txt file
        """
        input = open(name, "rt")
        text = input.read()
        input.close()
        text = text.decode("utf-8")

        # Show if we get bad hits
        for c in text:
            if c == u"\xa0":
                print "Ufff"

        text = text.replace(u"\xa0", u" ")
        text = text.encode("utf-8")

        output = open(name, "wt")
        output.write(text)
        output.close()


    # Process all .txt files in the
    # current folder
    for f in os.listdir(os.getcwd()):
        if f.endswith(".txt"):
            fix(f)

