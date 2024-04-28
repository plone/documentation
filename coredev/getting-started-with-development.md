---
myst:
  html_meta:
    "description": "Getting started with Plone development"
    "property=og:description": "Getting started with Plone development"
    "property=og:title": "Getting started with Plone development"
    "keywords": "Plone, development"
---

# Getting started with development

This document assumes you want to run the current latest Plone source, fix a bug in Plone, or test an add-on in the context of the latest code, and will detail the full process.
For how to write Plone Improvement Proposals (PLIPs), read {doc}`plips`.


## Version support policy

If you are triaging or fixing bugs, keep in mind that Plone has a [version support policy](https://plone.org/download/release-schedule#91815aec-0513-40e0-a804-55ea787a8c68).


## Dependencies

-   git. See [Set up Git](https://docs.github.com/en/get-started/quickstart/set-up-git).
-   [Python](https://python.org/). See the [current supported versions of Python](https://plone.org/download/release-schedule).
-   If you are on macOS, you will need to install [XCode](https://developer.apple.com/xcode/).
    You can do this through the App Store or registering through the Apple Developer Program.
-   [Pillow](https://pypi.org/project/Pillow/).
-   [GCC](https://gcc.gnu.org/) in order to compile ZODB, Zope and lxml.
-   [libxml2 and libxslt](https://gitlab.gnome.org/GNOME/libxslt/-/releases), including development headers.


(setup-development-environment)=

## Set up your development environment

The first step in fixing a bug is getting this [buildout](https://github.com/plone/buildout.coredev) running.
We recommend fixing the bug on the latest branch, and then [backporting](https://en.wikipedia.org/wiki/Backporting) as necessary.
Dependent on the current development cycle, there may exist a future branch.
For example, `6.0` is the actively maintained stable branch.
[Some other branch] is the future, currently unstable, active development branch.
More information on switching release branches is described below.

To set up a plone 6 development environment.

```shell
cd ~/projects  # or wherever you want to put things
git clone -b 6.0 https://github.com/plone/buildout.coredev ./plone6devel
cd ./plone6devel
./bootstrap.sh
```

If you run into issues in this process, please see {doc}`troubleshooting`.

This will run for a long time if it is your first pull (approximately 20 minutes).
Once that is done pulling down eggs, you can start your new instance with:

```shell
./bin/instance fg
```

or as a WSGI service with:

```shell
./bin/wsgi
```

To login, the defaults are:

-   username: admin
-   password: admin


## Switching branches

If your bug is specific to one branch, or you think it should be backported, you can switch branches.
The first time you get a branch, you must do:

```shell
git checkout -t origin/6.0
```

This should set up a local 6.0 branch tracking the one on GitHub.
From then on you can just do:

```shell
git checkout 6.0
```

To see what branch you are currently on:

```shell
git branch
```

The line with a `*` by it will indicate the branch on which you are currently working.

```{important}
Make sure to rerun buildout if you were in a different branch earlier to get the correct versions of packages, otherwise you will get some weird behavior.
```


## Jenkins and mr.roboto

Plone has a continuous integration (CI) setup and follows CI rules.

When you push a change to any Plone package, our testing/CI middleware `mr.roboto` starts running all the tests that are needed to make sure that you don't break anything.
For each Plone and Python version we run two jobs, one for the package itself (which will give you a fast feedback, within 10 minutes) and one on the full `coredev` build (which can take up to an hour, but makes sure no other packages are effected by your change.

For more information you can read {doc}`Mr. Roboto workflow <roboto>` or our [Jenkins machine](https://jenkins.plone.org/).

The CI system at `jenkins.plone.org` is a shared resource for Plone developers to notify them of regressions in Plone code.
Build breakages are a normal and expected part of the development process.
Our aim is to find errors and eliminate them as quickly as possible, without expecting perfection and zero errors.
Though, there are some essential practices that need to be followed in order to achieve a stable build:

1.  Don't check in on a broken build. Check Jenkins first.
2.  Always run all commit tests locally before committing.
3.  Wait for commit tests to pass before moving on.
4.  Never go home on a broken build.
5.  Always be prepared to revert to the previous revision.
6.  Time-box fixing before reverting.
7.  Don't comment out failing tests.
8.  Take responsibility for all breakages that result from your changes.

See {doc}`continous-integration` for more information.

Since it can be burdensome to check this manually, install the tools locally to always see the current state of the Plone CI Server:

-   For Linux and X11 environments, there is [BuildNotify](https://pypi.org/project/BuildNotify/).
-   For macOS there is [CCMenu](http://ccmenu.org/).
-   For windows there is [CCTray](https://cruisecontrolnet.org/cctray_download_plugin-2/).
-   For Firefox there is [CruiseControl Monitor](https://addons.thunderbird.net/EN-US/firefox/addon/cruisecontrol-monitor/?src=cb-dl-name) (no longer supported), and many other [Jenkins plugins](https://addons.mozilla.org/en-US/firefox/search/?q=jenkins).

These tools were built to parse a specific file that CruiseControl, another CI tool, generated.
Jenkins generates this file too.
You can configure your notifier of choice with this url: `https://jenkins.plone.org/cc.xml` [which is a 404, LOL!]


## Check out packages to fix

Most packages are not in {file}`src/` by default, so you can use `mr.developer` to get the latest and make sure you are always up to date.
It can be a little daunting at first to find out which packages cause the bug in question, but just ask in https://community.plone.org/ if you need some help.
Once you know which packages you want, pull their source.

You can get the source of the package with `mr.developer` and the checkout command, or you can go directly to editing {file}`checkouts.cfg`.
We recommend the latter but will describe both.
In the end, {file}`checkouts.cfg` must be configured, so you might as well start there.

At the base of your buildout, open {file}`checkouts.cfg` and add your package if it's not already there:

```cfg
auto-checkout =
        # my modified packages
        plone.app.caching
        plone.caching
        # others
        ...
```

Then rerun buildout to get the source packages:

```shell
./bin/buildout
```

Alternatively, we can manage checkouts from the command line, by using `mr.developer`'s `bin/develop` command to get the latest source.
For example, if the issue is in `plone.app.caching` and `plone.caching`:

```shell
./bin/develop co plone.app.caching
./bin/develop co plone.caching
./bin/buildout
```

Don't forget to rerun buildout!
In both methods, `mr.developer` will download the source from GitHub (or otherwise) and put the package in the {file}`src/` directory.
You can repeat this process with as many or as few packages as you need.
For some more tips on working with `mr.developer`, please read {doc}`mrdeveloper`.


## Testing Locally

To run a test for the specific module you modify:

```shell
./bin/test -m plone.app.caching
```

These should all run without error.
Please don't check in anything that doesn't succeed!
Now write a test case for the bug you are fixing, and make sure everything is running as it should.

After the module level tests run with your change, please make sure other modules aren't affected by the change by running the full suite, including robot-tests (remove the `--all` to run without robot tests):

```shell
./bin/test --all
```

```{note}
Tests take a long time to run.
Once you become a master of bugfixes,
you may just let jenkins do this part for you.
More on that below.
```


## Updating `CHANGES.rst` and `checkouts.cfg`

Once all the tests are running locally on your machine, you are **ALMOST** ready to commit the changes.
You must perform a couple housekeeping chores before moving on.

First, edit {file}`CHANGES.rst` (or {file}`CHANGES.txt`, or {file}`HISTORY.txt`) in each package you have modified and add a summary of the change.
This change note will be collated for the next Plone release and is important for integrators and developers to be able to see what they will get if they upgrade.
New changelog entries should be added at the very top of {file}`CHANGES.rst`.
Some packages already switched to use [towncrier](https://pypi.org/project/towncrier/).
If this is the case you'll find a note at the top of the `CHANGES.rst` file.

Most importantly, if you didn't do it earlier, edit the file  {file}`checkouts.cfg` in the buildout directory, and add your changes package to the `auto-checkout` list.
This lets the release manager know that the package has been updated, so that when the next release of Plone is cut, a new egg will be released, and Plone will need to pin to the next version of that package.
In other words, this is how your fix becomes an egg!

Note that there is a section separator called "# Test Fixes Only".
Make sure your egg is above that line, else your egg probably won't get made very quickly.
This just tells the release manager that any eggs below this line have tests that are updated, but no code changes.

Modifying the file {file}`checkouts.cfg` also triggers the buildbot, [jenkins](https://jenkins.plone.org/), to pull in the egg and run all the tests against the changes you just made.
Not that you would ever skip running all tests.

If your bug is in more than one release, for example 5.2 and 6.0, please checkout both branches, and add it to the file {file}`checkouts.cfg`.


## Commits and pull requests

Review the following checklist:

-   Did you fix the original bug?
-   Is your code consistent with our [Style Guides](https://5.docs.plone.org/develop/styleguide/index.html)?
-   Did you remove any extra code and lingering pdbs?
-   Did you write a test case for that bug?
-   DO all test cases for the modules and Plone pass?
-   Did you update {file}`CHANGES.rst` in each packages you touched?
-   Did you add your changed packages to {file}`checkouts.cfg`?

If you answered *YES* to all of these questions, then you are ready to push your changes!
A couple quick reminders:

-   Only commit directly to the development branch if you're confident that your code won't break anything badly and the changes are small and fairly trivial.
    Otherwise, please create a `pull request` (more on that below).
-   Please try to make one change per commit.
    If you are fixing three bugs, make three commits.
    That way, it is easier to see what was done when, and easier to roll back any changes if necessary.
    If you want to make large changes cleaning up whitespace or renaming variables, it is especially important to do so in a separate commit for this reason.
-   We have a few angels that follow the changes and each commit to see what happens to their favourite CMS!
    If you commit something REALLY sketchy, they will politely contact you, most likely after immediately reverting changes.
    There are no official people assigned to this so if you are especially nervous, ask in https://community.plone.org/.


## Commit to `Products.CMFPlone`

If you are working a bug fix on `Products.CMFPlone`, there are a couple other things to take notice of.
First and foremost, you'll see that there are several branches.
At the time of writing this document, there are branches for 4.2.x, 4.3.x and master, which is the implied 5.0.
This may change faster than this documentation, so check the branch dropdown on GitHub.

If the fix is only for one version, make sure to get that branch.
However, chances are the bug is in multiple branches.

Let's say the bug starts in 4.1.
Pull the 4.1 branch and fix and commit there with tests.

If your fix only involved a single commit, you can use git's `cherry-pick` command to apply the same commit to a different branch.

First check out the branch:

```shell
git checkout 4.2
```

And then cherry-pick the commit (you can get the SHA hash from git log):

```shell
git cherry-pick b6ff4309
```

There may be conflicts.
If so, resolve them, then follow the directions git gives you to complete the cherry-pick.

If your fix involved multiple commits, cherry-picking them one by one can get tedious.
In this case, things are easiest if you did your fix in a separate feature branch.

In that scenario, you first merge the feature branch to the 4.1 branch:

```shell
git checkout 4.1
git merge my-awesome-feature
```

Then return to the feature branch, and make a branch for rebasing it onto the 4.2 branch:

```shell
git checkout my-awesome-feature
git checkout -b my-awesome-feature-4.2
git rebase ef978a --onto 4.2
```

(`ef978a` happens to be the last commit in the feature branch's history before it was branched off of 4.1.
You can look at `git log` to find this.)

At this point, the feature branch's history has been updated, but it hasn't actually been merged to 4.2 yet.
This lets you deal with resolving conflicts before you actually merge it to the 4.2 release branch.
Let's do that now:

```shell
git checkout 4.2
git merge my-awesome-feature-4.2
```

### Branches and forks and direct commits - oh my!

```{note}
This section needs a rewrite.
Meanwhile we do not allow direct commits, except in very rare cases.
```

Plone used to be in an svn repository, so everyone is familiar and accustomed to committing directly to the branches.
After the migration to GitHub, the community decided to maintain this spirit.
If you have signed the [contributor agreement](https://plone.org/foundation/contributors-agreement), you can commit directly to the branch.
For Plone, this would be the version branch, whereas for most other packages this would be `main`.

HOWEVER, there are a few situations where a branch is appropriate.
If you:

-   are just getting started
-   are not sure about your changes
-   want feedback or code review
-   are implementing a non-trivial change

then you should create a branch of whatever packages you are using, and then use the [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) feature of GitHub to get review.
Everything about this process would be the same except you need to work on a branch.
Take the `plone.app.caching` example.
After checking it out with `mr.developer`, create your own branch with:

```shell
cd src/plone.app.caching
git checkout -b my_descriptive_branch_name
```

```{note}
Branching or forking is your choice.
I prefer branching, and I'm writing the docs so this uses the branch method.
If you branch, it helps us because we *know* that you have committer rights.
Either way it's your call.
```

Proceed as normal.
When you are ready to push your fix, push to a remote branch with:

```shell
git push origin my_descriptive_branch_name
```

This will make a remote branch in GitHub.
Navigate to this branch in the GitHub user interface, and on the top right, there will be a button that says {guilabel}`Pull Request`.
This will turn your request into a pull request on the main branch.
There are people who look once a week or more for pending pull requests and will confirm whether or not it's a good fix, and give you feedback where necessary.
The reviewers are informal and very nice, so don't worry.
They are there to help!
If you want immediate feedback, visit https://community.plone.org/ with the pull request link and ask for a review.

```{note}
You still need to update the file {file}`checkouts.cfg` in the correct branches of `buildout.coredev`!
```


## Finalize issues

If you are working from an issue, please don't forget to go back to the issue, and add a link to the change set.
We don't have integration with GitHub yet so it's a nice way to track changes.
It also lets the reporter know that you care.
If the bug is really bad, consider pinging the release manager and asking them to make a release.


## FAQ

How do I know when my package got made?
: You can follow the project on GitHub, and watch its [timeline](https://github.com/orgs/plone/dashboard).
  You can also check the {file}`CHANGES.rst` of every plone release for a comprehensive list of all changes, and validate that yours is present.
