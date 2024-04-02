---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

```{todo}
I seriously question the value of this entire guide.
I think it should be purged.
Plone should not be in the business of teaching how to use git or GitHub.
```

# Working with Git and GitHub

## The Plone Git workflow and branching model

Our repository on GitHub has the following layout:

-   **feature branches**:
    All development for new features must be done in dedicated branches, normally one branch per feature.
-   **main** or **master** **branch**:
    when features get completed they are merged into the master branch; bugfixes are commited directly on the master branch,
-   **tags**:
    whenever we create a new release, we tag the repository so we can later retrace our steps, or rerelease versions.


## Git basics

Some introductory definitions and concepts, if you are already familiar enough with Git, head to next section: {ref}`general-guidelines-label`.


### Mental working model

With Git (as well as all modern [DVCS](http://en.wikipedia.org/wiki/Distributed_revision_control)), distributing changes to others is a two steps process (contrary to traditional VCS like `svn`).

This way what on svn is a single `svn ci` in Git is two commands: `git commit` and `git push`.

This may seem to be a drawback, but instead it's a feature.

**You are working locally until you decide to push your changes.**

Not a single commit anymore, but a series of them, meaning that all those fears, concerns, doubts are taken away!

You can freely fix/change/remove/rework/update/... your commits afterwards.

Push your changes whenever you are sure they are what you, and others, expect them to be.


### Concepts

In Git there are:

commits

: A patch made out of changes (additions, removals) on files tracked by Git.

branches

: Series of commits that have a name.

tags

: A name attached to a single commit.

`HEAD`

: A pointer that always tells you where you are (extremely useful when doing some operations).

The index

: A temporal staging storage with changes on files that are pending to be added to a commit.
  If your Git output is colored, green filenames are those in the index.

Working tree

: Your current modified files.
  This is the only place where you can loose your changes.
  If your Git output is colored, red filenames are those in the working tree.

Stash

: Temporal storage for changes, again, extremely useful in some scenarios, see further below for examples.

### Branches

Another great feature of DVCS is cheap branching, i.e. branching in Git is effortless and really useful.
As it's no longer too much effort to branch, there is no need to always work on the master branch.

A developer can branch easily for each fix/feature.

Branches allow you to tinker with your changes while keeping the master branch clean.

Not only that, it also allows you to keep modifying your changes until you and your peers are fine with them.

Further documentation:
[Introduction to branching](http://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell).

### Commands

Some of the most useful/common commands (note that most of them have switches that enhance/*completely twist* their functionality):

Just append `--help` on all of them to get their full definitions and options,
i.e. `git add --help`.

clone

: Download a repository from a given remote URL.

add

: Add the given files to the index.

  ```{note}
  **pro tip**: once a file is add via `git add` your changes will never be lost!
  As long as you don't remove the `.git` folder, even if you remove the file you just added, the changes you made before doing `git add` are still there ready to be recovered at any time!
  ```

status

: Get an overview of the repository status.

  If there are files on the index, or files not tracked by Git, or the status of your local branch with regards to the remote, etc.

diff

: See the current changes made to the files already tracked by Git.

  ```note}
  Fear not, if you used `git add SOME_FILE` and then `git diff` doesn't output anything you haven't lost your changes!

  Just try `git diff --cached`.
  Now you know how to see the working tree changes (`git diff`) and index changes (`git diff --cached`).
  ```

commit

: Create/record changes to the repository (locally only, nothing is sent over the wire).

push

: Send your changes,
  either commits or a complete new branch,
  to the configured remote repository.

show

: Display the given commit(s) details.

log

: Shows the repository history.
  Sorted by date (last commit at the top),
  and like all other commands,
  extremely versatile with all its switches.

  See further below for an example of a powerful combination of switches.

branch

: Create a branch.

fetch

: Download changes from the remote repository.

  **Without** changing the current `HEAD` (see rebase and pull commands).

pull

: Fetch and integrate changes from remote repository.

  Internally that means to do a `git fetch` plus either `git merge` or `git rebase`.

  :::{note}
  Used careless most probably adds extra superfluous commits.
  See further down.
  :::

merge

: Join two,
  or more,
  branches together.

rebase

: Forward-port your current local commits (or branch) to be based on top of another commit.

  An image is worth 1000 words: <http://git-scm.com/docs/git-rebase>

checkout

: Change to the given branch or get the given file to its latest committed version.

  :::{note}
  If Git is criticized for being complex,
  this command is one of the main sources of complains.

  You can compare it with `svn switch` if you happen to know it.

  Fear not though,
  two main use cases are:
  change branches and reset a file to its last committed version.
  Still,
  the syntax for both cases is really simple.
  :::

cherry-pick

: Apply a commit(s) to the current working branch.

stash

: Use a temporal storage to save/restore current changes still not meant to be used on a commit.

  :::{note}
  Seems a bit not so useful on a first look,
  but it is indeed.

  Think about this scenario:
  you are working on your branch coding away.
  All of the sudden you notice a small fix that should be done directly on master.
  Thanks to `git stash` you can save your changes quickly and safely,
  move to master branch,
  do the quick fix,
  commit and push it,
  move back to your branch and `git stash pop` to recover your changes and continue hacking away.
  :::

reflog

: When things go bad you will **love** this command.

  It effectively shows you a histogram of what happened on the repository,
  allowing you to rollback you repository to a previous stage.

  Extremely useful once a bad interactive rebase has happened.

(general-guidelines-label)=

## General guidelines

### Pulling code

Let's compare this two histories:

```
*   3333333 (HEAD, master) Merge branch 'feature-branch' into master
|\
| * 2222222 (feature-branch) Last changes on feature-branch
| *   1111111 Merge branch 'master' into feature-branch
| |\
| * | 0000000 More changes on feature branch
| * |   fffffff Merge branch 'master' into feature-branch
| |\ \
* | | | eeeeeee master keeps rocking
| |_|/
|/| |
* | | ddddddd master goes and goes
| |/
|/|
* | ccccccc master evolves
| * bbbbbbb First commit on feature-branch
|/
* aaaaaaa commit on master  # this is where feature-branch was created
```

With:

```
* 3333333 (HEAD, master) Merge branch 'feature-branch' into master
|\
| * 2222221 (feature-branch) Last changes on feature-branch
| * 0000001 More changes on feature branch
| * bbbbbb1 First commit on feature-branch
|/
* eeeeeee master keeps rocking
* ddddddd master goes and goes
* ccccccc master evolves
* aaaaaaa commit on master
```

What do we see above? Actually and contrary to what it seems,
exactly the same **result**
(as how the files and its content look like on commit `333333`).

The second version is far more easy to understand what happened and removes two superfluous commits
(the two partial merges with master (`fffffff` and `1111111`).

This happens if you have not properly configured `git pull`.
By default it does a `merge` meaning that an extra commit is always added,
tangling the history and making this more complex when looking back for what happened there.

#### How to solve it?

*ALWAYS* do a {command}`git pull --rebase` when fetching new code,
configure Git to do always so with:

```
git config branch.autosetuprebase always # add the --global switch to make it default everywhere
```

This way you do not introduce new extra commits and the Git history is kept as simple as possible.

This is especially important when trying to understand why some changes were made,
or who did actually change that line,
etc.

A couple of further explanations:
<http://stevenharman.net/git-pull-with-automatic-rebase>

<http://www.slideshare.net/michalczyzcs3b/git-merge-vs-rebase-miksturait-4>

Search for `git merge vs rebase`, you will find plenty of literature.

### Reviewing your changes

After hacking for some minutes/hours/days you are finished and about to commit your changes,
great!

*BUT*,
please,
do so with {command}`git add --patch`.

The `--patch` (also `-p`) switch allows you to select which hunks you want to add on a commit.

This is not only great to split changes into different commits,
but is also the time when you actually **review** your code before anyone else sees it.

This is the time when you spot typos, pep8 errors, misaligned code, lack of docstrings in methods,
that a permission is not defined on Generic Setup, that an upgrade should be needed...

Remember that the first code review is the one you do on your own.
Some inspiration/better phrasing:
<http://ada.mbecker.cc/2012/11/22/be-your-own-code-review/>

And please, do remember the gold metric about reviewing code:
<http://www.osnews.com/story/19266/WTFs_m>

#### One commit does one thing

Repeat with me: *One commit does one thing*. Period.

When someone else needs to review your code, most probably she will give up or just skim over your code
if there are too many (unrelated) changes.

Reviewing commits with +20 files doing all sorts of changes on them (maybe even unrelated)
is no fun and adds complexity and [cognitive load](http://en.wikipedia.org/wiki/Cognitive_load).

Something that should mostly be a verification of a checklist like:

- the browser view is registered on ZCML?

- is there an interface for that form?

- the pt and py are there?

- ...

Turns instead into a list of questions:

- why is this interface renamed here if it has nothing to do with this adapter?
- all this removal of deprecated code while adding new features just mixes the diff,
  am I missing something?
- *others*

If you can not express what has been changed within 50 characters (suggested length of a commit message subject),
or you say it like "it does XXX and YYY", you most probably need to split that commit into, at least,
two or more commits.

That doesn't mean that a +20 files or +100 lines of code changes are bad per se, you may be doing
a simple refactoring across lots of files, that's fine and good actually.

As long as a commit is just and only about a specific purpose, and not a mixed selection of the following:

- refactoring code
- moving things around
- fixing some bugs while at it
- adding some docs
- a new cool feature
- fixing typos on documentation
- pep8 fixes

It is absolutely fine to refactor.

And this is actually to help both your present self and your +5 years from now that will have to refactor that code of yours,
and maybe is struggling to understand what was going on there.

Following this advice will:

- keep things simple where there's no gain in adding complexity
- make your changes easy to be reviewed
- make later on lookups on those changes easy to follow

### Making commits

For commit messages see: {ref}`git_commit_message_style_guide`.

#### Adding references to issues

Always add the full URL to the issue/pull request you are fixing/referring to.

Maybe within the Git repository it makes sense, but as soon as you are outside of it, it will not.

Take into account mr.roboto automatic commits to buildout.coredev for example, if your commit message goes like *Fix for #33*,
which issue/pull request is that fixing?

The one in buildout.coredev itself? On another issue tracker? Somewhere else?

It would be far better if the commit goes instead like:

```
Brief description

Further explanation.

Fixes: https://github.com/plone/plone.app.discussion/issue/999
```

#### Bad examples

Some bad examples of commit messages:
<https://github.com/plone/plone.app.content/commit/0f3a6c65b2018e0ecc65d0ad1581e345f17e531b>

Commit messages goes like *"Make note about how this interface is now for BBB only"*.

Question: if it's BBB only, where is the new place to look for that interface now?

The problem is that, in this case Martin, wrote that in 2009, so most probably once a refactor of that package
is done later on 2015, Martin is no longer around, and if he was, most probably he would not remember something from +6 years ago.

Ask yourself a question:

If someone comes to you asking details about a random commit done by you +5 years ago, what will you reply?

Try that, get one project that you worked 5 years ago, get a random commit and:

See if, just by reading the commit message, you are given enough information of what changes have been made,
when comparing the commit message and the actual code.
Does the commit message match the code changed?

### Before pushing commits

Code is reviewed, spread into nice isolated commits, descriptive enough commit messages are written, *what's left?*

A final overview of what you are about to push.

To do so, you can get an idea with the following Git alias (to be added on your `~/.gitconfig`):

```
[alias]
    fulllog = log --graph --decorate --pretty=oneline --abbrev-commit --all
```

Now run {command}`git fulllog` on your Git repository, you will see a nice graph showing you the current situation.

Maybe it makes you realize that commits need to be reordered, commit messages could get some improvements,
that you forgot to add a reference to an issue, ...

## Pull requests

Some specific tips and best practices for pull requests.

### Always rebase

Always rebase on top of the branch you want your changes to be merged before sending a pull request,
and as your pull request is still pending to be merged and the master branch evolves, keep rebasing it.

To do so:

```
git checkout <your branch>
git rebase master # or the branch you are targeting to integrate your changes to
# done!
# or if there are conflicts,
# fix them and follow instructions from git itself
```

The principle is, if you do merges with master, you are actually spreading your pull request into more commits,
and at the end making it more difficult to track what was changed.

On top of that, the commit history is more complex to follow.

See the history example above: {ref}`general-guidelines-label`.

Unfortunately the flat view from GitHub prevents us from seeing that,
which is a shame.

### One line one commit

On a series of commits make sure the same code line is not changed twice,
the worst thing you can do to the one reviewing your changes,
is to make him/her spend time reviewing some code changes that one the next commit are changed again to do something else.

It will not only make your commits smaller, but it will also make it easy to do atomic commits.

### No cleanup commits please

*On the context of a pull request*

Ask yourself: What relation does a cleanup commit, say pep8 fixes or other code analysis fixes,
have with your pull request?

Couldn't that pep8 fixes commit or small refactoring go straight into master branch?

Or even if you send a pull request for it, chances are that it will be merged right away.
As long as it is a cleanup commit, there's not much to argue with it.

The same goes with commits that improve or actually fix previous commits (within the same pull request).
A series of commits like this:

```
* 11ba28c Last fix, finally
* 11ba28c Fix tests, again
* 11ba28c Fix tests
* 11ba28c Do something fancy
* 11ba28c Failing test, we are doing TDD right?
```

Only tells you that the author did not take care at all about the one who will review it,
and specially about the person that in +5 years will try to understand that test.
Specially because now the test is not only spread between 4 commits, but most probably during those 5 years
it has already been refactored, maybe a {command}`git blame` will report that within that test method,
there are +5 related current commits to check, not nice right?

#### Squashing commits

To fix the previous example, run the following command:

```
git rebase ---interactive <base> # which mostly is usually master
```

This allows you to rewrite the story of your branch.
See a more [elaborate description with examples](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase-i/).

:::{note}
Be careful on not to run that on master itself!
Please take your time to really understand it.

It's a really powerful tool,
and as [Stan Lee says](http://en.wikiquote.org/wiki/Stan_Lee),
it comes with great responsibility.
:::

To actually make it easier you can do commits like this:

```
git commit --fixup HASH
```

Where `HASH` is the commit hash you want the changes you are about to commit be merged with.

This way, when running {command}`git rebase --interactive`, Git will already reorder the commits as you already want.

### No side changes

That's an extension to the previous point.

Keeping pull requests simple and to the point, without changes not related to the pull request itself,
will make your changes easier to understand and easier to follow.

Again this applies:
<http://www.osnews.com/story/19266/WTFs_m>

### The review-change-push-review cycle

After you have made a pull request,
you should ask for a review via the GitHub interface.

After the review you will frequently have to do some changes of your PR,
perhaps add a missing changelog entry, and so on.

When the changes are done, rebase your branch again
and squash any fixup-commits, all as described above.

Finally you should force push your feature branch to GitHub.
Only force push on your own feature branches!
Never on branches shared with other people.

After the update of your branch,
the GitHub PR interface will pick up the changes,
ready for returning to the reviewer,
and hopefully get a final go for the merge.

## Recipes

Assorted list of tips and tricks.

### Change branches with uncommitted changes

**Situation:** you are working on a pull request and while working on it founds that some cleanups are needed,
how to proceed forward?

**Solution:** `git stash` or `git commit --amend -m"TMP"`.

The basic idea here is: store your current changes safely (either on a Git stash commit or directly on a commit on the branch,
whichever you prefer), move to the canonical branch (`master` usually), do the fixes/cleanups/refactorings there,
commit those changes, rebase your branch on top of the changes you made, hack away.

Command line version:

```
git stash # or git commit --amend -m"TMP"
git checkout master # or whatever happens to be the canonical branch name (i.e. 5.0 on buildout.coredev)
# do the cleanups && push them
git checkout your-branch # get back to your branch
git rebase master # again the canonical branch where you made the changes
git stash pop # or git reset HEAD^ if you did a git commit --amend -m"TMP"
# if needed, fix the conflicts, with patience and practise that's a piece of cake once you are used to
```

### Git visual applications

Not everyone is a fan of the command line, for them there is a list of GUI clients on the official Git website:

<http://git-scm.com/downloads/guis>

### Enhanced Git prompt

Do one (or more) of the following:

- <http://clalance.blogspot.com/2011/10/git-bash-prompts-and-tab-completion.html>
- <http://en.newinstance.it/2010/05/23/git-autocompletion-and-enhanced-bash-prompt/>
- <http://gitready.com/advanced/2009/02/05/bash-auto-completion.html>

### Git dotfiles

Plone developers have dotfiles similar to these:
<https://github.com/plone/plone.dotfiles>.

## Learn more

What's here is just the tip of the iceberg, there's plenty of Git knowledge on the web.

A few good further resources are listed here (contributions welcome):

- official online Git book: [Pro Git](http://git-scm.com/book/en/v2)
- PyCon 2015 talk: [Advanced Git by David Baumgold](https://www.youtube.com/watch?v=4EOZvow1mk4)
