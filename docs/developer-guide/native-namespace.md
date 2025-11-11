---
myst:
  html_meta:
    "description": "How to convert a Python distribution from a pkg_resources namespace to a native namespace"
    "property=og:description": "How to convert a Python distribution from a pkg_resources namespace to a native namespace"
    "property=og:title": "Native namespace"
    "keywords": "Plone 6, developer guide, native namespaces, pkg_resources, Python"
---

# Native namespace

This document explains the steps needed to convert a python distribution from `pkg_resources` namespace to native namespaces.

## Background

Python, since Python 3.3, added support for native namespaces, see [PEP 420](https://peps.python.org/pep-0420/).

Plone has been using `pkg_resources`-style namespaces, but they are deprecated in `setuptools`.

`setuptools` is planning to remove `pkg_resources`'s namespaces support by the end of 2025.

[PLIP 3928](https://github.com/plone/Products.CMFPlone/issues/3928) tracks the changes needed for Plone to adapt to the _new_ native namespaces.

## Steps

To convert a given (`$package`) python distribution to use native namespaces follow these steps.

### Create maintenance branch

```{note}
Only relevant for Plone core packages
```

```{tip}
This part is only needed when the `main` or `master` branch is used on multiple versions of the Plone core development buildout.
```

Clone the repository or ensure you are at latest changes:

```shell
git clone git@github.com:plone/$package
cd $package
# or update
git fetch -p
git checkout main # or master
git rebase
```

Find out what's the last release and create a branch for it:

```shell
# list all tags
git for-each-ref --sort=taggerdate --format '%(tag)' refs/tags
# get the last tag's major number
MAJOR=`git for-each-ref --sort=taggerdate --format '%(tag)' refs/tags | tail -n1 | cut -d"." -f1`
# create a branch for it
git checkout -b $MAJOR.x
# push the newly created branch
git push
```

### Update buildout.coredev

```{note}
Only relevant for Plone core packages
```

Update `buildout.coredev`'s branch 6.1 to use the newly created branch

```shell
# go to the repository or clone it
cd buildout.coredev
# ensure you are at latest changes
git fetch -p
git checkout 6.1
git rebase
# update the branch being used by the python distribution
sed -i "s/$package.git branch=master/$package.git branch=$MAJOR.x/" sources.cfg
# add the changes, commit and push
git add sources.cfg
git commit -m"chore: use branch $MAJOR.x for $package"
git push
```

Now check if you need to do the same on the 6.0 branch of `buildout.coredev`.

```{tip}
You can use this [handy table](https://jenkins.plone.org/roboto/branches) to know which branch is used of a given package on each Plone version
```

```{tip}
To lower the amount of builds in Jenkins, either do a few at a time or add a `[ci-skip]` on the commit message
```

### Numbers before

One risk of changing to the native namespaces is that some files, or tests, might be left behind.

To ensure all tests and files are kept after the switch, gather the numbers before the change:

Get the list of tests:

```shell
tox run -e test -- --list-tests | wc -l
```

```{note}
Adapt to whichever way you are using to run the tests.
The above is meant for repositories that follow `plone.meta` conventions.
The `--list-tests` comes from `zope.testrunner`, if you are using that but not `plone.meta` you can use that as well.
```

Create a distribution to get a listing of how many files are currently packaged:

```shell
rm -rf dist/
uvx --from build pyproject-build
```

A `dist` folder is created with two archives in it: a `.tar.gz` and a `.whl`.

To get the number of files on them run the following commands:

```shell
python -c "import glob; import tarfile; print(len(tarfile.open(glob.glob('dist/*.tar.gz')[0], 'r:gz').getnames()))"
python -c "import glob; from zipfile import ZipFile; print(len(ZipFile(glob.glob('dist/*.whl')[0]).namelist()))"
```

Keep these numbers around for later.

### Build backend

To ensure the package continues to build, ensure that `setuptools` is defined as its build backend.

For that inspect the `pyproject.toml`, it should have these lines:

```toml
[build-system]
requires = ["setuptools>=68.2,<80", "wheel"]
```

If they are not there, add them, commit and push the changes.

### Convert to native namespace

Use `plone.meta`'s `switch-to-pep420` script:

```shell
cd $package
uvx --from plone.meta switch-to-pep420 --no-tests .
```

```{tip}
This will also bump the version to a new major release.

If the `main` or `master` branch is already an alpha version that is only used in Plone 6.2, you can specify that you don't want this version bump by adding the `--no-breaking` option.
```

### Update the test matrix

```{note}
Only relevant for Plone core packages
```

As the switch to the native namespace has to be coordinated, all python distributions need to be only for the same Plone version, in this case it was decided to do it for the Plone 6.2 version.

Thus, we need to ensure that the test matrix only tests against this Plone version.

For that, update `.meta.toml` with the following changes:

```toml
[tox]
test_matrix = {"6.2" = ["*"]}
```

And update the scaffolding files with `plone.meta`:

```shell
uvx --from plone.meta config-package --branch current .
```

Review the changes and ensure all changes are sound.

```{note}
If the diff is quite big, run `config-package` before all the changes, get that on a Pull Request, approved and merged and then do a follow up Pull Request to move to native namespace.
```

### Compare numbers

Get the list of tests, like before and compare the lists to ensure that the same amount of tests are found.

```shell
tox run -e test -- --list-tests | wc -l
```

Likewise, create the distribution files and compare the numbers with the previous run:

```shell
rm -rf dist/
uvx --from build pyproject-build
python -c "import glob; import tarfile; print(len(tarfile.open(glob.glob('dist/*.tar.gz')[0], 'r:gz').getnames()))"
python -c "import glob; from zipfile import ZipFile; print(len(ZipFile(glob.glob('dist/*.whl')[0]).namelist()))"
```

It is okay if the numbers are slightly lower.
For obvious reasons the old source distribution will have one or more extra `__init__.py` files.
Both old distributions are expected to have an extra `namespace_packages.txt` file and possible an `x-nspkg.pth` file.
If you lose more than a few files though, something is wrong.

If the numbers are close enough, review the changes once more, and push the branch with the changes for others to review it.
