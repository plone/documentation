---
myst:
  html_meta:
    "description": "Essential continuous integration practices"
    "property=og:description": "Essential continuous integration practices"
    "property=og:title": "Essential continuous integration practices"
    "keywords": "Plone, continuous integration, best practices"
---

# Continuous Integration

As a complex system build out of hundreds of small packages, Plone can be easily broken, inadvertently, with any change on any of its packages.

For that a mix of a {term}`CI` system at [jenkins.plone.org](https://jenkins.plone.org) and GitHub Actions ensure that any change is thoroughly checked.

## Jenkins

Jenkins is the primary source of truth to know if the complete test suite of any Plone versions in development is passing or not.

Jenkins is configured to react on changes done in any of the hundreds of repositories that all together make Plone.

Whenever a change on any of those repositories happen, Jenkins starts a slew of testing jobs that ultimately answer the question of if those changes pass Plone's test suite.

### Triggering jobs (automatically)

As running the Jenkins jobs is a bit expensive, in time, Jenkins does not run automatically on any new commit.

Rather, Jenkins waits for a special comment to be found in a pull request on a repository that is monitored by Jenkins.

```text
@jenkins-plone-org please run jobs
```

Pasting the text above on a pull request, will trigger Jenkins to run all configured test suites related to the current pull request, **with the changes of the pull request itself**.

#### buildout.coredev special case

`buildout.coredev` is the special repository where our configuration and tooling to orchestrate Plone lies in.

Contrary to all the other repositories, whenever a commit is made on this repository, it automatically triggers Jenkins jobs to be run.

### Triggering jobs (manually)

Jenkins jobs can also be triggered manually by going to our Jenkins server, login in with your GitHub account, finding the right job, and triggering the `Run` button.

### Results

Once a jenkins job is finished, it will update its status icon on Jenkins UI itself, but also report back to GitHub, the result of the job.

For pull requests, this means a green check mark or a red cross will be displayed at the end of the pull request, on pull requests listings, even on the favicon itself.

This gives the expected feedback to the pull request author, or any reviewer interested in knowing how a given pull request fared in Jenkins. Thus allowing pull request reviewers or authors to decide if the pull request can already be merged.

#### On failures

If the Jenkins jobs reports failures, the statuses of the pull request will provide a `Details` link back to Jenkins.

That link leads back to the Jenkins job build for that pull request.

In that page, there is the list of test failures (if any) already listed. Clicking on them show the stacktrace that should help diagnose why there was an error on a given test.

On the side bar of the job build page in Jenkins there is also `Console Output` link. This leads to the **full job output**, note that is large, where it can be seen all the steps and debugging information that Jenkins generated running the job.

This can be helpful whenever the errors where not on a single test, but rather a general testing set up/tear down problem.

### Retrying

If there were errors on the Jenkins jobs, and corrections have been made on the code, triggering the jenkins jobs again is a matter of giving the special comment on the GitHub pull request again:

```text
@jenkins-plone-org please run jobs
```

Jenkins jobs can also be restarted within Jenkins UI itself. On the Jenkins job itself, and provided you are logged in, you can find a `Retry` link on the left toolbar. Clicking it will trigger a new Jenkins job with the same configuration as the one you are on.

Jenkins will update GitHub statuses accordingly.
