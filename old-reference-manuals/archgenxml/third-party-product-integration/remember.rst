========
Remember
========

.. contents :: :local:

.. admonition:: Description

        Generate 'Remember' based Member-Types. Its the successor of CMFMember.

Prerequisites
-------------
You must install to additional Products:

* `membrane <http://plone.org/products/membrane>`_

* `remember <http://plone.org/products/remember>`_ (using `Five 1.4.3+ <http://codespeak.net/z3/five/>`_)

You should also read the documentation of both and understand how they work!

A Content-Type based on remember
--------------------------------
* Create a class in your class diagram and give it a a stereotype ``<<remember>>``
* add the tagged value ``use_workflow`` and set it to one of ``member_approval_workflow`` or ``member_auto_workflow``. You can create also your own workflow if you know what remember needs (look at the workflows shipped with remember).
* set the ``active_workflow_states`` tagged value to the class and declare which states of the used workflow are the ones, where the user can log in with. It expects a list of values, e.g. ``python:["private", "public"]``
* Add attributes (fields) as you need. Attention here, only override fields of remembers BaseMember schema if you know what youre doing.
* Generate & Done
