Introduction
------------

.. admonition:: description

    What is this thing called testing anyway?

"I know I should write tests, but …

*  … they take time to write
*  … I’m a good developer
*  … my customer / the community does the testing"

Sound familiar? No matter how good you think you are, you will make
mistakes. Your code will contain bugs and someone will come after you
demanding an explanation. Without some methodical way of testing, you
are guaranteeing your code with nothing more than guesswork and
arrogance. Clicking around the Plone interface for a few minutes before
you ship your code off to the customer or user is simply not enough.

Testing is an art, it needs to be built into your development cycle from
the very beginning - it is not something you do only after all the other
work is finished, it is something you do continuously. Unfortunately,
testing often evokes emotions of dread in developers. It’s slow, it’s
boring, it’s not what they signed up to do. But the art of testing has
evolved beyond that - there is considerable elegance and fun to be found
in well-conceived test strategies.

This tutorial aims to give you the tools you need to write tests and
testable software in Plone. If you are writing software for Plone core
itself, don’t even think about committing any bug fix or feature without
test coverage. If you are writing an add-on product or doing a
customisation, holding yourself to the same high standards that the
Plone core team do will give you better confidence in your software and
will likely save you considerable pain down the road.

Examples
~~~~~~~~

This tutorial contains several examples of the various types of tests.
They are available in the
`example.tests <http://dev.plone.org/collective/browser/examples/example.tests/trunk>`_
package, which you can install as a develop egg in a Plone 3 buildout.
The examples of running tests use the standard commands for buildouts, since
this is the only way that works reliably on Windows (that is, plain zopectl
test will not work on Windows).

Take a look at the :doc:`buildout docs </old-reference-manuals/buildout/index>` for more information.
