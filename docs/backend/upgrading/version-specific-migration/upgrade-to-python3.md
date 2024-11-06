---
myst:
  html_meta:
    "description": "Upgrading to Python 3 in Plone 5.2"
    "property=og:description": "Upgrading to Python 3 in Plone 5.2"
    "property=og:title": "Upgrading to Python 3 in Plone 5.2"
    "keywords": "Upgrading, Python 3, Plone 5.2"
---


(migrating-52-to-python3-label)=

# Migrating Plone 5.2 to Python 3

This chapter provides instructions and tips for porting Plone projects to Python 3.


## Principles

-   You should support Python 2 and 3 with the same codebase to allow it to be used in existing versions of Plone.
-   Plone 5.2 supports Python 2.7, Python 3.6, Python 3.7, and Python 3.8.
-   We use [six](https://six.readthedocs.io) and [modernize](https://pypi.org/project/modernize) for the first steps toward Python 3.

In general, you should follow these steps to port add-ons:

1.  Prepare `buildout` for the add-on to be ported.
2.  Update code with [python-modernize](https://python-modernize.readthedocs.io/en/latest/).
3.  Use [plone.recipe.precompiler](https://github.com/plone/plone.recipe.precompiler) (also called `precompiler` for brevity) to find syntax errors.
4.  Start the instance and find more errors.
5.  Test functionality manually.
6.  Run and fix all tests.
7.  Update package information.
8.  Update package buildout and test setup.


## 1. Preparation

In the GitHub repository of the add-on:

-   Open a ticket with the title "Add support for Python 3".
-   Create a new branch named `python3`.


### Using released Plone 5.2

Usually you can use the latest Plone 5.2 release.
The version pins for the latest release can be found for `pip` at https://dist.plone.org/release/5.2-latest/requirements.txt and for `buildout` at https://dist.plone.org/release/5.2-latest/versions.cfg.
Install Plone with Python 3.6, 3.7, or 3.8, and then add your add-ons as source using `mr.developer`.


### Using core development buildout

With [`buildout.coredev`](https://github.com/plone/buildout.coredev), the latest development version of Plone can be used.
It contains everything for porting an add-on to Python 3.
Follow these steps:

```shell
# Clone coredev and use branch 5.2:
git clone git@github.com:plone/buildout.coredev.git coredev_py3
cd coredev_py3
git checkout 5.2
# Create a py3 virtual environment with either Python 3.6, 3.7, or 3.8:
python3.8 -m venv .
# Install buildout:
./bin/pip install -r requirements.txt
```

Next create a file called `local.cfg` in the root of the buildout.
This file will be used to add your add-on to the buildout.
Add your package as in the following example.
Exchange `collective.package` with the name of the add-on you want to port.

```{note}
This example expects a branch with the name `python3` to exist for the package.
Adapt it for your use case.
```

```ini
[buildout]
extends = buildout.cfg

always-checkout = true
allow-picked-versions = true

custom-eggs +=
    collective.package

test-eggs +=
    collective.package [test]

auto-checkout +=
    collective.package

[sources]
collective.package = git git@github.com:collective/collective.package.git branch=python3
```

With the file in place, run `buildout`.
Then the source of the add-on package will be checked out into the `src` folder.

```shell
./bin/buildout -c local.cfg
```

````{note}
You can also add development tools like [`Products.PDBDebugMode`](https://pypi.org/project/Products.PDBDebugMode/), [`plone.reload`](https://pypi.org/project/plone.reload/) and [`Products.PrintingMailHost`](https://pypi.org/project/Products.PrintingMailHost/) to your `buildout`.

Especially `Products.PDBDebugMode` will help a lot with issues during porting to Python 3.

```ini
custom-eggs +=
    collective.package
    Products.PDBDebugMode
    plone.reload
    Products.PrintingMailHost

test-eggs +=
    collective.package [test]

auto-checkout +=
    collective.package
```
````

Now everything is prepared to work on the migration of the package.

For small packages or packages that have few dependencies, it is a good idea to try starting your instance now.

```shell
./bin/instance fg
```

If it does not start up, you should continue with the next steps instead of trying to fix each issue as it appears.


## 2. Automated fixing with modernize

`python-modernize` is a utility that automatically prepares Python 2 code for porting to Python 3.
After running `python-modernize`, there is manual work ahead.
There are some problems that `python-modernize` cannot fix on its own.
It also can make changes that are not really needed.
You need to closely review all changes after you run this tool.

`python-modernize` will warn you when it is not sure what to do with a possible problem.
Check this [Cheat Sheet](https://python-future.org/compatible_idioms.html) with idioms for writing Python 2/3 compatible code.

`python-modernize` adds an import of the compatibility library `six` if needed.
The import is added as the last import, therefore it is often necessary to reorder the imports.
The easiest way is to use [isort](https://pypi.org/project/isort), which does this for you automatically.
Check the [Python style guide for Plone](https://5.docs.plone.org/develop/styleguide/python.html#grouping-and-sorting) for information about the order of imports and an example configuration for `isort`.

If `six` is used in the code, make sure that `six` is added to the `install_requires` list in the `setup.py` of the package.


### Installation

Install `modernize` into your Python 3 environment with `pip`.

```shell
./bin/pip install modernize
```

Install `isort` into your Python 3 environment with `pip`.

```shell
./bin/pip install isort
```


### Usage

The following command is a dry-run. It shows all changes that `modernize` would make.

```shell
./bin/python-modernize -x libmodernize.fixes.fix_import  src/collective.package
```

```{note}
The `-x` option is used to exclude certain fixers.
The one that adds `from __future__ import absolute_import` should not be used.
See `./bin/python-modernize -l` for a complete list of fixers and the [fixers documentation](https://python-modernize.readthedocs.io/en/latest/fixers.html).
```

The following command applies all fixes to the files:

```shell
./bin/python-modernize -wn -x libmodernize.fixes.fix_import src/collective.package
```

You can use `isort` to fix the order of imports:

```shell
./bin/isort -rc src/collective.package
```

After you run the commands above, you need to review all changes and fix what `modernizer` did not get right.


## 3. Use `precompiler`

You can make use of `plone.recipe.precompiler` to identify syntax errors quickly.
This recipe compiles all Python code already at buildout-time, not at run-time.
You will see right away when there is some illegal syntax.

Add the following line to the section `[buildout]` in `local.cfg`.
Then run `./bin/buildout -c local.cfg` to enable and use `precompiler`.

```ini
parts += precompiler
```

`precompile` will be run every time you run buildout.
If you want to avoid running the complete buildout every time, you can use the `install` keyword of buildout like this as a shortcut:

```shell
./bin/buildout -c local.cfg  install precompiler
```


## 4. Start the instance

As a next step, we recommend that you try to start the instance with your add-on.
This will fail on all import errors (e.g., relative imports that are not allowed in Python 3).
If it works then you can try to install the add-on.

You need to fix all issues that appear before you can do manual testing to check for big, obvious issues.


### Common Issues during startup

The following issues will abort your startup.
You need to fix them before you are able to test the functionality by hand or run tests.


#### Class advice

If you get an error message similar to the following.

```console
TypeError: Class advice impossible in Python3.  Use the @implementer class decorator instead.
```

This tells you that there is a class using an `implements` statement which needs to be replaced by the `@implementer` decorator.

For example, code that is written as follows:

```python
from zope.interface import implements

class Group(form.BaseForm):
    implements(interface.IGroup)
```

needs to be replaced with:

```python
from zope.interface import implementer

@implementer(interfaces.IGroup)
class Group(form.BaseForm):
```

The same is true for `provides(IFoo)` and some other class advices.
These need to be replaced with their respective decorators, such as `@provider`.


#### Relative imports

Relative imports such as `import permissions` are no longer permitted.
Instead, use fully qualified import paths, such as `from collective.package import permissions`.


#### Syntax error on importing async

Starting with Python 3.7, you can no longer have a module called `async` (see https://github.com/celery/celery/issues/4849).
You need to rename all such files, folders, or packages (such as `zc.async` and `plone.app.async`).


## 5. Test functionality manually

Now that the instance is running, you should do the following, and fix all errors as they appear.

-   Install the add-on.
-   Test basic functionality, for example, adding and editing content types and views.
-   Uninstall the add-on.

For this step, it is recommended that you have installed `Products.PDBDebugMode` to help debug and fix issues.


## 6. Run Tests

```shell
$ ./bin/test --all -s collective.package
```

Remember that you can run `./bin/test -s collective.package -D` to enter a `pdb` session when an error occurs.

With some luck, there will not be too many issues left with the code at this point.

If you are unlucky, then you have to fix doctests.
These should be changed so that Python 3 is the default.
For example, string types (or text) should be represented as `'foo'`, not `u'foo'`, and bytes types (or data) should be represented as `b'bar'`, not `'bar'`.
Search for examples of `Py23DocChecker` in Plone's packages to find a pattern which allows updated doctests to pass in Python 2.


## 7. Update add-on information

Add the following four entries of the classifiers list in `setup.py`.

```python
"Framework :: Plone :: 5.2",
# ...
"Programming Language :: Python :: 3.6",
"Programming Language :: Python :: 3.7",
"Programming Language :: Python :: 3.8",
```

Make an entry in the `CHANGES.rst` file.


## 8. Create a test setup that tests in Python 2 and Python 3

You need to update the `buildout` of the add-on you are migrating to also support Plone 5.2 and Python 3.
Since the `buildout` of most add-ons are different, we cannot offer advice that works for all add-ons.

But it is a good idea to create an empty new package with {py:mod}`bobtemplates.plone`, and either copy the code of the add-on in there or the new skeleton files into the old add-on.
The least you can do is look at the files created by {py:mod}`bobtemplates.plone`, and copy whatever is appropriate to the add-on you are working on.

```
$ ./bin/pip install bobtemplates.plone
$ ./bin/mrbob -O some.addon bobtemplates.plone:addon
```

Always use the newest version of {py:mod}`bobtemplates.plone`!

Add-ons created like this contain a setup that allows testing in Python 2 and Python 3, and various Plone versions locally, and on Travis-CI using {py:mod}`tox`.
Look at the files `tox.ini` and `travis.yml`.


## 9. Frequent Issues


### Text and Bytes

This is by far the biggest issue when porting to Python 3.
Read the [Conservative Python 3 Porting Guide, Strings](https://portingguide.readthedocs.io/en/latest/strings.html) to be prepared.

```{note}
As a rule of thumb, you can assume that in Python 3 everything should be text.
Only in very rare cases will you need to handle bytes.
```

`python-modernize` will _not_ fix all your text/bytes issues.
It only replaces all cases of `unicode` with `six.text_type`.
You need to make sure that the code you are porting will remain unchanged in Python 2 and (at least in most cases) use text in Python 3.

Try to modify the code in such a way that when dropping support for Python 2 you will be able to delete while lines.
For example:

```python
if six.PY2 and isinstance(value, six.text_type):
    value = value.encode('utf8')
do_something(value)
```

You can use the helper methods `safe_text` and `safe_bytes` (`safe_unicode` and `safe_encode` in Plone 5.1).

`python-modernize` also does not touch the import statement `from StringIO import StringIO`, even though this works only in Python 2.
You have to check whether you are dealing with text or binary data and use the appropriate import statement from `six` (https://six.readthedocs.io/#six.StringIO).

```python
# For textual data
from six import StringIO
# For binary data
from six import BytesIO
```

```{seealso}
Here is a list of helpful references on the topic of porting Python 2 to Python 3.

-   https://portingguide.readthedocs.io/en/latest/index.html
-   https://eev.ee/blog/2016/07/31/python-faq-how-do-i-port-to-python-3/
-   https://diveintopython3.net/
-   https://docs.djangoproject.com/en/1.11/topics/python3/
-   https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html
-   https://docs.python.org/2/library/doctest.html#debugging
```
