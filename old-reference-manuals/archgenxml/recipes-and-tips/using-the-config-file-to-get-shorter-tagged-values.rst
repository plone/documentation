==================================================
Using the config file to get shorter tagged values
==================================================

.. contents :: :local:

.. admonition:: Description

    Some tagged values can get quite lengthy. If you use such a lengthy value a
    few times, you can store it in your project's config file.

An example of long tagged values are the permissions you set on workflow
states. A key ``view``, with the value ``Manager, Member, Reviewer``, for
instance.

In tagged values, the text you type in is normally taken as a string. If you
prefix your value with ``python:``, it is copy-pasted literally into your code.
So ``python:["a", "b"]`` is put into your code as ``["a", "b"]``.

The config file
===============

ArchGenXML generates a ``config.py`` file in your Product's root directory,
which in turn tries to import ``AppConfig.py``. So stuff you put in there is
treated as if it is placed in the main config file.

Every ArchGenXML-generated file contains an import like ``from
Products.YourProduct.config import *``, so the variables defined in your
AppConfig are directly available in all the files. This means that *you can
specify shortcuts* for the tagged values.

Shorter tagged values
=====================

Example line in your 'AppConfig.py'::

   EDITORS = 'Manager, Member, Reviewer'

Remember that we can use ``python:`` to paste raw python code directly into the
generated files. After adding above line, the original tagged value ``view``
with value ``Manager, Member, Reviewer`` can be shortened to the tagged value
``view`` with value ``python:EDITORS``. Now that's handy :-) And if you need to
change this definition you have it at a central place. No need to touch 2, 3 or
more ``states`` in UML where it's used several times on each.

You can use this little *feature* almost everywhere, so its not limited to
workflow.
