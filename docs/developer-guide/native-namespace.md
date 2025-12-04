---
myst:
  html_meta:
    "description": "How to convert a Python distribution from a pkg_resources namespace to a native namespace"
    "property=og:description": "How to convert a Python distribution from a pkg_resources namespace to a native namespace"
    "property=og:title": "Native namespace"
    "keywords": "Plone 6, developer guide, native namespaces, pkg_resources, Python"
---

# Native namespace

This chapter is guide for how to convert a Python distribution from a `pkg_resources` namespace to a native namespace.

Python 3.3 added support for native namespaces.
See [PEP 420](https://peps.python.org/pep-0420/) for more details.

Plone has been using `pkg_resources`-style namespaces, but they are deprecated in `setuptools`.
`setuptools` is planning to remove `pkg_resources`'s namespace support by the end of 2025.
[PLIP 3928](https://github.com/plone/Products.CMFPlone/issues/3928) tracks the changes needed for Plone to adapt to the _new_ native namespaces.

To convert a given Python distribution to use a native namespace, follow these steps.


## Create maintenance branch

```{note}
This step is relevant only for Plone core packages.
```

```{tip}
This part is only needed when the `main` or `master` branch is used on multiple versions of the Plone core development buildout.
```

If you haven't cloned the package's repository, then do so.

```shell
git clone git@github.com:plone/$package
cd $package
```

Otherwise, pull the latest changes into your local repository.

```shell
git fetch -p
git checkout main # or master
git rebase
```

Find the last release tag, and create a branch for it.

List all tags.

```shell
git for-each-ref --sort=taggerdate --format '%(tag)' refs/tags
```

Get the last tag's major number.

```shell
MAJOR=`git for-each-ref --sort=taggerdate --format '%(tag)' refs/tags | tail -n1 | cut -d"." -f1`
```

Create a branch for it.

```shell
git checkout -b $MAJOR.x
```

Push the newly created branch.

```shell
git push
```


## Update `buildout.coredev`

```{note}
This step is relevant only for Plone core packages.
```

Update `buildout.coredev`'s branch `6.1` to use the newly created branch.

```shell
cd buildout.coredev
```

Ensure you have the latest changes.

```shell
git fetch -p
git checkout 6.1
git rebase
```

Update the branch being used by the Python distribution.

```shell
sed -i "s/$package.git branch=master/$package.git branch=$MAJOR.x/" sources.cfg
```

Add the changes, commit, and push.

```shell
git add sources.cfg
git commit -m"chore: use branch $MAJOR.x for $package"
git push
```

Now check if you need to do the same on the `6.0` branch of `buildout.coredev`.

```{tip}
You can use this [handy table](https://jenkins.plone.org/roboto/branches) to know which branch is used by a given package for each Plone version.
```

```{tip}
To lower the amount of builds in Jenkins, either do a few at a time or add a `[ci-skip]` on the commit message.
```

## Counts before change

There is a risk when changing to the native namespaces that some files, or tests, might be left behind.
To ensure all tests and files are kept after the switch, gather the counts before the change.

```shell
tox run -e test -- --list-tests | wc -l
```

```{note}
Adapt to whichever way you are using to run the tests.
The above is meant for repositories that follow `plone.meta` conventions.
The `--list-tests` comes from `zope.testrunner`, if you are using that, but not `plone.meta`, although you can use that as well.
```

Create a distribution to get a listing of how many files are currently packaged.

```shell
rm -rf dist/
uvx --from build pyproject-build
```

A `dist` folder is created with two archives in it, one each with the file suffix of `.tar.gz` and `.whl`.
To get the count of files in them, run the following commands.

```shell
python -c "import glob; import tarfile; print(len(tarfile.open(glob.glob('dist/*.tar.gz')[0], 'r:gz').getnames()))"
python -c "import glob; from zipfile import ZipFile; print(len(ZipFile(glob.glob('dist/*.whl')[0]).namelist()))"
```

Note these counts for later in the step {ref}`compare-counts-after-change`.


## Build backend

To ensure the package continues to build, verify that `setuptools` is defined as its build backend.
For that, inspect the {file}`pyproject.toml`.
It should have the following lines.

```toml
[build-system]
requires = ["setuptools>=68.2,<80", "wheel"]
```

If they are not there, then add them, commit, and push the changes.


## Convert to native namespace

Use `plone.meta`'s `switch-to-pep420` script.

```shell
cd $package
uvx --from plone.meta switch-to-pep420 --no-tests .
```

```{tip}
This will also bump the version to a new major release.

If the `main` or `master` branch is already an alpha version that is only used in Plone 6.2, you can specify that you don't want this version bump by adding the `--no-breaking` option.
```


## Update the test matrix

```{note}
This step is relevant only for Plone core packages.
```

Because the switch to the native namespace must be coordinated, all Python distributions need to be only for the same Plone version.
In this case, it was decided to do it for the Plone 6.2 version.
Thus, we need to ensure that the test matrix only tests against this Plone version.
For that, update {file}`.meta.toml` with the following changes.

```toml
[tox]
test_matrix = {"6.2" = ["*"]}
```

Update the scaffolding files with `plone.meta`.

```shell
uvx --from plone.meta config-package --branch current .
```

Review the changes and ensure all changes are sound.

```{note}
If the diff is quite big, then run `config-package` before all the changes.
Get the result into a pull request, approved, and merged.
Then do a follow up pull request to move it to a native namespace.
```


(compare-counts-after-change)=

## Compare counts after change

Get the list of tests, and compare this result to the earlier one to ensure the same test counts.

```shell
tox run -e test -- --list-tests | wc -l
```

Similarly, create the distribution files and compare the numbers with the previous run.

```shell
rm -rf dist/
uvx --from build pyproject-build
python -c "import glob; import tarfile; print(len(tarfile.open(glob.glob('dist/*.tar.gz')[0], 'r:gz').getnames()))"
python -c "import glob; from zipfile import ZipFile; print(len(ZipFile(glob.glob('dist/*.whl')[0]).namelist()))"
```

It is okay if the numbers are slightly lower.
For obvious reasons, the old source distribution will have one or more extra {file}`__init__.py` files.
Both old distributions are expected to have an extra {file}`namespace_packages.txt` file and possibly an {file}`x-nspkg.pth` file.
If you lose more than a few files though, something is wrong.

If the numbers are close enough, review the changes once more, and push the branch with the changes for others to review it.
