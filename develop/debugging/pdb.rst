================
Python Debugging
================

.. admonition:: Description

    Using Python command-line debugger (``Pdb``) to debug Plone and Python
    applications.


Introduction
============

The `Python Debugger <https://docs.python.org/2/library/pdb.html>`_ (``Pdb``) is an interactive command-line debugger.

Plone also has through-the-web-browser Pdb debugging add-on products.

.. note::

   ``Pdb`` is not the same as the Python interactive shell.
   ``Pdb`` allows you to step through the code, whilst the Python shell allows you to
    inspect and manipulate objects.

If you wish to play around with Zope in interactive Python shell or run scripts instead of debugging (exceptions),
please read :doc:`Command line </develop/plone/misc/commandline>` documentation.

Usage
=====

# Go to your code and insert the statement ``import pdb; pdb.set_trace()`` at the point where you want have a closer look.
  Next time the code is run, the execution will stop there and you can examine the current context
  variables from a Python command prompt.

# After you have added ``import pdb; pdb.set_trace()`` to your code, stop Zope and start it in the foreground using the ``bin/instance fg`` command.

Example:

.. code-block:: python

    class AREditForm(crud.EditForm):
        """ Present edit table containing rows per each item added and delete controls """
        editsubform_factory = AREditSubForm

        template = viewpagetemplatefile.ViewPageTemplateFile('ar-crud-table.pt')

        @property
        def fields(self):

            #
            # Execution will stop here and interactive Python prompt is opened
            #

            import pdb ; pdb.set_trace()
            constructor = ARFormConstructor(self.context, self.context.context, self.request)
            return constructor.getFields()

Printing Objects
================

Example:

.. code-block:: python

    >>> from pprint import pprint as pp
    >>> pp folder.__dict__
    {
      '_Access_contents_information_Permission': ['Anonymous',
                                                  'Manager',
                                                  'Reviewer'],
      '_List_folder_contents_Permission': ('Manager', 'Owner', 'Member'),
      '_Modify_portal_content_Permission': ('Manager', 'Owner'),
      '_View_Permission': ['Anonymous', 'Manager', 'Reviewer'],
      '__ac_local_roles__': {'gregweb': ['Owner']},
      '_objects': ({'meta_type': 'Document', 'id': 'doc1'},
                   {'meta_type': 'Document', 'id': 'doc2'}),
      'contributors': (),
      'creation_date': DateTime('2005/02/14 20:03:37.171 GMT+1'),
      'description': 'Dies ist der Mitglieder-Ordner.',
      'doc1': <Document at doc1>,
      'doc2': <Document at doc2>,
      'effective_date': None,
      'expiration_date': None,
      'format': 'text/html',
      'id': 'folder',
      'language': '',
      'modification_date': DateTime('2005/02/14 20:03:37.203 GMT+1'),
      'portal_type': 'Folder',
      'rights': '',
      'subject': (),
      'title': "Documents",
      'workflow_history': {'folder_workflow': ({'action': None,
        'review_state': 'visible', 'comments': '', 'actor': 'gregweb',
        'time': DateTime('2005/02/14 20:03:37.187 GMT+1')},)}
    }


Commands
========

Type the command and hit enter.

.. code-block:: console

   ``s``

step into, go into the function in the cursor

.. code-block:: console

   ``n``

step over, execute the function under the cursor without stepping into it

.. code-block:: console

   ``c``

continue, resume program

.. code-block:: console

   ``w``

where am I? displays current location in stack trace

.. code-block:: console

   ``b``

set breakpoint

.. code-block:: console

   ``cl``

clear breakpoint

.. code-block:: console

   ``bt``

print stack trace

.. code-block:: console

   ``up``

go to the scope of the caller function

.. code-block:: console

   ``pp``

pretty print object

.. code-lock:: console

   ``until``

Continue execution until the line with the line number greater than the current one is reached or when returning from current frame.


Snippets
========

Output object's class:

.. code-block:: python

   (Pdb) print obj.__class__

Output object attributes and methods:

.. code-block:: python

   (Pdb) for i in dir(obj): print i

Print local variables in the current function:

.. code-block:: python

   (Pdb) print locals()

Dumping incoming HTTP GET or HTTP POST:

.. code-block:: python

   (Pdb) print "Got request:"
   (Pdb) for i in self.request.form.items(): print i

Executing code on the context of the current stack frame:

.. code-block:: python

   (Pdb) from pprint import pprint as pp
   (Pdb) pp my_tags
   ['bar', 'barbar']

   (Pdb) !my_tags = ['foo', 'foobar']
   (Pdb) pp my_tags
   ['foo', 'foobar']


.. note::

   The example above will modify the previous value of the variable ``my_tags`` in the current stack frame.


Start Debugger When Exception Is Raised
=======================================

Browser
-------

You can start interactive through-the-browser Python debugger when your site throws an exception.

Instead of getting "We're sorry there seems to be an error..." page you get a Pdb prompt which allows you to debug the exception.
This is also known as post-mortem debugging.

This can be achieved with ` `Products.PDBDebugMode`` add-on.
By using this add-on, you have a ``/@@pdb`` view that you can call on any context too.


* https://pypi.python.org/pypi/Products.PDBDebugMode

.. note::

   Remember that this add-on hooks into the "error_log" exception handling.

   If you don't want to enter into Pdb when an specific exception is raised, like ``Unauthorized``, you should edit it in the ZMI.

   PDBDebugMode is not safe to install on the production server due to sandbox security escape.


Command Line
------------

.. note::

   This cannot be directly applied to a web server, but works with command line scripts.
   This does not work with Zope web server launch as it forks a process.

Example:

.. code-block:: python

   python -m pdb myscript.py

Hit ``c`` and ``enter`` to start the application.
It keeps running, until an uncaught exception is raised.
At this point, it falls back to the ``Pdb`` debug prompt.


For more information see

* http://docs.python.org/library/pdb.html


Interactive Debugging
=====================

You can use interactive debugging via ``bin/{client1|instance} debug`` (use the name of the instance script you're using in your buildout).
It gives you an interactive Python interpreter with access to Zope's root object (bound to "app").

In the interpreter, you can do "normal" Python debugging.


Alternative Debugger
====================

Some of these options (like ``q``) are complementary to ``Pdb`` itself.
We suggest you to try the alternatives here, some features (like tab completion and syntax highlighting)
are hard to live without after getting used to them.

ipdb
----

ipdb exports functions to access the IPython debugger, which features tab completion, syntax highlighting, better tracebacks,
better introspection with the same interface as the Pdb module.

If you install iw.debug with ipdb, you can call ipdb in any object of your instance, by adding /ipdb to any url.

* https://pypi.python.org/pypi/ipdb
* https://pypi.python.org/pypi/iw.debug

pdbpp
-----

This module is an extension of the Pdb module of the standard library.
It is meant to be fully compatible with its predecessor, yet it introduces a number of new features to make your debugging experience as nice as possible.

pdb++ is meant to be a drop-in replacement for Pdb.

- colorful TAB completion of Python expressions (through fancycompleter)
- optional syntax highlighting of code listings (through pygments)
- sticky mode
- several new commands to be used from the interactive (Pdb++) prompt
- smart command parsing (hint: have you ever typed r or c at the prompt to print the value of some variable?)
- additional convenience functions in the Pdb module, to be used from your program

* https://pypi.python.org/pypi/pdbpp

debug
-----

Instead of ``import pdb;pdb.set_trace()`` you can use use ``import debug``, then it automatically enters into ipdb.
You can do ``/bin/instance debug`` and then call ``import debug`` as well.

* https://pypi.python.org/pypi/debug

pudb
----
It's an alternative to Pdb with a curses interface.
Its goal is to provide all the niceties of modern GUI-based debuggers in a more lightweight and keyboard-friendly package.

PuDB allows you to debug code right where you write and test it–in a terminal.
If you’ve worked with the excellent (but nowadays ancient) DOS-based Turbo Pascal or C tools, PuDB’s UI might look familiar.

- Syntax-highlighted source, the stack, breakpoints and variables are all visible at once and continuously updated. This helps you be more aware of what’s going on in your program. Variable displays can be expanded, collapsed and have various customization options.
- Simple, keyboard-based navigation using single keystrokes makes debugging quick and easy. PuDB understands cursor-keys and Vi shortcuts for navigation. Other keys are inspired by the corresponding pdb commands.
- Use search to find relevant source code, or use “m” to invoke the module browser that shows loaded modules, lets you load new ones and reload existing ones.
- Breakpoints can be set by pointing at a source line and hitting “b” and then edited visually in the breakpoints window. Or hit “t” to run to the line under the cursor.
- Drop to a Python shell in the current environment by pressing “!”.
- PuDB places special emphasis on exception handling. A post-mortem mode makes it easy to retrace a crashing program’s last steps.
- IPython integration (see wiki)

* https://pypi.python.org/pypi/pudb

q
-

Quick and dirty debugging output.
All output goes to /tmp/q, which you can watch with this shell command: ``tail -f /tmp/q``.

That way you can print variables, functions, etc.
Check it's documentation for more examples.

* https://pypi.python.org/pypi/q


Debugging Page Templates
========================

Since Plone 5, Chameleon (five.pt) is used for the TAL engine.
When using Chameleon, we can use the following snippet to debug page templates:

Example:

.. code-block:: python

   <?python locals().update(econtext); import pdb; pdb.set_trace() ?>

However, this doesn't work in skin templates and in TTW (Through-The_Web) templates.

If you want a full explanation of how this snippet works (specially about the context variable),
check https://www.starzel.de/blog/magic-templates-in-plone-5.


Debugging ZMI Python Script
===========================

If you install https://pypi.python.org/pypi/Products.enablesettrace in your instance, you can import Pdb inside a Python Script.


Browser Extensions
==================

If you need to call ``/@@reload`` (if you installed plone.reload) or ``?diazo`` on your current Plone, you can use the Plone Reloader extension.

* https://chrome.google.com/webstore/detail/plone-reloader/bcdahfmmenfikninekekpbncgdkdlapl

This extension displays the plone.reload form in a popup so you can reload your current Plone instance code without switching to another tab.
It also provides buttons to open diazo off/debug Urls.
