---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

```todo
This should probably be purged.
It is redundant to the default [CONTRUBITING.md](https://github.com/plone/.github/blob/main/CONTRIBUTING.md) and other files.
```

% Note: this page is linked to from CONTRIBUTING.rst in all packages.  Keep it short!

# Guidelines for contributing to Plone Core

You probably came here by clicking one of the 'guidelines for contributing' links on GitHub.
You probably have an issue to report or you want to create a pull request.
Thanks a lot!
Let's bring you up to speed with the minimum you need to know to start contributing.

## Create an issue

-   If you know the issue is for a specific package, you can add an issue there.
    When in doubt, create one in the [CMFPlone issue tracker](https://github.com/plone/Products.CMFPlone/issues).

-   Please specify a few things:

    -   What steps reproduce the problem?
    -   What do you expect when you do that?
    -   What happens instead?
    -   Which Plone version are you using?

-   If it is a visual issue, can you add a screen shot?

-   If there is an error in the Site Setup error log, please include it.
    Especially a traceback is helpful.
    Click on the 'Display traceback as text' link if you see it in the error log.


## Create a pull request

-   Legally, you can NOT contribute code unless you have signed the {doc}`contributor agreement <agreement>`.
    This means that we can NOT accept pull requests from you unless this is done, so please don't put the code reviewers at risk and do it anyways.
-   Add a changelog entry as file in the news directory.
    For helpful instructions, please see: <https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst>
-   For new features, an addition to README.rst is probably needed.
    A package may include other documentation that needs updating.
-   All text that can be shown in a browser must be translatable.
    Please mark all such strings as translatable.
-   Be nice and use code quality checkers like flake8 and jshint.
-   See if you can use git to squash multiple commits into one where this makes sense.
    If you are not comfortable with git, never mind.
-   If after reading this you become hesitant: don't worry.
    You can always create a pull request, mark it as WIP (work in progress), and improve the above points later.
