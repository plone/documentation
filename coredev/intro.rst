.. -*- coding: utf-8 -*-

================================
Getting started with development
================================

This document assumes you want to run the current latest Plone source,
fix a bug in Plone, or test an addon in the context of the latest code,
and will detail the full process.
For more information on writing PLIPS, please :doc:`go here <plips>`.

Version Support Policy
======================
If you are triaging or fixing bugs,
keep in mind that Plone has a `version support policy <http://plone.org/support/version-support-policy>`_.

Dependencies
============
* git, `how to setup <https://help.github.com/articles/set-up-git/>`_
* `Python <http://python.org/>`_ version 3.6 or 3.7 or 3.8 including development headers.
* If you are on Mac OSX,
  you will need to install `XCode <https://developer.apple.com/xcode/>`_.
  You can do this through the app store or several other soul-selling methods.
  You will likely want to install your own python 2.6 as well since they strip out all the header files which makes compiling some extensions weird.
  You can ignore this advice to start,
  but have faith,
  you'll come back to it later.
  They always do...
* `Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`_.
  Make sure to install it or its dependencies.
  This depends on the your operating system.
* `GCC <http://gcc.gnu.org/>`_ in order to compile ZODB, Zope and lxml.
* `libxml2 and libxslt <http://xmlsoft.org/XSLT/downloads.html>`_,
  including development headers.


.. _setup-development-environment:

Setting up Your Development Environment
=======================================
The first step in fixing a bug is getting this `buildout <https://github.com/plone/buildout.coredev>`_ running.
We recommend fixing the bug on the latest branch and then `backporting <http://en.wikipedia.org/wiki/Backporting>`_ as necessary.
`GitHub <https://github.com/plone/buildout.coredev/>`_ by default always points to the currently active branch.
Dependent on the current development cycle there may exist a future branch.
I.e. 5.2 is the actively maintained stable branch and 6.0 is the future, currently unstable, active development branch.
More information on switching release branches is below.

To set up a plone 6 development environment::

  > cd ~/buildouts # or wherever you want to put things
  > git clone -b 6.0 https://github.com/plone/buildout.coredev ./plone6devel
  > cd ./plone6devel
  > ./bootstrap.sh


If you run into issues in this process,
please see the doc :doc:`issues`.

This will run for a long time if it is your first pull (~20 mins).
Once that is done pulling down eggs,
you can start your new instance with::

  > ./bin/instance fg

or as WSGI service with::

  > ./bin/wsgi

The default username/password for a dev instance is **admin/admin**.

Switching Branches
------------------
If your bug is specific to one branch or you think it should be `backported <http://en.wikipedia.org/wiki/Backporting>`_,
you can easily switch branches. The first time you get a branch, you must do::

  > git checkout -t origin/4.3

This should set up a local 4.3 branch tracking the one on GitHub.
From then on you can just do::

  > git checkout 4.3

To see what branch you are currently on,
just do::

  > git branch

The line with a * by it will indicate which branch you are currently working on.

.. important::
   Make sure to rerun buildout if you were in a different branch earlier to get the correct versions of packages,
   otherwise you will get some weird behavior!


Jenkins / mr.roboto
===================
Plone has a Continuous Integration setup and follows CI rules.

When you push a change to any Plone core package,
our testing/CI middleware ``mr.roboto`` starts running all the tests that are needed to make sure that you don't break anything.
For each Plone and Python version we run two jobs,
one for the package itself (which will give you a fast feedback, within 10 minutes)
and one on the full coredev build (which can take up until an hour,
but makes sure no other packages are effected by your change.

For more information you can check :doc:`Mr. Roboto workflow <roboto>` or our `Jenkins machine <https://jenkins.plone.org/>`_.

The CI system at jenkins.plone.org is a shared resource for Plone core developers to notify them of regressions in Plone core code.
Build breakages are a normal and expected part of the development process.
Our aim is to find errors and eliminate them as quickly as possible,
without expecting perfection and zero errors.
Though,
there are some essential practices that needs to be followed in order to achieve a stable build:

#. Don’t Check In on a Broken Build - check Jenkins before
#. Always Run All Commit Tests Locally before Committing
#. Wait for Commit Tests to Pass before Moving On
#. Never Go Home on a Broken Build
#. Always Be Prepared to Revert to the Previous Revision
#. Time-Box Fixing before Reverting
#. Don’t Comment Out Failing Tests
#. Take Responsibility for All Breakages That Result from Your Changes

See :doc:`Essential Continuous Integration Practices <continous-integration>` for more information.

Since it can be burdensome to check this manually,
install yourself the tools to always see the current state of the Plone CI Server:

- For (Ubuntu?) Linux there is `BuildNotify <https://bitbucket.org/Anay/buildnotify/wiki/Home>`_.
- For Mac there is `CCMenu <http://ccmenu.org/>`_.
- For windows there is `CCTray <http://cruisecontrolnet.org/projects/ccnet/wiki/CCTray_Download_Plugin>`_.
- For Firefox there is `CruiseControl Monitor <https://addons.mozilla.org/en-US/firefox/addon/cruisecontrol-monitor/>`_ and many other jenkins specific plugins.

These tools were built to parse a specific file that CruiseControl another CI tool generated.
Jenkins generates this file too.
You want to configure your notifier of choice with this url: ``http://jenkins.plone.org/cc.xml``

Checking out Packages for Fixing
================================
Most packages are not in :file:`src/` by default,
so you can use ``mr.developer`` to get the latest and make sure you are always up to date.
It can be a little daunting at first to find out which packages are causing the bug in question,
but just ask on irc if you need some help.
Once you [think you] know which package(s) you want,
we need to pull the source.

You can get the source of the package with ``mr.developer`` and the checkout command,
or you can go directly to editing :file:`checkouts.cfg`.
We recommend the latter but will describe both.
In the end,
:file:`checkouts.cfg` must be configured either way so you might as well start there.

At the base of your buildout,
open :file:`checkouts.cfg` and add your package if it's not already there::

  auto-checkout =
          # my modified packages
          plone.app.caching
          plone.caching
          # others
          ...

Then rerun buildout to get the source packages::

  > ./bin/buildout

Alternatively,
we can manage checkouts from the command line,
by using mr.developer's :command:`bin/develop` command to get the latest source.
For example,
if the issue is in ``plone.app.caching`` and ``plone.caching``::

  > ./bin/develop co plone.app.caching
  > ./bin/develop co plone.caching
  > ./bin/buildout

Don't forget to rerun buildout!
In both methods,
``mr.developer`` will download the source from GitHub (or otherwise) and put the package in the :file:`src/` directory.
You can repeat this process with as many or as few packages as you need.
For some more tips on working with ``mr.developer``,
please :doc:`read more here <mrdeveloper>`.

Testing Locally
===============
To run a test for the specific module you are modifying::

  > ./bin/test -m plone.app.caching

These should all run without error.
Please don't check in anything that doesn't!
Now write a test case for the bug you are fixing and make sure everything is running as it should.

After the module level tests run with your change,
please make sure other modules aren't affected by the change by running the full suite, including robot-tests (remove the `--all` to run without robot tests)::

  > ./bin/test --all

.. note::
    Tests take a long time to run.
    Once you become a master of bugfixes,
    you may just let jenkins do this part for you.
    More on that below.

Updating CHANGES.rst and checkouts.cfg
======================================

Once all the tests are running locally on your machine,
you are **ALMOST** ready to commit the changes.
A couple housekeeping things before moving on.

First,
please edit :file:`CHANGES.rst` (or :file:`CHANGES.txt`, or :file:`HISTORY.txt`) in each package you have modified and add a summary of the change.
This change note will be collated for the next Plone release and is important for integrators and developers to be able to see what they will get if they upgrade.
New changelog entries should be added at the very top of :file:`CHANGES.rst`.
Some packages already switched to use `towncrier <https://pypi.org/project/towncrier/>`_.
If this is the case you'll find a note at the top of the `CHANGES.rst` file.

*Most importantly*,
if you didn't do it earlier,
edit :file:`checkouts.cfg` file in the buildout directory and add your changes package to the ``auto-checkout`` list.
This lets the release manager know that the package has been updated,
so that when the next release of Plone is cut,
a new egg will be released and Plone will need to pin to the next version of that package.
READ: this is how your fix becomes an egg!

Note that there is a section separator called "# Test Fixes Only".
Make sure your egg is above that line or your egg probably won't get made very quickly.
This just tells the release manager that any eggs below this line have tests that are updated,
but no code changes.

Modifying :file:`checkouts.cfg` file also triggers the buildbot,
`jenkins <https://jenkins.plone.org/>`_, to pull in the egg and run all the tests against the changes you just made.
Not that you would ever skip running all tests of course...
More on that below.

If your bug is in more than one release (e.g. 4.1 and 4.2),
please checkout both branches and add to the :file:`checkouts.cfg` file.

Committing and Pull Requests
============================
Phew! We are in the home stretch.
How about a last minute checklist:

 * Did you fix the original bug?
 * Is your code consistent with our :doc:`/develop/styleguide/index`?
 * Did you remove any extra code and lingering pdbs?
 * Did you write a test case for that bug?
 * Are all test cases for the modules(s) and for Plone passing?
 * Did you update :file:`CHANGES.rst` in each packages you touched?
 * Did you add your changed packages to :file:`checkouts.cfg`?

If you answered *YES* to all of these questions,
you are ready to push your changes!
A couple quick reminders:

 * Only commit directly to the development branch if you're confident your code won't break anything badly and the changes are small and fairly trivial.
   Otherwise, please create a ``pull request`` (more on that below).
 * Please try to make one change per commit.
   If you are fixing three bugs,
   make three commits.
   That way,
   it is easier to see what was done when,
   and easier to ``roll back`` any changes if necessary.
   If you want to make large changes cleaning up whitespace or renaming variables,
   it is especially important to do so in a separate commit for this reason.
 * We have a few angels that follow the changes and each commit to see what happens to their favourite CMS!
   If you commit something REALLY sketchy,
   they will politely contact you,
   most likely after immediately reverting changes.
   There is no official people assigned to this so if you are especially nervous,
   jump into `#plone <http://webchat.freenode.net?channels=plone>`_ and ask for a quick eyeball on your changes.

Committing to Products.CMFPlone
===============================
If you are working a bug fix on ``Products.CMFPlone``,
there are a couple other things to take notice of.
First and foremost,
you'll see that there are several branches.
At the time of writing this document,
there are branches for 4.2.x, 4.3.x and master,
which is the implied 5.0.
This may change faster than this documentation,
so check the branch dropdown on GitHub.

Still with me? So you have a bug fix for 4.x.
If the fix is only for one version,
make sure to get that branch and party on.
However, chances are the bug is in multiple branches.

Let's say the bug starts in 4.1. Pull the 4.1 branch and fix and commit there with tests.

If your fix only involved a single commit,
you can use git's ``cherry-pick`` command to apply the same commit to a different branch.

First check out the branch::

  > git checkout 4.2

And then ``cherry-pick`` the commit (you can get the SHA hash from git log).::

  > git cherry-pick b6ff4309

There may be conflicts;
if so,
resolve them and then follow the directions git gives you to complete the ``cherry-pick``.

If your fix involved multiple commits,
``cherry-picking`` them one by one can get tedious.
In this case things are easiest if you did your fix in a separate feature branch.

In that scenario,
you first merge the feature branch to the 4.1 branch::

  > git checkout 4.1
  > git merge my-awesome-feature

Then you return to the feature branch and make a branch for `rebasing` it onto the 4.2 branch::

  > git checkout my-awesome-feature
  > git checkout -b my-awesome-feature-4.2
  > git rebase ef978a --onto 4.2

(ef978a happens to be the last commit in the feature branch's history before it was branched off of 4.1.
You can look at git log to find this.)

At this point,
the feature branch's history has been updated,
but it hasn't actually been merged to 4.2 yet.
This lets you deal with resolving conflicts before you actually merge it to the 4.2 release branch.
Let's do that now::

  > git checkout 4.2
  > git merge my-awesome-feature-4.2


Branches and Forks and Direct Commits - Oh My!
----------------------------------------------

.. note::

    This section needs a rewrite.
    Meanwhile we do not allow direct commits, except in very rare cases.

Plone used to be in an svn repository,
so everyone is familiar and accustomed to committing directly to the branches.
After the migration to GitHub,
the community decided to maintain this spirit.
If you have signed the :doc:`contributor agreement <contributors_agreement_explained>` form,
you can commit directly to the branch
(for plone this would be the version branch, for most other packages this would be ``master``).

HOWEVER,
there are a few situations where a branch is appropriate.
If you:

 * are just getting started,
 * are not sure about your changes
 * want feedback/code review
 * are implementing a non-trivial change

then you likely want to create a branch of whatever packages you are using and then use the `pull request <https://help.github.com/articles/using-pull-requests>`_ feature of GitHub to get review.
Everything about this process would be the same except you need to work on a branch.
Take the ``plone.app.caching`` example.
After checking it out with ``mr.developer``,
create your own branch with::

  > cd src/plone.app.caching
  > git checkout -b my_descriptive_branch_name

.. note::

    Branching or forking is your choice.
    I prefer branching,
    and I'm writing the docs so this uses the branch method.
    If you branch,
    it helps us because we *know* that you have committer rights.
    Either way it's your call.

Proceed as normal.
When you are ready to ``push`` your fix,
push to a remote branch with::

  > git push origin my_descriptive_branch_name

This will make a remote branch in GitHub.
Navigate to this branch in the GitHub UI and on the top right there will be a button that says **"Pull Request"**.
This will turn your request into a pull request on the main branch.
There are people who look once a week or more for pending pull requests and will confirm whether or not its a good fix and give you feedback where necessary.
The reviewers are informal and very nice so don't worry - they are there to help!
If you want immediate feedback,
jump into IRC with the ``pull request`` link and ask for a review.

.. note::
    You still need to update :file:`checkouts.cfg` file in the correct branches of buildout.coredev!

Finalizing Tickets
==================
If you are working from a ticket,
please don't forget to go back to the ticket and add a link to the changeset.
We don't have integration with GitHub yet so it's a nice way to track changes.
It also lets the reporter know that you care.
If the bug is really bad,
consider pinging the release manager and asking him to make a release pronto.

FAQ
===
 * *How do I know when my package got made?*
    You can follow the project on GitHub and watch its `timeline <https://github.com/organizations/plone>`_.
    You can also check the :file:`CHANGES.rst` of every plone release for a comprehensive list of all changes and validate that yours is present.

