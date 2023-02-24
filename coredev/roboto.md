---
myst:
  html_meta:
    "description": "Mr. Roboto"
    "property=og:description": "Mr. Roboto"
    "property=og:title": "Mr. Roboto"
    "keywords": "Mr. Roboto, mr.roboto, Plone"
---

# Mr. Roboto

```{todo}
Add brief description of what is Mr. Roboto and what it does.
```

## GitHub push

When a push happens on GitHub, `mr.roboto` is triggered and it starts to analyze the push.

-   If it's on `buildout-coredev`, it starts the job of the branch that has been pushed.
    In this case, we send to `plone-cvs` the commit to keep track of the commits on that list.
-   If it's on a package that's on the {file}`sources.cfg` of a `buildout-coredev`, it starts the coredev jobs that are linked to that package and a kgs job with that package.
    This kgs job is a snapshot of the last working version of the `buildout.coredev` with the newest version of the package that is involved on the push.
    These jobs are really fast, as we only test the package applied to the kgs Plone and Python version `coredev` buildout.
-   If it's on a PLIP specification, it runs the job that is configured Through The Web on the `mr.roboto` interface at http://jenkins.plone.org/roboto/plips.

```{todo}
`http://jenkins.plone.org/roboto/plips` is obsolete, and returns a 404 not found.
``` 


## Job finishes

When Jenkins finishes a job, it makes a callback to `mr.roboto`, which in turn does the following:

-   If it comes from a `coredev` job, when all the `coredev` jobs related to that push are finished, it writes a comment on the GitHub commit with all the information.
    It does this one time only, with all the information, so no more empty mails from the GitHub notification system.
-   If it comes from a kgs job and all the kgs jobs are finished, (that may take max 10 min) and some have failed, we send an email to the testbot mailing list saying that a commit failed on the kgs job.
    We also send an email to [plone-cvs](https://sourceforge.net/projects/plone/lists/plone-cvs) with the information to keep track of all the commits.
-   If it comes from a kgs job and all the kgs jobs are finished, and all are working, we send an email to [plone-cvs](https://sourceforge.net/projects/plone/lists/plone-cvs) with the information to keep track of all the commits.

For all kgs jobs jenkins sends an email to the author with the results when is finished.

All the notifications have an URL similar to http://jenkins.plone.org/roboto/get_info?push=9a183de85b3f48abb363fa8286928a10.

```{todo}
http://jenkins.plone.org/roboto/get_info?push=9a183de85b3f48abb363fa8286928a10 is obsolete, and returns a 404 not found.
```

On this URL, there is the commit hash, who committed it, the diff, the files, and the result for each Jenkins job.

-   [plone-testbot](https://lists.plone.org/mailman/listinfo/plone-testbot) mailing list receives messages only when a test fails on the kgs environment, and may take up to ten minutes from the push.
-   [plone-cvs](https://sourceforge.net/projects/plone/lists/plone-cvs) always has the commit, diff, and the information, and it may take ten minutes to get there after the push.
-   The author receives the results of tests failing against kgs after ten minutes after the push.

```{note}
In case of integration errors with other packages that may fail because of the push, kgs will not be aware of that.
It's important that at the end (and after the fifty minutes that takes the `coredev` jobs to complete), that you also check the latest version of `coredev` with your push.
```
