================
Python debugging
================

.. admonition:: Description

    Using Python command-line debugger (``pdb``) to debug Plone and Python
    applications.


Introduction
============

The Python debugger (``pdb``) is an interactive command-line debugger.

It is very limited in functionality, but it will work in every environment
and type of console. Plone also has through-the-web-browser PBD debugging
add-on products.

.. note::

    ``pdb`` is not the same as the Python interactive shell. ``pdb`` allows
    you to step through the code, whilst the Python shell allows you just to
    inspect and manipulate objects.

If you wish to play around with Zope in interactive Python shell or run
scripts instead of debugging (exceptions), please read :doc:`Command line
</develop/plone/misc/commandline>` documentation.

See also


Using ``pdb``
=============

# Go to your code and insert the statement ``import pdb; pdb.set_trace()`` at
  the point where you want have a closer look.  Next time the code is run,
  the execution will stop there and you can examine the current context
  variables from a Python command prompt.

# After you have added ``import pdb; pdb.set_trace()`` to your code, stop
  Zope and start it in the foreground using the ``bin/instance fg`` command.

# TextMate support for ``pdb`` can be found at
  `https://pypi.python.org/pypi/PdbTextMateSupport/0.3
  <https://pypi.python.org/pypi/PdbTextMateSupport/0.3>`_.

# ``mr.freeze`` allows traces to be added without restarting:
  `https://pypi.python.org/pypi/mr.freeze
  <https://pypi.python.org/pypi/mr.freeze>`_.

Example::

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

Pretty printing objects
=======================

Example::

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


Useful ``pdb`` commands
========================

Just type the command and hit enter.

``s``
    step into, go into the function in the cursor

``n``
    step over, execute the function under the cursor without stepping into it

``c``
    continue, resume program

``w``
    where am I? displays current location in stack trace

``b``
    set breakpoint

``cl``
    clear breakpoint

``bt``
    print stack trace

``up``
    go to the scope of the caller function

``pp``
    pretty print object

``until``
    Continue execution until the line with the line number greater than the
    current one is reached or when returning from current frame

.. note::

    The ``until`` command (or ``unt``) is available only on Plone 4.x or
    superior as it is a new feature provided by the ``pdb`` module under
    Python 2.6.


Useful ``pdb`` snippets
=======================

Output object's class::

    (Pdb) print obj.__class__

Output object attributes and methods::

    (Pdb) for i in dir(obj): print i

Print local variables in the current function::

    (Pdb) print locals()

Dumping incoming HTTP GET or HTTP POST::

    (Pdb) print "Got request:"
    (Pdb) for i in self.request.form.items(): print i

Executing code on the context of the current stack frame::

    (Pdb) pp my_tags
    ['bar', 'barbar']

    (Pdb) !my_tags = ['foo', 'foobar']
    (Pdb) pp my_tags
    ['foo', 'foobar']


.. note::

     The example above will modify the previous value of the variable
     ``my_tags`` in the current stack frame.


Automatically start debugger when exception is raised (browser)
==================================================================

You can start interactive through-the-browser Python debugger when your site
throws an exception.

Instead of getting "We're sorry there seems to be an error..." page you get
a pdb prompt which allows you to debug the exception. This is also
known as post-mortem debugging.

This can be achieved with ` `Products.PDBDebugMode`` add-on.

* https://pypi.python.org/pypi/Products.PDBDebugMode


.. note ::

   PDBDebugMode is not safe to install on the production server due to
   sandbox security escape.


Automatically start debugger when exception is raised (command line)
=====================================================================

.. note::

    This cannot be directly applied to a web server, but works with command
    line scripts.

.. note::

    This does not work with Zope web server launch as it forks a process.

Example::

    python -m pdb myscript.py

Hit ``c`` and ``enter`` to start the application. It keeps running, until
an uncaught exception is raised. At this point, it falls back to the ``pdb``
debug prompt.


For more information see

* http://docs.python.org/library/pdb.html
