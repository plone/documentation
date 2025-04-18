---
myst:
  html_meta:
    "description": "Create a backend add-on for Plone"
    "property=og:description": "Create a backend add-on for Plone"
    "property=og:title": "Create a backend add-on for Plone"
    "keywords": "Plone, create, add-on, plonecli, mr.bob, bobtemplates.plone, Cookieplone, buildout, backend"
---

(create-backend-add-on-label)=

# Create backend add-on

This chapter describes how to create a backend add-on for Plone using {term}`plonecli`.

```{note}
This chapter does not apply for either of the following methods, because they create a backend add-on, as well as install Plone for development.

-   {doc}`/install/create-project-cookieplone`
-   `uvx cookieplone backend_addon` command

Additionally, if you created a frontend add-on only project using the command `uvx cookieplone frontend_addon` and later realized you need a backend add-on to complement it, then you can create a new project using the command `uvx cookieplone` to generate both the frontend and backend add-ons, then finally move files from your existing project to the new one.
```


## Prerequisites

-   You've installed Plone for development through either of the following methods.

    -   {doc}`/admin-guide/install-buildout`
    -   {doc}`/admin-guide/install-pip`

-   {term}`plonecli` is designed for developing backend add-ons—or packages—for Plone.

    You can install `plonecli` as any other Python package.
    Since it's used for development, it's advantageous to install it in your user environment, thus making it available to all your Plone projects.

    ```shell
    python -m pip install plonecli --user
    ```


## `plonecli` usage

Change your working directory to the root of your Plone development installation for your project.
Create the backend add-on with the following command.

```shell
plonecli create addon src/collective.myaddon
```

Answer the prompts by either hitting the {kbd}`Enter` key to accept the default value, or entering a custom value.

```console
RUN: bobtemplates.plone:addon -O src/collective.myaddon

Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

Answer with a question mark to display help.
Values in square brackets at the end of the questions show the default value if there is no answer.


--> Author's name [YOUR NAME]: 

--> Author's email [YOUR EMAIL]: 

--> Author's GitHub username:

--> Package description [An add-on for Plone]: 

--> Do you want me to initialize a GIT repository in your new package? (y/n) [y]: 

--> Plone version [6.0.0]: 

--> Python version for virtualenv [python3]: 

--> Do you want me to activate VS Code support? (y/n) [y]: 

<snip>

Should we run?:
git add .
git commit -m Create addon: collective.myaddon
in: /path/to/buildout/project/src/collective.myaddon
[y]/n: 
RUN: git add .
RUN: git commit -m Create addon: collective.myaddon

Generated file structure at /path/to/buildout/project/src/collective.myaddon/src/collective.myaddon
```

You can now start developing your new add-on and add features to it.


### Available templates

To list the available {term}`mr.bob` templates, issue the following command.

```shell
plonecli -l
```

You should see output similar to the following.

```console
 - addon
  - behavior
  - content_type
  - controlpanel
  - form
  - indexer
  - mockup_pattern
  - portlet
  - restapi_service
  - site_initialization
  - subscriber
  - svelte_app
  - theme
  - theme_barceloneta
  - theme_basic
  - upgrade_step
  - view
  - viewlet
  - vocabulary
 - buildout
```


(backend-add-on-subtemplates-label)=

### Subtemplates

You can add different features to your add-on through subtemplates, using any of the available mr.bob templates.
You can use them multiple times to create different features of the same type, such as two different content types.

First change your working directory into the root of your add-on.
Then issue the command to add a feature as a subtemplate, and answer the prompts.

```shell
cd src/collective.myaddon/
plonecli add <TEMPLATE>
```

```{seealso}
The `plonecli` `README.md` has a section on [Usage](https://github.com/plone/plonecli?tab=readme-ov-file#usage).
```

```{seealso}
-   {doc}`create-control-panel`
```