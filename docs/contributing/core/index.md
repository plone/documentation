---
myst:
  html_meta:
    "description": "Contributing to Plone 6 Core"
    "property=og:description": "Contributing to Plone 6 Core"
    "property=og:title": "Contributing to Plone 6 Core"
    "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

# Contributing to Plone 6 core

This part describes the process of development in Plone core.
It's primarily a technical resource for setting up your development environment, fixing bugs, and writing Plone Improvement Proposals (PLIPs).

It expands upon {doc}`/contributing/index` and, where applicable, {doc}`/contributing/first-time`.

## Version support policy

If you are triaging or fixing bugs, keep in mind that Plone has a [version support policy](https://plone.org/download/release-schedule)

## Dependencies

```{include} ../../volto/contributing/install-operating-system.md
```

- {ref}`setup-build-installation-python-label` {SUPPORTED_PYTHON_VERSIONS}
- {ref}`setup-build-installation-gnu-make-label`
- [git](https://help.github.com/articles/set-up-git/)
- [Pillow](https://pypi.org/project/Pillow/).
- [libxml2 and libxslt](https://gitlab.gnome.org/GNOME/libxslt/-/releases), including development headers.
- [GCC](https://gcc.gnu.org/) in order to compile ZODB, Zope and lxml.

The first step in fixing a bug is getting this [buildout](https://github.com/plone/buildout.coredev) running.
We recommend fixing the bug on the latest branch and then [backporting](http://en.wikipedia.org/wiki/Backporting) as necessary.
[GitHub](https://github.com/plone/buildout.coredev/) by default always points to the currently active branch.
Depending on the current development cycle there may exist a future branch.
I.e. at the moment 6.0 is the actively maintained stable branch and 6.1 is the future, currently unstable, active development branch.
More information on switching release branches is below.

To set up a plone 6 development environment:

```shell
cd ~/buildouts # or wherever you want to put things
git clone -b 6.1 https://github.com/plone/buildout.coredev ./plone6devel
cd ./plone6devel
./bootstrap.sh
```

If you run into issues in this process, please see {doc}`troubleshooting`.

This will run for a long time if it is your first pull (approximately 20 minutes).
Once that is done pulling down eggs, you can start your new instance with:

```shell
./bin/instance fg
```

or as WSGI service with::

```shell
./bin/wsgi
```

To login, the defaults are:

- username: admin
- password: admin

## Switching branches

If the bug is specific to one branch or should be [backported](http://en.wikipedia.org/wiki/Backporting),
you can easily switch branches. The first time you get a branch, you must do:

```shell
git checkout -t origin/6.1
```

This should set up a local 6.1 branch tracking the one on GitHub.
From then on you can do:

```shell
git checkout 6.1
```

To see what branch you are currently on,

```shell
git branch
```

The line with a * by it will indicate which branch you are currently working on.

```{important}
Make sure to rerun buildout if you were in a different branch earlier to get the correct versions of packages, otherwise you will get some weird behavior.
```

## Jenkins and mr.roboto

Plone has a continuous integration (CI) setup and follows CI rules.

When you push a change to any Plone package, the testing/CI middleware `mr.roboto` starts running all the tests that are needed to make sure that you don't break anything.
For each Plone and Python version we run two jobs, one for the package itself (which will give you a fast feedback, within 10 minutes) and one on the full `coredev` build (which can take up to an hour, but makes sure no other packages are effected by your change.

The CI system at `jenkins.plone.org` is a shared resource for Plone developers to notify them of regressions in Plone code.
Build breakages are a normal and expected part of the development process.
The aim is to find errors and eliminate them as quickly as possible, without expecting perfection and zero errors.
Though, there are some essential practices that need to be followed in order to achieve a stable build:

1. Don't check in on a broken build. Check Jenkins first.
2. Always run all commit tests locally before committing.
3. Wait for commit tests to pass before moving on.
4. Never go home on a broken build.
5. Always be prepared to revert to the previous revision.
6. Time-box fixing before reverting.
7. Don't comment out failing tests.
8. Take responsibility for all breakages that result from your changes.

See {doc}`continuous-integration` for more information.

## Check out packages to fix

Most packages are not in {file}`src/` by default, so you can use `mr.developer` to get the latest and make sure you are always up to date.
It can be a little daunting at first to find out which packages cause the bug in question, you can ask in <https://community.plone.org/> if you need some help.
Once you know which packages you want, pull their source.

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
Once you have enough experience in doing bugfixes,
you may let jenkins do this part for you.
More on that below.
```

## Updating `CHANGES.rst` and `checkouts.cfg`

Once all the tests are running locally on your machine, you are **ALMOST** ready to commit the changes.
You must perform a couple housekeeping chores before moving on.

You need to create a change note of what has been modified.
This change note will be collated for the next Plone release and is important for integrators and developers to be able to see what they will get if they upgrade.

Most packages are using [towncrier](https://pypi.org/project/towncrier/).
If that is the case, there will be a directory "news" in the package. Please follow the Towncrier format and put a note in that directory.

For packages that haven't switched to using Towncrier, edit {file}`CHANGES.rst` (or {file}`CHANGES.txt`, or {file}`HISTORY.txt`) in each package you have modified and add a summary of the change. New changelog entries should be added at the very top of {file}`CHANGES.rst`.

Most importantly, if you didn't do it earlier, edit the file  {file}`checkouts.cfg` in the buildout directory, and add your changes package to the `auto-checkout` list.
This lets the release manager know that the package has been updated, so that when the next release of Plone is cut, a new egg will be released, and Plone will need to pin to the next version of that package.
In other words, this is how your fix becomes an egg!

Note that there is a section separator called "# Test Fixes Only".
Make sure your egg is above that line, else your egg probably won't get made very quickly.
This tells the release manager that any eggs below this line have tests that are updated, but no code changes.

Modifying the file {file}`checkouts.cfg` also triggers the buildbot, [jenkins](https://jenkins.plone.org/), to pull in the egg and run all the tests against the changes you just made.

If your bug is in more than one release, for example 6.1 and 6.0, please checkout both branches, and add it to the file {file}`checkouts.cfg`.

## Commits and pull requests

Review the following checklist:

- Did you fix the original bug?
- Is your code consistently formatted? You can use the [Plone Meta](https://github.com/plone/meta) project to set up your development environment to be consistent with Plone community agreed best practices.
- Did you remove any extra code and lingering pdbs?
- Did you write a test case for that bug?
- DO all test cases for the modules and Plone pass?
- Did you write an update note (using Towncrier or via {file}`CHANGES.rst`) in each package you changed?
- Did you add your changed packages to {file}`checkouts.cfg`?

If you answered *YES* to all of these questions, then you are ready to push your changes!
A couple of quick reminders:

- Never commit directly to the development branch. Create a `pull request` (more on that below).
- Please try to make one change per commit.
    If you are fixing three bugs, make three commits.
    That way, it is easier to see what was done when, and easier to roll back any changes if necessary.
    If you want to make large changes cleaning up whitespace or renaming variables, it is especially important to do so in a separate commit for this reason.

## Branching and pull requests

You should create a branch of whatever packages you are updating, and then use the [pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) feature of GitHub to get review.

Take the `plone.app.caching` example.
After checking it out with `mr.developer`, create your own branch with:

```shell
cd src/plone.app.caching
git checkout -b my_descriptive_branch_name
```

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
If you want immediate feedback, visit <https://community.plone.org/> with the pull request link and ask for a review.

## Finalize issues

If you are working from an issue, please don't forget to go back to the issue, and add a link to the change set.
We don't have integration with GitHub yet so it's a nice way to track changes.
It also lets the reporter know that you care.

## Additional material

```{toctree}
:maxdepth: 1

package-dependencies
release
```
