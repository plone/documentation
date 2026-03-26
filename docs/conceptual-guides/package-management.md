---
myst:
  html_meta:
    "description": "Package management in Plone."
    "property=og:description": "Package management in Plone."
    "property=og:title": "Package management"
    "keywords": "Plone 6, package management, pip, uv, mxdev"
---

# Package management

Plone 6 consists of a collection of Python and Node.js packages.
Over the decades of its existence, Plone has used several package management tools, sometimes multiple tools at one time.
Each one has its strengths and weaknesses for performing specific tasks, such as installation, conflict resolution, updates and upgrades, and working with virtual environments and across platforms.

With Volto as the default frontend in Plone 6, first npm, then pnpm, was brought into the mix as a package manager for its Node.js packages.

Python itself has a complex and convoluted history with package management, as [xkcd](https://xkcd.com/1987/) illustrates.

```{image} /_static/conceptual-guides/xkcd-1987-python-environment.png
:alt: A comic from xkcd entitled Python Environment
:class: figure
:target: https://xkcd.com/1987/
```


## Manage backend Python packages

### pip

By convention in the Python community, {term}`pip` is commonly used to install Python packages.
It is one supported way to install the Plone backend.

Each Plone version requires specific versions of many different packages.
So, pip should be used with constraints to make sure the correct versions are installed.
For example:

```shell
bin/pip install -c https://dist.plone.org/release/6.1-latest/constraints.txt Plone
```

In the Plone community, constraints are sometimes called "version pins."

As a best practice, pip should always be used inside a specific Python {term}`virtual environment` to keep the packages separate from other applications.

(manage-packages-mxdev-label)=

### mxdev

During development, it is sometimes necessary to override the Plone version constraints.
This makes it possible to:
- install a newer version of a core Plone package that was released with a bugfix
- install an unreleased core Plone package from a source control system

Unfortunately pip does not allow overriding constraints this way.
{term}`mxdev` solves this issue.

`mxdev` resolves Plone constraints according to your needs for pinning versions or source checkouts.
It reads its configuration file {file}`mx.ini`, and your {file}`requirements.txt` and {file}`constraints.txt` files.
Then it fetches the requirements and constraints of Plone.
Finally, it writes new combined requirements in {file}`requirements-mxdev.txt` and new constraints in {file}`constraints-mxdev.txt`.
Together these two files contain the combined requirements and constraints, but modified according to the configuration in {file}`mx.ini`.
The generated files indicate from where the constraints were fetched, and comments are added when a modification was necessary.

`mxdev` does not run `pip` or install packages.
You or your development tools, such as GNU Make, must perform that step.

```{seealso}
{doc}`/admin-guide/add-ons`
```

### uv

More recently, {term}`uv` has become popular as a way to install Python packages.
This package manager is popular for its speed, its ability to manage the installation of Python itself, and its ability to consistently reproduce installed packages using a {file}`uv.lock` file.

When a project is fully managed using uv, it is configured in `pyproject.toml` and the packages are installed using `uv sync`.

uv also has a backwards-compatible mode which works more like pip, and installs packages into a virtual environment via the command `uv pip install`.

If you create a Plone project using Cookieplone, it creates a backend managed by uv.

### buildout

{term}`Buildout` is a tool for installing Python packages that has been used in the Plone community since about 2007, and is still preferred by some members of the community.

It not only installs packages, but can set up other things using an extensible system of "recipes."

Buildout does not install Python packages into a virtual environment.
Instead, it creates scripts that add the necessary packages to `sys.path` before running the script target.

## Manage frontend Node.js packages

### pnpm

Plone uses {term}`pnpm` to install Node.js packages.

Compared to the standard {term}`npm`, it has features that help with developing multiple Node.js packages in the same workspace.
In Plone, this is used to manage the installation of your project add-on alongside Volto core and other add-ons.
