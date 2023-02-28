---
myst:
  html_meta:
    "description": "Essential continuous integration practices"
    "property=og:description": "Essential continuous integration practices"
    "property=og:title": "Essential continuous integration practices"
    "keywords": "Plone, continuous integration, best practices"
---

# Essential continuous integration practices

The CI system at [jenkins.plone.org](https://jenkins.plone.org) is a shared resource for Plone core developers to notify them of regressions in Plone core code.

Build breakages are a normal and expected part of the development process.
Our aim is to find errors and eliminate them as quickly as possible, without expecting perfection and zero errors.
Though, there are some essential rules that needs to be followed in order to achieve a stable build.


## 1) Don't check in on a broken build

Do not make things more complicated for the developer who is responsible for breaking the build.

If the build breaks, the developer has to identify the cause of the breakage as soon as possible and should fix it.
If we adopt this strategy, we will always be in the best position to find out what caused the breakage and fix it immediately.
If one of the developers has made a check-in and broken the build as a result, we have the best chance of fixing the build if we have a clear look at the problem.
Checking in further changes and triggering new builds will just lead to more problems.

If the build is broken over a longer period of time (more than a couple of hours) you should either notify the developer who is responsible for the breakage, fix the problem yourself, or just revert the commit in order to be able to continue to work.

```note
There is one exception to this rule.
Sometimes there are changes or tests that depend on changes in other packages.
If this is the case, there is no way around breaking a single build for a certain period of time.
In this case run the all tests locally with all the changes and commit them within a time frame of ten minutes.
```


## 2) Always run all commit tests locally before committing

Following this practice ensures the build stays green, and other developers can continue to work without breaking the first rule.

There might be changes that have been checked in before your last update from the version control that might lead to a build failure in Jenkins in combination with your changes.
Therefore it is essential that you check out ({command}`git pull`) and run the tests again before you push your changes to GitHub.

Furthermore, a common source of errors on check-in is to forget to add some files to the repository.

If you follow this rule and your local build passes, you can be sure that this is because someone else checked in in the meantime, or because you forgot to add a new class or configuration file that you have been working on into the version control system.


## 3) Wait for commit tests to pass before moving on

Always monitor the build's progress, and fix the problem right away if it fails.
You have a far better chance of fixing the build, if you just introduced a regression than later.
Also another developer might have committed in the meantime (by breaking rule 1), making things more complicated for yours.


## 4) Never go home on a broken build

Taking into account the first rule of CI ("Don't check in on a broken build"), breaking the build essentially stops all other developers from working on it.
Therefore going home on a broken build (or even on a build that has not finished yet) is **not** acceptable.
It will prevent all the other developers to stop working on the build or fixing the errors that you introduced.


## 5) Always be prepared to revert to the previous revision

In order for the other developers to be able to work on the build, you should always be prepared to revert to the previous (passing) revision.


## 6) Time-box fixing before reverting

When the build breaks on check-in, try to fix it for ten minutes.
If, after ten minutes, you aren't finished with the solution, revert to the previous version from your version control system.
This way you will allow other developers to continue to work.


## 7) Don't comment out failing tests

Once you begin to enforce the previous rule, the result is often that developers start commenting out failing tests in order to get the build passing again as quick as possible.
While this impulse is understandable, it is **wrong**.

The tests have been passing for a while and then start to fail.
This means that we either caused a regression, made assumptions that are no longer valid, or the application has changed the functionality being tested for a valid reason.

You should always either fix the code (if a regression has been found), modify the test (if one of the assumptions has changed), or delete it (if the functionality under test no longer exists).


## 8) Take responsibility for all breakages that result from your changes

If you commit a change and all the tests you wrote pass, but others break, the build is still broken.
This also applies to tests that fail in `buildout.coredev` and don't belong directly to the package you worked on.
This means that you have introduced a regression bug into the application.

It is **your responsibility**—because you made the change—to fix all tests that are not passing as a result of your changes.

There are some tests in Plone that fail randomly, we are always working on fixing those.
If you think you hit such a test, try to fix it (better) or re-run the Jenkins job to see if it passes again.

In any case the developer who made the commit is responsible to make it pass.


## Further Reading

Those rules were taken from the excellent book "Continuous Delivery" by Jez Humble and David Farley (Addison Wesley), and have been adopted and rewritten for the Plone community.

If you want to learn more about continuous integration and continuous delivery, I'd recommend that you buy this book.
