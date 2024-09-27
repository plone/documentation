---
myst:
  html_meta:
    "description": "Working with continuous integration via Jenkins and GitHub workflows in Plone"
    "property=og:description": "Working with continuous integration via Jenkins and GitHub workflows in Plone"
    "property=og:title": "Continuous integration"
    "keywords": "Plone, continuous integration, Jenkins, GitHub workflows"
---

# Continuous integration

As a complex system built from hundreds of small packages, Plone can be easily and inadvertently broken from a change to any of its packages.
To help prevent breaking Plone, a mix of a {term}`continuous integration` (CI) systems of GitHub workflows and Jenkins thoroughly checks all changes.

Do not use continuous integration as a replacement for running tests and other checks locally before pushing commits to a Plone repository.
See {ref}`test-and-code-quality-label` for an explanation, and {ref}`contributing-specific-contribution-policies-for-projects-label` for a project's specific contributing guidelines.


## GitHub workflows

Most Plone repositories use {term}`GitHub workflows` to run tests, check code quality, and perform other CI tasks on pushed commits to an open pull request.

If a pull request is opened from a branch in the repository, then checks will automatically run.
Only members of certain Plone GitHub organization teams and users with write permission in the repository can do this.
Otherwise GitHub workflows do not run automatically, and require a member with write permission to run the checks.

GitHub workflows should pass before running Jenkins checks and before merging an open pull request.


## `mr-roboto`

[`mr-roboto`](https://github.com/plone/mr.roboto) enforces the requirement of a signed Plone Contributor Agreement from a new contributor, and being assigned to a Plone team on GitHub.
It also suggests to run Jenkins for many Plone packages.


## Jenkins

[Jenkins](https://jenkins.plone.org) is the authoritative source to see whether the complete test suite passes for any Plone version under development.
Jenkins can be run on a change to any of Plone's hundreds of repositories that it monitors.


### Run Jenkins

Running the entire test suite on Jenkins takes at least 30 minutes, and consumes precious server resources.
For this reason, Jenkins is configured not to run automatically on each push to an open pull request.
Instead you should wait until you have completed pushing commits to an open pull request, and have seen that all GitHub workflows have passed.

After all GitHub checks pass, and if Jenkins monitors the project, you can run Jenkins by adding a comment to the open pull request.

```text
@jenkins-plone-org please run jobs
```

This will trigger Jenkins to run all configured test suites using the changes in the pull request.

You can also manually run Jenkins jobs by visiting our [Jenkins server](https://jenkins.plone.org/), logging in with your GitHub account, finding the right job, and clicking the <img alt="Build now icon" src="/_static/contributing/core/icon-build-now.svg" class="inline"> {guilabel}`Build now` button.


#### `buildout.coredev` special case

`buildout.coredev` contains the configuration and tooling to orchestrate Plone.
Contrary to all the other repositories, whenever a push is made to this repository, it automatically triggers Jenkins to run its jobs.


### Results

Once a Jenkins job completes, it updates its status icon in the Jenkins UI, and reports the result of the job to the open pull request on GitHub.

In GitHub at the end of the pull request, a status indicator of either a green check mark {guilabel}`✅` or a red cross {guilabel}`❌` will be displayed for the job, followed by a {guilabel}`Details` link back to the Jenkins job build for that pull request.
The status indicator will also appear in the GitHub Octocat favicon in the web browser tab on the pull request, and on lists of pull requests.

You can use the results to decide whether to merge the pull request.


### Failure

If the Jenkins job reports a failure, you can investigate its cause.
Click the {guilabel}`Details` link to show the stacktrace on Jenkins.

In the side bar of the job build page in Jenkins, click the <img alt="Console Output terminal icon" src="/_static/contributing/core/icon-terminal.svg" class="inline"> {guilabel}` Console Output` link to show the full console output.
You can examine all the steps and debugging information that Jenkins generated while running the job.
This can be helpful whenever the errors were not in a single test, but rather a test set up or tear down or other problem.


### Retry

If there were errors on the Jenkins jobs, and you push additional commits to correct the errors, you can trigger the Jenkins jobs again by adding a comment to the open pull request in GitHub.

```text
@jenkins-plone-org please run jobs
```

You can also restart Jenkins jobs in the Jenkins UI.
After logging in to Jenkins, and finding the appropriate job, you can click the <img alt="Retry icon" src="/_static/contributing/core/icon-retry.svg" class="inline"> {guilabel}`Retry` link on the left toolbar to retry the failed job.
Jenkins will update GitHub statuses accordingly.
