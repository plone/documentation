How To Commit Fixes to Plone Core
=================================
This document assumes you want to fix a bug and will detail the full process. For more information on writing PLIPS, please :doc:`go here <plips>`.

Version Support Policy
----------------------
If you are triaging or fixing bugs, keep in mind that Plone has a `version support policy <https://plone.org/support/version-support-policy>`_.

We recommend fixing the bug on the latest branch and then `backporting <http://en.wikipedia.org/wiki/Backporting>`_ as necessary.
`Github <https://github.com/plone/buildout.coredev/>`_ by default always points to the currently active branch.
I.e 4.3 is latest stable release and 5.0 has no stable release it points to 4.3.
More information on switching release branches is below.

Setting up Your Development Environment
---------------------------------------

The first step in fixing a bug is getting this `buildout <https://github.com/plone/buildout.coredev>`_ running.
It contains also some information, please read it.

Install `Git <http://git-scm.com/>`_!

Setup your environment without the unified installers, we are using buildout directly.
Do not create a buildout, just prepare everything.
Therefore read carefully chapter :doc:`Installation <manage/installing/installation>`.
Understand what is needed and why.

To set up a plone 4.3 development environment (using ``bootstrap.py``)::

  > cd ~/buildouts # or wherever you want to put things
  > git clone -b 4.3  https://github.com/plone/buildout.coredev ./plone-coredev-4.3
  > cd plone-coredev-4.3
  > virtualenv --clear --no-setuptools .
  > ./bin/python bootstrap.py # (where "python" is your python 2.7 binary in virtualenv).
  > bin/buildout -v

To set up a plone 5.0 development environment (using ``pip``)::

  > cd ~/buildouts # or wherever you want to put things
  > git clone -b 5.0  https://github.com/plone/buildout.coredev ./plone-coredev-5.0
  > cd plone-coredev-5.0
  > virtualenv --clear  .
  > ./bin/pip install zc.buildout -r requirements.txt # ("pip" is setup from virtualenv).
  > bin/buildout -v

If you run into issues in this process, please see the doc :doc:`issues`.

This will run for a long time if it is your first pull (~20 mins). Once that is done pulling down eggs, You can start your new instance with::

  > ./bin/instance fg

The default username/password for a dev instance is **admin/admin**.

Switching Branches
^^^^^^^^^^^^^^^^^^
If your bug is specific to one branch or you think it should be `backported <http://en.wikipedia.org/wiki/Backporting>`_, you can easily switch branches. The first time you get a branch, you must do::

  > git checkout -t origin/4.3

This should set up a local 4.3 branch tracking the one on github. From then on you can just do::

  > git checkout 4.3

To see what branch you are currently on, just do::

  > git branch

The line with a * by it will indicate which branch you are currently working on.

.. important::
   Make sure to rerun buildout if you were in a different branch earlier to get the correct versions of packages, otherwise you will get some weird behavior!

For more information on buildout, please see the :doc:`collective developer manual documentation on buildout </old-reference-manuals/buildout/index>`.


Checking out Packages for Fixing
--------------------------------
Most packages are not in :file:`src/` by default, so you can use `mr.developer <>` to get the latest and make sure you are always up to date.
It can be a little daunting at first to find out which packages are causing the bug in question, but just ask on IRC if you need some help.
Once you [think you] know which package(s) you want, we need to pull the source.

You can get the source of the package with `mr.developer <https://pypi.python.org/pypi/mr.developer/>`_ using it's :command:`bin/develop` command to get the latest source.
For example, if the issue is in ``plone.app.caching`` and ``plone.caching``::

  > ./bin/develop co plone.app.caching
  > ./bin/develop co plone.caching
  > ./bin/buildout -N

Don't forget to rerun buildout after ``develop co``!
On buildout time ``mr.developer`` will download the source from github (or otherwise) and put the package in the :file:`src/` directory.
You can repeat this process with as many or as few packages as you need.
Read about :doc:'more tips on working with mr.developer <mrdeveloper>`.

.. note::

    For several packages there are version-lines for i.e. Plone 4.3 and master is i.e. for Plone 5.0.
    Some of them are shared by both versions.
    Keep that in mind while doing changes!
    Do not break a different main-line version of Plone!

Testing Locally
---------------
In an ideal world, you would write a test case for your issue before actually trying to fix it.
It's fine too, if you first fix it and then write the test.
If you don't start with a test case, save yourself potential problems and validate the bug before getting too deep into the issue!
Writing the tests is often more work than fixing the actual bug.
No matter how you approach it, you should ALWAYS run test cases for both the module and whole plone-coredev buildout.
Tests must pass to get the change into Plone core!

To run tests for the specific module you are modifying::

  > ./bin/test -m plone.app.caching

These should all run without error.
If you haven't written it already, this is a good time to write a test case for the bug you are fixing and make sure everything is running as it should.

After the module level tests run with your change, please make sure other modules aren't affected by the change by running the full suite::

  > ./bin/alltests --all

.. note::

    Tests take a long time to run.
    Once you become a master of bugfixes, you may just let Jenkins CI server do this part for you.
    More on that below.

Housekeeping: Updating CHANGES.rst
----------------------------------
Some Housekeeping is needed before a pull-request can be created.

* Check you code if it confirms with the :doc:`plone style guide`!
  Consider running code-analysis.

* Check the version number.
  We stick to `sematic versioning <http://semver.org/>`_
  Basic increase at bugfix level is done automatically post release, but check ``setup.py``.
  Does your change is more than a bugfix minor version increase is needed.
  This should be discussed at the plone development mailing list!
  Major chnages are needing in nearley all cases a plip/

* Document your change!
  Edit :file:`CHANGES.rst` (or :file:`CHANGES.txt`, or :file:`HISTORY.txt`) in each package you have modified and add a summary of the change.
  New changelog entries should be added at the very top of the file.
  This change note will be collated for the next Plone release and is important for integrators and developers to be able to see what they will get if they upgrade.


Creating a Pull Requests
-------------------------

Phew! We are in the home stretch. How about a last minute checklist:

 * Did you fix the original bug?
 * Is your code consistent with our :doc:`style`?
 * Are your commit messages good?
 * Did you remove any extra code and lingering pdbs?
 * Did you write a test case for that bug?
 * Are all test cases for the modules(s) and for Plone passing?
 * Did you check the version?
 * Did you update :file:`CHANGES.rst` in each packages you touched?
 * Are all local commits pushed to your branch on github?
 * Is your branch uptodate with the target branch (rebase needed)?

If you answered *YES* to all of these questions, you are ready to create a Pull Request!

Quick reminders:
 * Please try to make one bugfix/change per pull request.
 * If you are fixing three bugs, make three branches and three pull requests.
   That way, it is easier to see what was done when, and easier to ``revert`` any changes if necessary.
   If you want to make large changes cleaning up whitespace or renaming variables, it is especially important to do so in a separate pull request for this reason.

`Pull request are made using the Github UI <https://help.github.com/articles/using-pull-requests/>`_.
Please provide a good title and provide a good description.
Expect a discussion!
We have a few angels that follow the changes and each commit to see what happens to their favourite CMS!
There is no official people assigned to this so if you are especially nervous, jump into `#plone <http://webchat.freenode.net?channels=plone>`_ and ask for a quick eyeball on your changes.

Merging a Pull-Request
----------------------

.. note::

    A pull request must be merged by a different person than the requester.

Checks
~~~~~~

The merging person (merger) needs to check a bunch of things before merge:
* Did the requester signed the contributor agreement?
* As a merger review the change!
  Invite other people to help with reviev if not sure yourself
* Is the branch up to date with the target branch (i.e. master)?
* Is the code consistent with our :doc:`style`?
* Was the version set right?
* Are the changes documented in the packages changelog?
* Are all tests passing?
* Are backports needed or does the fix need upporting?

At the moment a merger has two options to ensure passing tests:
* let it run local
* merge, check after some time (30-60 min.) the `CI server<http://jenkins.plone.org/>`_
* in future there will be a pre-check option in jenkins. But it is not available by now.

Modify checkouts in buildout.coredev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Most importantly*, if you didn't do it earlier, edit :file:`checkouts.cfg` file in the buildout directory and add the changed package to the ``auto-checkout`` list.
This lets the release manager know that the package has been updated so that when the next release of Plone is cut a new egg will be released and Plone will need to pin to the next version of that package.
Otherwise the change will not land in the next Plone release.

Note that there is a section seperator called "# Test Fixes Only".
Make sure your egg is above that line or your egg probably won't get made very quickly.
This just tells the release manager that any eggs below this line have tests that are updated, but no code changes.

Committing :file:`checkouts.cfg` file also triggers the CI task, `jenkins <https://jenkins.plone.org/>`_, to pull in the egg and run all the tests against the changes you just made.

If your bug is in more than one release (e.g. 4.3 and 5.0), please checkout both branches and add to the :file:`checkouts.cfg` file of both.

.. note::

    Did you add your changed packages to :file:`checkouts.cfg`?

Merge
~~~~~

Now if all above is done klcik the merge button at github.
Please check jenkins to make sure your changes haven't borked things. It runs every half an hour and takes a while to run so checking back in an hour is a safe bet. Have a beer and head over to the `Jenkins control panel <https://jenkins.plone.org/>`_.


Revert
~~~~~~

Prepare to revert the merge if for some reason tests are failing.
Reverting is one click in the Github UI:
It creates a new pull request with the reverted changes, which then need to be merged.
In order to work on the original code the revert need to be reverted, this creates a new branch and pull request again.
Problems can be fixed on that branch and then merged again.
This can be repeated many times, but should be avoided since it leads to confusion.

Housekeeping
~~~~~~~~~~~~
If you are working from a ticket, please don't forget mention the ticket in the PR or vice versa.
It also lets the reporter know that you care.
If the bug is really bad, consider pinging the release manager and asking him to make a release pronto.
Close the ticket!

Delete the feature branch, we do not want to pollute the branches overview with tasks done already!


Committing to packages with different branches
----------------------------------------------
If you are working a bug fix on i.e. ``Products.CMFPlone`` you'll see that there are several branches.
Importantly there are branches for i.e. 4.1, 4.2, 4.3 and master, which is the implied newest version in development.
Other packages having a 1.x branch for Plone 4 and master is for Plone 5.

If the fix is only for one version, make sure to get that branch and party on.

So you have a bug fix valid for all feature branches or aome of them?

However, chances are the bug is in multiple branches.

Let's say the bug starts in 4.1. Pull the 4.1 branch and fix and commit there with tests.

If your fix only involved a single commit, you can use git's ``cherry-pick`` command to apply the same commit
to a different branch.

First check out the branch::

  > git checkout 4.2

And then ``cherry-pick`` the commit (you can get the SHA hash from git log).::

  > git cherry-pick b6ff4309

There may be conflicts; if so, resolve them and then follow the directions
git gives you to complete the ``cherry-pick``.

If your fix involved multiple commits, ``cherry-picking`` them one by one can get tedious.
In this case things are easiest if you did your fix in a separate feature branch.

In that scenario, you first merge the feature branch to the 4.1 branch::

  > git checkout 4.1
  > git merge my-awesome-feature

Then you return to the feature branch and make a branch for `rebasing` it onto the 4.2 branch::

  > git checkout my-awesome-feature
  > git checkout -b my-awesome-feature-4.2
  > git rebase ef978a --onto 4.2

``ef978a`` happens to be the last commit in the feature branch's history before it was branched off of 4.1.
You can look at git log to find this.

At this point, the feature branch's history has been updated, but it hasn't actually been merged to 4.2 yet.
This lets you deal with resolving conflicts before you actually merge it to the 4.2 release branch. Let's do that now::

  > git checkout 4.2
  > git merge my-awesome-feature-4.2


Direct Commits - Oh My!
^^^^^^^^^^^^^^^^^^^^^^^

Do not commit/push directly to master. Never.
If you have signed the :doc:`contributor agreement <contributors_agreement_explained>` form, you can commit directly to the main branch (for plone this would be the version branch, for most other packages this would be ``master``).
Plone used to be in an svn repository, so everyone was familiar and accustomed to committing directly to the branches.
After the migration to github, the community decided to maintain this spirit.
But with git branching is -compared to subversion - so easy, that we do not further want to have commits to master.

FAQ
---
 * *How do I know when my package got made?*
    You can follow the project on github and watch its `timeline <https://github.com/organizations/plone>`_. You can also check the :file:`CHANGES.txt` of every plone release for a comprehensive list of all changes and validate that yours is present.

