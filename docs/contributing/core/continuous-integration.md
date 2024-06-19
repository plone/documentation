---
myst:
  html_meta:
    "description": "Essential continuous integration practices"
    "property=og:description": "Essential continuous integration practices"
    "property=og:title": "Essential continuous integration practices"
    "keywords": "Plone, continuous integration, best practices"
---

# Essential continuous integration practices

The {term}`CI` system at [jenkins.plone.org](https://jenkins.plone.org) is a shared resource for Plone core developers to notify them of regressions in Plone core code.

Build breakages are a normal and expected part of the development process.
The aim is to find errors and remove them as quickly as possible, without expecting perfection and zero errors.
Though, there are some essential practices that you need follow to achieve a stable build:

## 1) Don't check in on a broken build

Do not make things more complicated for the developer who is responsible for breaking the build.

If the build breaks, the developer has to identify the cause of the breakage as soon as possible and should fix it.
This strategy gives the developer the best option to find out what caused the breakage and fix it immediately.
Fixing the build is easier with a clear look at the problem.
Checking in further changes and triggering new builds will complicate matters and lead to more problems.

If the build is broken over a longer period of time (more than a couple of hours) you should either:

- notify the developer who is responsible for the breakage
- fix the problem yourself
- or revert the commit so you and others can continue to work.

```{note}
There is one exception to this rule.
Sometimes there are changes or tests that depend on changes in other packages.
If this is the case, there is no way around breaking a single build for a certain period of time.
In this case run the all tests locally with all the changes and commit them within a time frame of ten minutes.
```

## 2) Always run all commit tests locally before committing

Follow this practice so the build stays green, and other developers can continue to work without breaking the first rule.

Remember that Plone development can happen all over the world, at all times. So other developers may have checked in changes since your last synchronization. These may interact with your work.

Therefore it's essential that you check out ({command}`git pull`) and run the tests again before you push your changes to GitHub.

A common source of errors on check-in is to forget to add some files to the repository.
Use {command}`git status` to check and correct for this. Also double-check to not check in files that should not be part of a package, such as editor configuration files.

## 3) Wait for commit tests to pass before moving on

Always monitor the build's progress, and fix the problem right away if it fails.
You have a far better chance of fixing the build, if you just introduced a regression than later.
Also another developer might have committed in the meantime (by breaking rule 1), making things more complicated for you.

## 4) Never go home on a broken build

Take into account the first rule of CI ("Don't check in on a broken build"): breaking the build essentially stops all other developers from working on it.
Therefore going home on a broken build (or even on a build that has not finished yet) is **not** acceptable.
It will prevent all other developers to stop working or they will need to fix the errors that you introduced.

## 5) Always be prepared to revert to the previous revision

In order for other developers to be able to work on the build, you should always be prepared to revert to the previous (passing) revision.

## 6) Time-box fixing before reverting

When the build breaks on check-in, try to fix it for ten minutes.
If, after ten minutes, you aren't finished with the solution, revert to the previous version from your version control system.
This way you will allow other developers to continue to work.

## 7) Don't comment out failing tests

Once you begin to enforce the previous rule, the result is often that developers start commenting out failing tests in order to get the build passing again as quick as possible.
While this impulse is understandable, it is **not acceptable**.

The tests were passing for a while and then start to fail.
This means that you either caused a regression, made assumptions that are no longer valid, or the application has changed the functionality being tested for a valid reason.

You should always either fix the code (if a regression has been found), modify the test (if one of the assumptions has changed), or delete it (if the functionality under test no longer exists).

## 8) Take responsibility for all breakages that result from your changes

If you commit a change and all the tests you wrote pass, but others break, the build is still broken.
This also applies to tests that fail in `buildout.coredev` and don't belong directly to the package you worked on.
This means that you have introduced a regression bug into the application.

It is **your responsibility** to fix all tests that are not passing because of your changes.

There are some tests in Plone that fail randomly, the community is always working on fixing those.
If you think you hit such a test, try to fix it (better) or re-run the Jenkins job to see if it passes again.

In any case the developer who made the commit is responsible to make it pass.

## Further reading

These rules were taken from the excellent book "Continuous Delivery" by Jez Humble and David Farley (Addison Wesley), and have been adopted and rewritten for the Plone community.
