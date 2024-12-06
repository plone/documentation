---
myst:
  html_meta:
    "description": "First-time contributors to Plone"
    "property=og:description": "First-time contributors to Plone"
    "property=og:title": "First-time contributors to Plone"
    "keywords": "Plone, first-time, GitHub, contributing, contributors"
---

(first-time-contributors-label)=

# First-time contributors

This chapter provides guidance to first-time contributors to Plone and all its projects and repositories under the Plone GitHub organization.


(for-students-and-learners)=

## For students and learners

```{important}
**We do not offer training, guidance, or mentoring to students or learners on GitHub.**
Don't ask for it.
The Plone organization may delete comments, lock conversations, or block GitHub users who ignore this.
```

If you are a student or learner of Plone, you probably are not a contributor.
See the next section, {ref}`expectations-of-first-time-contributors`, to determine whether you are in fact a contributor.

To learn how to use git and GitHub and make your first contribution to open source software, visit the amazing resource [`first-contributions`](https://github.com/firstcontributions/first-contributions).

For free support, training, guidance, or mentoring, you should work through some trainings, use the [Plone Community Forum](https://community.plone.org/), participate in an [event](https://plone.org/news-and-events/events), and **not use GitHub**.


(expectations-of-first-time-contributors)=

## Expectations of first-time contributors

As a first-time contributor to Plone on GitHub, we expect that you have:
 
-   {doc}`installed Plone <../install/index>` on your development machine
-   worked on a Plone project, even if it is just for fun
-   read and followed the guidance on the pages under {doc}`/contributing/index` both for Plone in general and for the specific project to which you want to contribute, as well as all the guidance on this page
-   worked through some trainings, such as the recommended:
    -   {doc}`training:mastering-plone/index`
    -   {doc}`training:volto-customization/index`
    -   {doc}`training:customizing-volto-light-theme/index`
    -   {doc}`training:voltohandson/index`
    -   {doc}`training:voltoaddons/index`
    -   {doc}`training:plone-deployment/index`
-   a sincere interest to contribute to Plone and become an ongoing contributing member of our organization
-   a GitHub account
-   basic knowledge of using git and GitHub

```{warning}
As a first-time contributor on GitHub, your expectations should align with ours, else you might feel disappointment or frustration.

Plone has a very large and complex code base.
It takes a significant amount of time to learn how to develop Plone.

If you want to quickly pad your résumé, satisfy a "contribute to open source" school assignment, or get recognition for participating in events such as Hacktoberfest, then Plone may not be the open source software project for you.
Such motivation behind these contributions usually results in poor quality breaking code, and drains limited volunteer time to triage.
```


(first-time-requirements-label)=

## Requirements

All first-time contributors to Plone must follow the contributing requirements described in {doc}`index`.

For [Plone Google Summer of Code (GSoC)](https://plone.org/community/gsoc) applicants, you must also follow both our and its program guidelines.


(contributing-make-contributions-through-github-label)=

## Make contributions through GitHub

Contributions to Plone are managed through git repositories on GitHub.
This section first discusses what not to do, then how to work effectively with a project on GitHub.


(things-not-to-do-label)=

### Things not to do

The following is a list of the most frequent mistakes made by first-time contributors.
Learn from their mistakes, and don't commit them yourself.

(mistake-1-label)=

1.  **Never ask to be assigned to an issue.**
    Instead you may post a comment to claim it, if no one else has claimed it (see {ref}`Avoid duplicate effort <mistake-2-label>`).
    For example, "I am working on this issue in pull request #123."
    You do not need to ask to be assigned to, or to work on, an open issue.
    As in any open source software project, you can start work on open issues at your convenience.
    Privileged team members may ignore or delete comments asking to be assigned to an issue.

    (mistake-2-label)=

2.  **Avoid duplicate effort.**
    Don't work on issues that have already been claimed or worked on, unless such effort has been abandoned by the author.
    GitHub's interface provides links to related issues and pull requests, and who is assigned to an issue.
    Pull requests will be reviewed in the order received.
    Duplicate pull requests may be ignored and closed without comment by the privileged GitHub teams.

3.  **Don't create and close multiple pull requests for the same issue.**
    GitHub should not be used as a place to test your contribution.
    It makes it impossible for reviewers to provide feedback to your contribution in one place.
    It also sends notifications to hundreds of developers, informing them that you have not read this guide, and annoying many of them.
    You should instead learn how to {ref}`work-with-github-issues-label` and {ref}`run tests and code quality checks locally <test-and-code-quality-label>`.

4.  **Don't ask if an issue is open.**
    Instead you can determine whether an issue is open by doing your own research using the following tips.

    -   Start Plone or its specific package, follow the steps to attempt to reproduce the issue, and see if it still exists.
    -   Check the issue's status indicator for a green label of {guilabel}`Open`.
    -   Look for linked open pull requests in the issue's history.
    -   Search open pull requests for the issue.
        Sometimes contributors fail to link their pull request to an open issue.
    -   Review unreleased change log entries in the package's {guilabel}`news` directory.
        Each pull request must have a change log entry, and these entries end up here when pull requests are merged and closed.
    -   Search release notes to see whether the issue has been resolved.
        On rare occasions, contributors forget to close the original issue.


(plone-contributors-team-label)=

### Plone Contributors Team

The Plone GitHub organization uses GitHub Teams to grant groups of GitHub users appropriate access to its repositories.
New users, including GSoC applicants, are assigned to the [Contributors](https://github.com/orgs/plone/teams/contributors) Team within a few business days after they have signed and returned the {ref}`Plone Contributor Agreement <contributing-sign-and-return-the-plone-contributor-agreement-label>`.
New contributors should wait for confirmation that they have been added to this team before creating a pull request to a Plone project.


(first-time-mr-roboto-on-github-label)=

### `mr-roboto` on GitHub

[`mr-roboto`](https://github.com/plone/mr.roboto) enforces the requirement of a signed Plone Contributor Agreement from a new contributor, and being assigned to a Plone team on GitHub.

New contributors to Plone who submit a pull request and do not wait for confirmation that they have been added to the Contributors team will be subjected to persistent nagging from `mr-roboto`.
`mr-roboto` will not respond to you if you `@` it.
Core developers may ignore your contribution because you did not follow these instructions.
Please don't be "that person".


(work-with-github-issues-label)=

### Work with GitHub issues

1.  **Find issues that you want to work on.**
    You can filter GitHub issues by labels.
    Working on documentation or on issues labeled with either [`33 needs: docs`](https://github.com/search?q=user%3Aplone+label%3A%2233+needs%3A+docs%22&type=issues&ref=advsearch) or [`41 lvl: easy`](https://github.com/search?q=user%3Aplone+label%3A%2241+lvl%3A+easy%22&type=Issues&ref=advsearch) are the two best ways for first-time contributors to contribute.
    This is because first-timers have a fresh perspective that might be overlooked by old-timers.
    
    Issues labeled `42 lvl: moderate`, `43 lvl: complex`, or `03 type: feature (plip)` are not suitable for first-timers because of their complexity.
    Issues with these labels may take weeks to complete.
1.  **Discuss whether you should perform any work.**
    First see {ref}`Avoid duplicate effort <mistake-2-label>`.
    Next, any discussion method listed below is acceptable, and they are listed in the order of most likely to get a response.
    -   Search for open issues in the issue trackers of Plone projects on GitHub, and comment on them.
    -   If an issue does not already exist for what you want to work on, then create a new issue in its issue tracker.
        Use a descriptive title and description, include steps to reproduce the issue, and screenshots or videos that demonstrate the issue.
    -   Discuss during sprints, conferences, trainings, and other Plone events.
    -   Discuss on the [Plone Community Forum](https://community.plone.org/).
    -   Discuss in the [Plone chat on Discord](https://discord.com/invite/zFY3EBbjaj).
1.  **Clarify the scope of work that needs to be done.**
    Sometimes the issue description is blank or lacks clarity, the requirements have changed since it was created, or work has been completed in a pull request but the issue was not closed.
    Ask for clarification, whether it is still relevant, or whether it should be closed.

After you have satisfied the above steps and have clear direction on how to proceed, then you can begin work on the issue.


(set-up-your-environment-label)=

### Set up your environment

As a member of the Plone Contributors Team, you do not have write access to push commits to GitHub repositories under the Plone organization.
You can push commits to your fork.
Thus a typical workflow will be circular in nature.
You will pull code from the upstream Plone repository, push your work from your local clone to your remote fork, then make a pull request from your fork to the upstream Plone repository.

````{card}
```{image} /_static/contributing/first-time-plone-git-workflow.svg
:alt: Plone git workflow
:target: /_static/contributing/first-time-plone-git-workflow.svg
```
+++
_Plone git workflow_
````

1.  Start by [forking the project's repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) to your account through the GitHub interface.
1.  [Clone your forked repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#cloning-your-forked-repository).
1.  [Configure git to sync your fork with the upstream repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo#configuring-git-to-sync-your-fork-with-the-upstream-repository).


(write-code-label)=

### Write code

Once you have your environment set up, then you can follow standard best practices for working with git.

In the following command examples, we will use `main` as the default branch, although `master` may still be in use for some repositories.

Always start by checking out the default branch then update the default branch.

```shell
git checkout main
git pull
```

Then create a new branch from the default branch, tracking the upstream Plone repository, and check it out to work on it.
We recommend using a branch name that includes the issue number and is descriptive of what it resolves.

```shell
git switch -c my-branch-name -t upstream/main
```

Now you can edit your code without affecting the default branch.

```{note}
The Plone organization is aware of the racially insensitive terms that exist in our projects.
We are working to correct this mistake.
We ask for your patience as we work through complex automated workflows that need to be updated.
```


(test-and-code-quality-label)=

### Test and code quality

Follow the project's testing and code quality policies.
Most projects have a test suite and code quality checkers and formatters.
We strongly recommend that you run the project's test suite and code quality checks locally before proceeding.
Do not depend upon our continuous integration and GitHub Workflows to run these checks for you.
Every commit you push sends an email notification to repository subscribers.
This will save you, members, and reviewers a lot of time and frustration.

A bug fix or new feature should have a test that ensures that it works as intended.


(create-a-pull-request-from-your-fork-label)=

### Create a pull request from your fork

Once you have completed, tested, and linted your code, and created a {ref}`contributing-change-log-label`, then you can follow the standard practice for making a pull request.

1.  Commit and push your changes to your fork.

    ```shell
    git add <files>
    git commit -m "My commit message"
    git push -u origin my-branch-name
    ```

1.  Visit your fork of the Plone repository on GitHub, and [**create a pull request**](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) against the development branch.
    -   Make both your title and description descriptive.
        Reviewers look at many pull requests, and need to quickly understand the context.
        A lazily written phrase such as "Fixes bug" is meaningless.
    -   Include "Fixes #ISSUE-NUMBER" in the description.
        This enables automatic closing of the related issue when the pull request is merged.
        This also creates a hyperlink to the original issue for easy reference.
        
        ```{seealso}
        [Linking a pull request to an issue using a keyword](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword)
        ```

1.  **Request a review.**
    Identify who you should ask by either checking the history of the files you edit, or viewing the project's list of contributors for an active member.
    If you have write access to the repository, [request a review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review) from other team members.
    If you do not have write access, instead add a comment and mention a few active contributors of the project, tagging them with `@username`.
    You can find them by either checking the files' history via `git blame` or visiting the project's {guilabel}`Contributors` page on GitHub.
1.  Members who subscribe to the repository will receive a notification and review your request.
    They will usually provide feedback within a week.


(update-your-pull-request-from-your-fork-label)=

### Update your pull request from your fork

Often another pull request will get merged before yours, and your pull request will fall behind the main branch.
To keep your pull request current, you can issue the following git commands, assuming you have already checked out the branch for the pull request that you want to update.
These commands will only work if you have {ref}`set-up-your-environment-label` as mentioned above.

```shell
# Assume `main` is the main branch.
git fetch upstream
git merge upstream/main  # You might need to resolve conflicts here.
git push
```

Welcome to the Plone community, and thank you for contributing!
