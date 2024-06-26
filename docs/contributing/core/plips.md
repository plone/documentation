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


## Process overview

1.  Developer submits a PLIP.
2.  [SOME_INDETERMINATE_TEAM] approves the PLIP for inclusion into Plone core for a given release.
3.  Developer implements the PLIP, including code, tests, and documentation.
4.  Developer creates a pull request of the PLIP for review by the [SOME_INDETERMINATE_TEAM].
5.  [SOME_INDETERMINATE_TEAM] reviews the PLIP and gives feedback.
6.  Developer addresses concerns from the feedback, and resubmits the PLIP, if necessary.
7.  Repeat the two previous steps, until both the [SOME_INDETERMINATE_TEAM] and developer are happy with the result.
8.  [SOMEBODY] approves the PLIP for merge.
9.  [SOMEBODY] merges the PLIP.

In rare circumstances, a PLIP may be rejected.
This is usually the result of the developer not responding to feedback or dropping out of the process.


(submit-a-plip)=

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
 
5.  If it does not automatically assign the label {guilabel}`03 type: feature (plip)`, then assign that label to the issue to make it easier to find.


## Get feedback

After you submit your PLIP, solicit feedback for your idea on the [Plone Community Forum](https://community.plone.org/).

You may revise your PLIP based on feedback.

If you need help at any point in this process, please contact a member of the [SOME_INDETERMINATE_TEAM] personally or ask for help at the [Framework Team Space](https://community.plone.org/c/development/framework-team/12).


## Implement your PLIP

You can start the development at any time, but if you intend to modify Plone core, it is a good idea to wait to see if your idea is approved.


### General rules

-   Any new packages must be in a branch in the `plone` namespace in GitHub.
-   The PLIP reviewers must be able run buildout, and everything should "just work"™.
-   New code must:
    -   Be {doc}`properly documented <documentation>`. If it ain't documented, it's broken.
    -   Have clear code.
    -   Follow current best practices in coding style.
        The [Plone Meta](https://github.com/plone/meta) project can help you set up your environment.
        For Volto, follow {doc}`/volto/contributing/linting`.
    -   [Be tested](https://5.docs.plone.org/develop/testing/index.html).
        For Volto, follow {doc}`/volto/contributing/testing`.


### Create a new PLIP branch

Create a buildout configuration file for your PLIP in the `plips` folder of {file}`buildout.coredev`.

Give it a descriptive name, starting with the PLIP number, for example, {file}`plip-1234-widget-frobbing.cfg`.

The PLIP number is your PLIP's issue number.

This file will define the branches you're working with in your PLIP, along with other buildout configuration.

It should look something like the following, such as in a file {file}`plips/plip-1234-widget-frobbing.cfg`.

```ini
[buildout]
extends = plipbase.cfg
auto-checkout +=
    plone.somepackage
    plone.app.someotherpackage

[sources]
plone.somepackage = git https://github.com/plone/plone.somepackage.git branch=plip-1234-widget-frobbing
plone.app.someotherpackage = git https://github.com/plone/plone.app.somepackage.git branch=plip-1234-widget-frobbing

[instance]
eggs +=
    plone.somepackage
    plone.app.someotherpackage
zcml +=
    plone.somepackage
    plone.app.someotherpackage
```

Use the same naming convention when you branch existing packages.
You should always branch packages when working on PLIPs.


### Working on a PLIP

To work on a PLIP, you bootstrap buildout, and then invoke buildout with your PLIP configuration:

```shell
virtualenv .
./bin/pip install -r requirements.txt
./bin/buildout -c plips/plip-1234-widget-frobbing.cfg
```

If you are using a {file}`local.cfg` to extend your PLIP file with some changes that you do not want to commit accidentally, be aware that you need to override some settings from {file}`plipbase.cfg` to avoid some files being created in the {file}`plips` directory or in the directory above the buildout directory.
This is done as shown below.

```ini
[buildout]
extends = plips/plip-1234-widget-frobbing.cfg
develop-eggs-directory = ./develop-eggs
bin-directory = ./bin
parts-directory = ./parts
sources-dir = ./src
installed = .installed.cfg

[instance]
var = ./var
```


### Finishing up

Before marking your PLIP as ready for review, please add a file to give a set of instructions to the PLIP reviewer.
This file should be called {file}`plip_<number>_notes.txt`.
This should include, but is not limited to:

- URLs pointing to all documentation created and updated
- Any concerns and issues still remaining
- Any weird buildout things

Once you have finished, update your PLIP issue to indicate that it is ready for review.
The Framework Team will assign 2-3 people to review your PLIP.
They will follow the guidelines listed at {doc}`plip-review`.

After the PLIP has been accepted by the Framework Team and the release managers, you will be asked to merge your work into the main development line.
Merging the PLIP in is not the hardest part, but you must think about it when you develop.

You'll have to interact with a large number of people to get it all set up.

The merge may have unintended interactions with other PLIPs coming in.
During the merge phase you must be prepared to help out with all the features and bugs that arise.

If all went as planned, the next Plone release will carry on with your PLIP in it.
You'll be expected to help out with that feature after it's been released (within reason).


## Frequently asked questions about PLIPs

This section provides detailed answers to common questions about PLIPs.


### PLIP or bug fix?

In general, anything that changes the API of Plone in the backend or the user interface (UI) on the front end should be filed as a PLIP.
When in doubt, submit it as a PLIP.
The Framework Team will reclassify it if your proposal falls below the threshold.
If the change you are proposing is not in the scope of a PLIP, a GitHub pull request or issue is the right format.
The key point here is that each change must be documented, allowing it to be tracked and understood.


### Who can submit PLIPs?

Anyone who has signed a Plone Contributor Agreement can work on a PLIP.

```{todo}
The FWT no longer participates in PLIPs.
Recommend deletion of next two paragraphs.
```
The Framework Team is happy to help you at any point in the process.

When the PLIP is accepted, a Framework Team member will "champion" your PLIP and follow up to its completion.


### What is a PLIP champion?

```{todo}
This section is no longer in practice.
Recommend deletion.
```

When you submit your PLIP and it is approved, a Framework Team member will take on the role of champion for that PLIP.

They are there to help you through completion, answer questions, and provide guidance.

A champion fulfills the following tasks:

-   Answer any questions the PLIP implementor has, technical or otherwise.
-   Encourage the PLIP author by constantly giving feedback and encouragement.
-   Keep the implementer aware of timelines, and push to get things done on time.
-   Assist with finding additional help when needed to complete the implementation in a timely matter.

Keep in mind that champions are volunteers as well, and have other tasks in life.
That means you will have to play an active role in asking for help or guidance.


### Can I get involved in other ways?

If you want to experience the process and how it works, help us review PLIPs as the implementations finish up.

Check the status of PLIPs at https://github.com/search?q=path%3A%2Fplone+label%3A%2203+type%3A+feature+%28plip%29%22++&type=issues&ref=advsearch&state=open.

Then, follow the instructions for {doc}`reviewing a PLIP <plip-review>`.


### When can I submit a PLIP?

Today, tomorrow, any time!

After the PLIP is accepted, the Framework Team will try to judge complexity and time to completion, and assign it to a milestone.


### When is the PLIP due?

**Summary: As soon as you get it done.**

Ideally, a PLIP should be completed for the release to which it's assigned.
Sometimes life gets in the way, and a PLIP may have to be re-assigned to the following release.

In general, PLIPs shouldn't take more than a year, otherwise they should be closed. A new PLIP can follow up if there is more capacity to see it through.


### What happens if your PLIP is not accepted?

If a PLIP isn't accepted in core, it doesn't mean it's a bad idea.
It is often the case that there are competing implementations, and the community wants to see it vetted as an add-on before "blessing" a particular implementation.


