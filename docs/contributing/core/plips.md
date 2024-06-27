---
myst:
  html_meta:
    "description": "Plone Improvement Proposals (PLIPs)"
    "property=og:description": "Plone Improvement Proposals (PLIPs)"
    "property=og:title": "Plone Improvement Proposals (PLIPs)"
    "keywords": "Plone Improvement Proposal, PLIP)"
---

# Plone Improvement Proposals (PLIPs)

A Plone Improvement Proposal, or {term}`PLIP`, is a change to a Plone package that would affect everyone who uses that package.
PLIPs go through a formal process compared to bug fixes because of their broad reach.
The Plone Framework Team reviews all PLIPs to make sure that it's in the best interest of the broader community, and that it's of high quality.

A project board of active PLIPs is located at https://github.com/orgs/plone/projects/47.


## Process overview

1.  Developer submits a PLIP and solicits feedback.
2.  Developer addresses concerns from the feedback, and resubmits the PLIP, if necessary.
3.  The designated team approves the PLIP for inclusion into Plone core for a given release.
4.  Developer implements the PLIP, including code, tests, and documentation.
5.  Developer creates a pull request of the PLIP for review by the designated team.
6.  The designated team reviews the pull request of the PLIP and gives feedback.
7.  Repeat the two previous steps, until both the designated team and developer are happy with the result.
8.  A designated team member approves the PLIP for merge.
9.  A designated team member merges the PLIP.

In rare circumstances, a PLIP may be rejected.
This is usually the result of the developer not responding to feedback or dropping out of the process.


(designated-teams-label)=

## Designated teams

The following packages and repositories have designated teams that you can contact by `@`-ing them in its GitHub issue tracker.
If the repository is not listed, use the default repository for `Products.CMFPlone`.

| Package | Repository | Team |
|---|---|---|
| `Products.CMFPlone` | https://github.com/plone/Products.CMFPlone | not applicable |
| Classic UI | https://github.com/plone/plone.classicui | `@plone/ClassicUI-Team` |
| Volto | https://github.com/plone/volto | `@plone/volto-team` |


(submit-a-plip-label)=

## Submit a PLIP

Prepare the following information for your PLIP.

-   Title
-   Proposer (you)
-   Seconder (another person supporting your PLIP)
-   Abstract (a comprehensive overview of the subject)
-   Motivation (reason or motivation for creating this proposal)
-   Assumptions (preconditions)
-   Proposal & Implementation (detailed proposal with implementation details and–if needed—possible variants to be discussed)
-   Deliverables (packages and documentation chapters involved, including any third party packages)
-   Risks (what will break or affect existing installations of Plone after an upgrade, including the end user point of view, training efforts, and other audiences)
-   Participants (list of persons and roles known)

Now that you are prepared, submit your PLIP.

1.  Visit the package's GitHub issue tracker, and Click {guilabel}`New issue`.

    If you do not see the option to create a PLIP, then the repository has not been configured with the PLIP GitHub issue template, and you should instead visit the default Plone issue tracker for PLIPs, [`Products.CMFPlone`](https://github.com/plone/Products.CMFPlone/issues).

2.  For the PLIP option, click {guilabel}`Get started`.

3.  Fill in the title and description.
    Preserve the headings and comments.
    The comments provide guidance for you to follow while composing your PLIP.

4.  When done, click {guilabel}`Submit new issue` to submit your PLIP.
 
5.  If GitHub does not automatically assign the label {guilabel}`03 type: feature (plip)`, then assign that label to the issue to make it easier to find.


## Get feedback

After you submit your PLIP, solicit feedback for your idea on the [Plone Community Forum](https://community.plone.org/) and through the repository's issue tracker.

You may revise your PLIP based on feedback.

If you need help at any point in this process, you can either `@` the team or personally contact a member of the designated team.


## Team approves proposal

After incorporating feedback to your proposal, you can request a final review and approval for inclusion in Plone.
Every PLIP must be approved by the designated team.


## Implement your PLIP

(plip-setup-instructions-label)=

```{important}
This section does not apply to Volto.
Instead see {doc}`../../volto/contributing/index`.
```

```{note}
This section assumes you have read and followed the instructions in {doc}`index` to set up your development environment, up until {ref}`contributing-core-edit-packages-label`.
```

You can start the development at any time, but if you intend to modify Plone core, it is a good idea to wait to see if your idea is approved.


### General rules

-   Any new packages must be in a branch in the `plone` namespace in GitHub.
-   The PLIP reviewers must be able run buildout, and everything should "just work"™.
-   New code must:
    -   Be {doc}`properly documented <documentation>`. If it ain't documented, it's broken.
    -   Have clear code.
    -   Follow current best practices in coding style.
        The [Plone Meta](https://github.com/plone/meta) project can help you set up your environment.
    -   Be tested according to Plone core's {doc}`plone5:develop/testing/index`.


### Create a new PLIP branch

Create a buildout configuration file for your PLIP in the `plips` folder of `buildout.coredev`.
Its name should follow the pattern `plip-repository-issue_number-description.cfg`.
For example, {file}`plip-volto-1234-widget-frobbing.cfg`.

This file will define the branches for your PLIP, along with other buildout configuration.
The following is example content for the file {file}`plips/plip-volto-1234-widget-frobbing.cfg`.

```ini
[buildout]
extends = plipbase.cfg
auto-checkout +=
    plone.somepackage
    plone.app.someotherpackage

[sources]
plone.somepackage = git https://github.com/plone/plone.somepackage.git branch=plip-volto-1234-widget-frobbing
plone.app.someotherpackage = git https://github.com/plone/plone.app.somepackage.git branch=plip-volto-1234-widget-frobbing

[instance]
eggs +=
    plone.somepackage
    plone.app.someotherpackage
zcml +=
    plone.somepackage
    plone.app.someotherpackage
```

Use the same naming convention when you branch existing packages.


### Work on a PLIP

To work on a PLIP, assuming you have followed the {ref}`PLIP set up instructions <plip-setup-instructions-label>`, you can invoke buildout with your PLIP configuration as follows.

```shell
./bin/buildout -c plips/plip-volto-1234-widget-frobbing.cfg
```

```{seealso}
See {ref}`contributing-core-test-locally-label`, {ref}`contributing-core-change-log-label`, and {ref}`contributing-core-create-a-pull-request-label`.
```


### Finish up

Before marking your PLIP as ready for review as a pull request, add a file to give a set of instructions to the PLIP reviewer.
This file should be called {file}`plip_<repository>_<number>_notes.txt`.
This should include, but is not limited to:

-   URLs pointing to all documentation created and updated
-   Any concerns and issues still remaining
-   Any weird buildout things

Once you have finished, update your PLIP issue and pull request to indicate that it is ready for review.
The designated team will review your PLIP.
They will follow the guidelines listed at {doc}`plip-review`.

After the PLIP has been accepted by the designated team and the release managers, you will be asked to merge your work into the main development line.

The merge may have unintended interactions with other PLIPs coming in.
During the merge phase you must be prepared to help out with all the features and bugs that arise.

If all went as planned, the next Plone release will carry on with your PLIP in it.
You'll be expected to help out with that feature after it's been released (within reason).
