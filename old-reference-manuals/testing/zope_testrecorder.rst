Using zope.testrecorder to record functional tests
--------------------------------------------------

.. admonition:: description

    The zope.testrecorder product brings us full-circle: functional tests are
    recorded from within the browser, and saved to a runnable test.


Functional tests using zope.testbrowser save us from clicking around the
browser to regression test UI, but writing them could still be easier.
With complex templates, it can sometimes be difficult to find out what
actual links and form fields the testbrowser test should be looking for,
and what text to use in assertions.

This is where zope.testrecorder comes in. The theory is that you click
around the UI only once, and then render the history of what you did to
a runnable testbrowser test. zope.testrecorder can even create
`Selenium <http://seleniumhq.org/>`_ tests - an alternative form of
functional tests which runs in the browser (i.e. it automates your browser
right before your eyes) and thus supports JavaScript, but which cannot
be run as part of an automated test run without a browser.

Installing zope.testrecorder is simple. First, check it out from Zope’s
subversion repository:

::

        svn co svn://svn.zope.org/repos/main/zope.testrecorder/trunk zope.testrecorder



See INSTALL.txt for further instructions, but the easiest way to install
it in a Zope 2 instance is just to put it in your Products directory:
Copy zope.testrecorder/src/zope/testrecorder as a product into
Products/testrecorder and restart Zope. Then, go to the ZMI and add a
Test Recorder object in the root of your Zope instance. Call it e.g.
test-recorder.

Presuming you run Zope on localhost:8080, you should now be able to go
to http://localhost:8080/test-recorder/index.html. You should see a page
something like this:

.. figure:: /develop/plone/images/blank-testrecorder.png
   :align: center
   :alt: Screenshot of blank test recorder

**NOTE:** Like most things, zope.testrecorder seems to work better in
Firefox than in other browsers.

Now, enter the address of your Plone site (or indeed any web site), e.g.
http://localhost:8080/Plone and click Go. You can perform any number of
operations, e.g. logging in and clicking around the UI. If you wish to
add a comment to your test run, as you would add free text inside a
doctest, click the Add comment button. If you wish to verify that some
text appears on the page, highlight that text, shift-click on it, and
select “Check text appears on page”:

.. figure:: /develop/plone/images/verify-testrecorder.png
   :align: center
   :alt: Screenshot of text verification

   Screenshot of text verification

When you are done, click Stop recording. You can then choose to render
the test as a Python doctest and you will get something like:

::

      Create the browser object we'll be using.

          >>> from zope.testbrowser import Browser
          >>> browser = Browser()
          >>> browser.open('http://localhost/test')

      A test comment.

          >>> 'start writing' in browser.contents
          True

You can then paste this into a doctest file, and perform any
post-processing or make any changes that may be necessary to make the
test more generally valid.

Tips for using zope.testrecorder
--------------------------------

Plan, plan, plan
    It's best if you have a rough script in front of you before you start recording
    tests, or you may get lost afterwards. Make good use of the Add comment button
    to state what you are testing before you test it, so that the final doctest will
    make sense.
Careful where you click
    Some parts of the Plone UI are more ephemeral than others. It may not be a good
    idea to rely on links in the Recent portlet, for example. Think about what
    operations will provide the most general and valid test. It will save you time
    in the long run.
Set up your site beforehand
    Recall from the section on zope.testbrowser that we set up users and basic site
    structure with calls to the Python APIs instead of using testbrowser to manipulate
    the "site setup" screents. When using zope.testrecorder you may want to set up the
    same users with the same user names and passwords, and the same site structure
    before you start recording to test. Otherwise, you may need to change some of
    the values of the test.
Check the doctest
    zope.testrecorder is a time-saving tool. Sometimes, it may end up referring to
    parts of the page that can't be guaranteed to be consistent (such as randomly
    generated ids of content objects), and sometimes you may have gone on a detour
    and ended up with a test that contains irrelevant or duplicate sections. Always
    fix up your test (and run it!) afterwards, to make sure that the test remains
    valid for the future - otherwise, you will end up clicking around the UI in
    anger again before you know it.
