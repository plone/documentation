Running tests
-------------

.. admonition:: description

    It is not much good writing a test or relying on someone else's tests
    if you don't know how to run them.

The easiest way to run tests in Zope is to use zopectl or the equivalent
control script.

::

      ./bin/zopectl test -s Products.RichDocument

This would run all tests in the Products.RichDocument module. If you are
using a `buildout <http://www.buildout.org/>`_ with an instance control script called instance,
this would be:

::

      ./bin/instance test -s Products.RichDocument

Using buildout is probably a good idea - see `the buildout tutorial <http://www.buildout.org/docs/tutorial.html>`_ -
not at least because this is the only way that works reliably on
Windows. We will use this syntax from now on.

To execute a single test or a set of tests matched by regular
expression, you can use:

::

      ./bin/instance test -s Products.RichDocument -t setup

This would run tests in files like test\_setup.py. To run all doctests
in README.txt (presuming there was a test suite for this file) you would
write:

::

      ./bin/instance test -s Products.RichDocument -t README.txt

The new test runner also includes a few debugging options. For example:

::

      ./bin/instance test -m Products.RichDocument -D

This will stop execution at the first failing test and drop into a PDB
post-mortem.

To see the other options that are available, run:

::

      ./bin/instance test --help

When the tests you think are relevant all pass, it’s time to run all
tests and make sure nothing else broke. (No, we don’t care that you are
writing your code in a totally different python module than what those
other tests are supposed to test, and that they were all fine and good
and all you changed was a docstring. Run the tests when you think you’re
done.)

When tests finish running, you will see a report like:

::

        ...
        Ran 18 tests in 6.463s

        OK

(it may look slightly different, depending on which test runner you are
using)

Rehearse a satisfied sigh as you read the line “OK”, as opposed to
seeing a count of failed tests. With time, this will be the little
notifier that lets you go to bed, see your friends again or generally
get back to real life with an svn commit.

If you’re not so lucky, you may see:

::

        Ran 18 tests in 7.009s

        FAILED (failures=1, errors=1)

(again, the output may look slightly different depending on your test
runner, but the same information should always be there)

This means that there were 1 python error and 1 failed test during test
execution.

A python error means that some of your test code, or some code that was
called by a test, raised an exception. This is bad, and you should fix
it right away.

A failed test means that your test was trying to assert something that
turned out not to be true. This could be OK. It could mean you haven't
written the code the test is testing yet (well done, you wrote the test
first!), or that you don't yet know why it's failing. Sometimes you may
be radically refactoring or rewriting parts of your code, and the tests
will keep on failing until you're done. Incidentally, this is part of
the reason why unit tests are so good - you can do that kind of stuff.

It's sometimes (not always - don't try this on Plone core unless you've
been told it's OK by the release manager) acceptable to go to bed and
check in a failing test if you are not in a position to know how to fix it.
At least other developers will be aware of the problem and may be able to fix it.
