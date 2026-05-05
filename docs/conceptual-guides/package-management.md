---
myst:
  html_meta:
    "description": "Package management in Plone."
    "property=og:description": "Package management in Plone."
    "property=og:title": "Package management"
    "keywords": "Plone 6, package management, mxdev"
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


(manage-backend-python-packages-label)=

## Manage backend Python packages

If you want to check out a Plone core package for development, or want to override the constraints of Plone, normally you would define constraints with a file {file}`constraints.txt` to tell `pip` to install a different version of a Plone package.

```text
# constraints.txt with unresolvable version conflict
-c https://dist.plone.org/release/6.0.9/constraints.txt
plone.api>=2.1.0
```

Unfortunately `pip` does not allow overriding constraints this way.
{term}`mxdev` solves this issue.


### `mxdev` to the rescue!

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


## Manage frontend Node.js packages

```{todo}
Why do we use pnpm?
```
