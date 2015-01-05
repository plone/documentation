Como enviar correções para o Core do Plone
==========================================
Este documento assume que você deseja corrigir um bug e irá detalhar o processo completo. Para mais informações sobre PLIPS, :doc:`go here <plips>`.

Política de Versões Suportadas
------------------------------
Se você estiver fazendo uma triagem ou corrigindo bugs, tenha em mente que o Plone possui uma `Política de versões suportadas <https://plone.org/support/version-support-policy>`_.

Dependências
------------
* `Git <http://help.github.com/mac-set-up-git/>`_
* `Subversion <http://subversion.apache.org/>`_
* `Python <http://python.org/>`_ 2.6 or 2.7 incluindo as bibliotecas de desenvolvimento.
* If you are on Mac OSX, you will need to install XCode. You can do this through the app store or several other soul-selling methods. You will likely want to install your own python 2.6 as well since they strip out all the header files which makes compiling some extensions weird. You can ignore this advice to start, but have faith, you'll come back to it later. They always do...
* `Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`_. Certifique-se de instalar no ambiente Python adequado.
* `VirtualEnv <http://www.virtualenv.org/en/latest/index.html>`_ No ambiente Python adequado.
* `GCC <http://gcc.gnu.org/>`_ A fim de compilar ZODB, Zope e lxml.
* `libxml2 and libxslt <http://xmlsoft.org/XSLT/downloads.html>`_, Incluíndo as bibliotecas de desenvolvimento.


Setting up Your Development Environment
---------------------------------------
The first step in fixing a bug is getting this buildout running. We recommend fixing the bug on the latest branch and then backporting as necessary. `Github <https://github.com/plone/buildout.coredev/>`_ by default always points to the currently active branch. More information on switching release branches is below.

To set up a plone 4.2 development environment::

  > cd ~/buildouts # or wherever you want to put things
  > git clone -b 4.2  https://github.com/plone/buildout.coredev ./plone42devel
  > virtualenv --no-site-packages plone42devpy
  > cd plone42devel
  > ../plone42devpy/bin/python bootstrap.py # (where "python" is your python 2.6 binary).
  > bin/buildout -v

If you run into issues in this process, please see the doc :doc:`issues`.

This will run for a long time if it is your first pull (~20 mins). Once that is done pulling down eggs, You can start your new instance with::

  > ./bin/instance fg

The default username/password for a dev instance is admin/admin.

Switching Branches
^^^^^^^^^^^^^^^^^^
If your bug is specific to one branch or you think it should be backported, you can easily switch branches. The first time you get a branch, you must do::

  > git checkout -t origin/4.1

This should set up a local 4.1 branch tracking the one on github. From then on you can just do::

  > git checkout 4.1

To see what branch you are currently on, just do::

  > git branch

The line with a * by it will indicate which branch you are currently working on.

.. important::
   Make sure to rerun buildout if you were in a different branch earlier to get the correct versions of packages, otherwise you will get some weird behavior!

For more information on buildout, please see the `collective developer manual documentation on buildout <http://collective-docs.plone.org/en/latest/tutorials/buildout/index.html>`_.


Checking out Packages for Fixing
--------------------------------
Most packages are not in src/ by default, so you can user mr.developer to get the latest and make sure you are always up to date. It can be a little daunting at first to find out which packages are causing the bug in question, but just ask on irc if you need some help. Once you [think you] know which package(s) you want, we need to pull the source.

You can get the source of the package with mr.developer and the checkout command, or you can go directly to editing checkouts.cfg. We recommend the latter but will describe both. In the end, checkouts.cfg must be configured either way so you might as well start there.

At the base of your buildout, open checkouts.cfg and add your package if it's not already there::

  auto-checkout =
          # my modified packages
          plone.app.caching
          plone.caching
          # others
          ...

Then rerun buildout to get the source packages::

  > ./bin/buildout

Altternatively, we can manage checkouts from the command line, by using mr.developer's ``bin/develop`` command to get the latest source. For example, if the issue is in plone.app.caching and plone.caching::

  > ./bin/develop co plone.app.caching
  > ./bin/develop co plone.caching
  > ./bin/buildout

Don't forget to rerun buildout! In both methods, mr.developer will download the source from github (or otherwise) and put the package in the src directory. You can repeat this process with as many or as few packages as you need. For some more tips on working with mr.developer, please :doc:`read more here <mrdeveloper>`.

Testing Locally
---------------
In an ideal world, you would write a test case for your issue before actually trying to fix it. In reality this rarely happens. No matter how you approach it, you should ALWAYS run test cases for both the module and plone.org before commiting any changes.

If you don't start with a test case, save yourself potential problems and validate the bug before getting too deep into the issue!

To run a test for the specific module you are modifying::

  > ./bin/test -m plone.app.caching

These should all run without error. Please don't check in anything that doesn't! If you haven't written it already, this is a good time to write a test case for the bug you are fixing and make sure everything is running as it should.

After the module level tests run with your change, please make sure other modules aren't affected by the change by running the full suite::

  > ./bin/alltests

*Note*: Tests take a long time to run. Once you become a master of bugfixes, you may just let jenkins do this part for you. More on that below.

Updating CHANGES.rst and checkouts.cfg
--------------------------------------
Once all the tests are running locally on your machine, you are ALMOST ready to commit the changes. A couple housekeeping things before moving on.

First, please edit CHANGES.rst (or CHANGES.txt) in each pakage you have modified and add a summary of the change. This change note will be collated for the next Plone release and is important for integrators and developers.

*Most importantly*, if you didn't do it earlier, edit checkouts.cfg in the buildout directory and add your changes package to the auto-checkout list. This lets the release manager know that the package has been updated so that when the next release of Plone is cut a new egg will be released and Plone will need to pin to the next version of that package. READ: this is how your fix becomes an egg!

Note that there is a section seperator called "# Test Fixes Only". Make sure your egg is above that line or your egg probably won't get made very quickly. This just tells the release manager that any eggs below this line have tests that are updated, but no code changes.

Modifying checkouts.cfg also triggers the buildbot, jenkins, to pull in the egg and run all the tests against the changes you just made. Not that you would ever skip running all tests of course... More on that below.

If your bug is in more than one release (e.g. 4.1 and 4.2), please checkout both branches and add to the checkouts.cfg.

Committing and Pull Requests
----------------------------
Phew! We are in the home stretch. How about a last minute checklist:

 * Did you fix the original bug?
 * Is your code consistent with our :doc:`style`?
 * Did you remove any extra code and lingering pdbs?
 * Did you write a test case for that bug?
 * Are all test cases for the modules(s) and for Plone passing?
 * Did you update CHANGES.rst in each packages you touched?
 * Did you add your changed packages to checkouts.cfg?

If you answered YES to all of these questions, you are ready to push your changes! A couple quick reminders:

 * Only commit directly to the development branch if you're confident your code won't break anything badly and the changes are small and fairly trivial. Otherwise, please create a pull request (more on that below).
 * Please try to make one change per commit. If you are fixing three bugs, make three commits. That way, it is easier to see what was done when, and easier to roll back any changes if necessary. If you want to make large changes cleaning up whitespace or renaming variables, it is especially important to do so in a separate commit for this reason.
 * We have a few angels that follow the changes and each commit to see what happens to their favourite CMS! If you commit something REALLY sketchy, they will politely contact you, most likely after immediately reverting changes. There is no official people assigned to this so if you are especially nervous, jump into #plone and ask for a quick eyeball on your changes.

Committing to Products.CMFPlone
-------------------------------
If you are working a bug fix on Products.CMFPlone,
there are a couple other things to take notice of.
First and foremost,
you'll see that there are several branches.
At the time of writing this document,
there are branches for 4.1, 4.2, and master, which is the implied 4.3.

Still with me? So you have a bug fix for 4.x.
If the fix is only for one version,
make sure to get that branch and party on.
However, chances are the bug is in multiple branches.

Let's say the bug starts in 4.1. Pull the 4.1 branch and fix and commit there with tests.

If your fix only involved a single commit,
you can use git's ``cherry-pick`` command to apply the same commit
to a different branch.

First check out the branch::

  > git checkout 4.2

And then cherry-pick the commit (you can get the SHA hash from git log).

  > git cherry-pick b6ff4309

There may be conflicts; if so, resolve them and then follow the directions
git gives you to complete the cherry-pick.

If your fix involved multiple commits, cherry-picking them one by one can get tedious.
In this case things are easiest if you did your fix in a separate feature branch.

In that scenario, you first merge the feature branch to the 4.1 branch::

  > git checkout 4.1
  > git merge my-awesome-feature

Then you return to the feature branch and make a branch for `rebasing` it onto the 4.2 branch::

  > git checkout my-awesome-feature
  > git checkout -b my-awesome-feature-4.2
  > git rebase ef978a --onto 4.2

(ef978a happens to be the last commit in the feature branch's history before
it was branched off of 4.1. You can look at git log to find this.)

At this point, the feature branch's history has been updated, but it hasn't actually
been merged to 4.2 yet. This lets you deal with resolving conflicts before you
actually merge it to the 4.2 release branch. Let's do that now::

  > git checkout 4.2
  > git merge my-awesome-feature-4.2


Branches and Forks and Direct Commits - Oh My!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Plone used to be in an svn repository, so everyone is familiar and accustomed to committing directly to the branches. After the migration to github, the community decided to maintain this spirit. If you have signed the contributor agreement, you can commit directly to the branch (for plone this would be the version branch, for most other packages this would be master).

HOWEVER, there are a few situations where a branch is appropriate. If you:
 * are just getting started,
 * are not sure about your changes
 * want feedback/code review
 * are implementing a non-trivial change

then you likely want to create a branch of whatever packages you are using and then use the pull request feature of github to get review. Everything about this process would be the same except you need to work on a branch. Take the plone.app.caching example. After checking it out with mr.developer, create your own branch with::

  > cd src/plone.app.caching
  > git checkout -b my_descriptive_branch_name

*Note*: Branching or forking is your choice. I prefer branching, and I'm writing the docs so this uses the branch method. If you branch, it helps us because we *know* that you have committer rights. Either way it's your call.

Proceed as normal. When you are ready to push your fix, push to a remote branch with::

  > git push origin my_descriptive_branch_name

This will make a remote branch in github. Navigate to this branch in the github UI and on the top right there will be a button that says "Pull Request". This will turn your request into a pull request on the main branch. There are people who look once a week or more for pending pull requests and will confirm whether or not its a good fix and give you feedback where necessary. The reviewers are informal and very nice so don't worry - they are there to help! If you want immediate feedback, jump into IRC with the pull request link and ask for a review.

*Note*: you still need to update checkouts.cfg in the correct branches of buildout.coredev!

Jenkins
-------
You STILL aren't done! Please check jenkins to make sure your changes haven't borked things. It runs every half an hour and takes a while to run so checking back in an hour is a safe bet. Have a beer and head over to the `Jenkins control panel <https://jenkins.plone.org/>`_.

Finalizing Tickets
------------------
If you are working from a ticket, please don't forget to go back to the ticket and add a link to the changeset. We don't have integration with github yet so it's a nice way to track changes. It also lets the reporter know that you care. If the bug is really bad, consider pinging the release manager and asking him to make a release pronto.

FAQ
---
 * *How do I know when my package got made?*
    You can follow the project on github and watch its timeline. You can also check the CHANGES.txt of every plone release for a comprehensive list of all changes and validate that yours is present.

