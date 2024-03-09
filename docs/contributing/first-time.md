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

It is assumed that the first-time contributor has already {doc}`installed Plone <../install/index>` on their development machine, has a GitHub account, and has basic knowledge of using git and GitHub.


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


(plone-contributors-team-label)=

### Plone Contributors Team

The Plone GitHub organization uses GitHub Teams to grant groups of GitHub users appropriate access to its repositories.
New users, including GSoC applicants, are assigned to the [Contributors](https://github.com/orgs/plone/teams/contributors) Team within a few days after they have signed and returned the {ref}`Plone Contributor Agreement <contributing-sign-and-return-the-plone-contributor-agreement-label>`.
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
    Working on documentation or on issues labeled with either `33 needs: docs` or `41 lvl: easy` are the two best ways for first-time contributors to contribute.
    This is because first-timers have a fresh perspective that might be overlooked by old-timers.
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

1.  Start by [forking the project's repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo) to your account through the GitHub interface.
1.  [Clone your forked repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#cloning-your-forked-repository).
1.  [Configure git to sync your fork with the upstream repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo#configuring-git-to-sync-your-fork-with-the-upstream-repository).


(write-code-label)=

### Write code

Once you have your environment set up, then you can follow standard best practices for working with git.

Always start by checking out the default branch, usually `main` or `master`, then update the default branch.

```shell
git checkout main
git pull
```

Then create a new branch from the default branch, and check it out to work on it.
We recommend using a branch name that includes the issue number and is descriptive of what it resolves.

```shell
git checkout -b branch_name
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
This will save you and reviewers a lot of time and frustration.

A bug fix or new feature should have a test that ensures that it works as intended.


(create-a-pull-request-from-your-fork-label)=

### Create a pull request from your fork

Once you have completed, tested, and linted your code, and created a {ref}`contributing-change-log-label`, then you can follow the standard practice for making a pull request.

1.  Commit and push your changes to your fork.

    ```shell
    git add <files>
    git commit -m "My commit message"
    git push
    ```

1.  Visit your fork of the Plone repository on GitHub, and [create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) against the development branch.
    -   Make your title and description descriptive.
        Don't be lazy with "Fixes bug" or other useless drivel.
    -   To automatically close the original issue when your pull request is merged, include "Closes #issue_number" in your description.
        This also creates a hyperlink to the original issue for easy reference.
1.  [Request a review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review) from other team members.
1.  Members who subscribe to the repository will receive a notification and review your request.

```{todo}
Provide instructions when the contributor needs to update their pull request with changes from the default branch.
Members of Contributors do not have the button "Update branch" to easily do this, and must use git foo to manage the situation.
```

Welcome to the Plone community, and thank you for contributing!
