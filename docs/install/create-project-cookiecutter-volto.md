---
myst:
  html_meta:
    "description": "Create a project with cookiecutter-volto (experimental)"
    "property=og:description": "Create a project with cookiecutter-volto (experimental)"
    "property=og:title": "Create a project with cookiecutter-volto (experimental)"
    "keywords": "Plone, Plone 6, create, project, install, cookiecutter-volto, pnpm"
---

(create-a-project-with-cookiecutter-volto-experimental-label)=

# Create a project with cookiecutter-volto (experimental)

This chapter describes the usage of the currently experimental {term}`cookiecutter` project [plone/cookiecutter-volto](https://github.com/plone/cookiecutter-volto/).
The development of this add-on is done in isolation using a new approach using {term}`pnpm` workspaces and latest {term}`mrs-developer` and other Volto core improvements.
In order to get started you will need {term}`pipx`, {term}`Make`, {term}`Node.js` and {term}`Docker` see {ref}`create-a-project-with-cookiecutter-volto-experimental-installation-label` section below.

After that you can run following command to create your project:
```shell
pipx run cookiecutter gh:plone/cookiecutter-volto
```

(create-a-project-with-cookiecutter-volto-experimental-installation-label)=

## Installation

(create-a-project-with-cookiecutter-volto-experimental-installation-pipx-label)=

### pipx

Install {term}`pipx`.

```shell
pip install pipx
```

(create-a-project-with-cookiecutter-volto-experimental-installation-gnu-make-label)=

### GNU make

```{include} ../volto/contributing/install-make.md
```

(create-a-project-with-cookiecutter-volto-experimental-installation-node.js-label)=

### Node.js

First you'll need nvm, {term}`Node Version Manager`.

#### nvm

The following terminal session commands use `bash` for the shell.
Adapt them for your flavor of shell.

```{seealso}
See the [`nvm` install and update script documentation](https://github.com/nvm-sh/nvm#install--update-script).
For the `fish` shell, see [`nvm.fish`](https://github.com/jorgebucaran/nvm.fish).
```

1.  Create your shell profile, if it does not exist.

    ```shell
    touch ~/.bash_profile
    ```

2.  Download and run the `nvm` install and update script, and pipe it into `bash`.

    ```shell
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v{NVM_VERSION}/install.sh | bash
    ```

3.  Source your profile.
    Alternatively close the session and open a new one.

    ```shell
    source ~/.bash_profile
    ```

4.  Verify that the `nvm` version is that which you just installed or updated:

    ```shell
    nvm --version
    ```
#### Finally install Node.js

```{include} ../volto/contributing/install-nodejs.md
```

(create-a-project-with-cookiecutter-volto-experimental-installation-docker-label)=

### Docker

{term}`Docker` is needed later to start the plone backend inside a container.

```{include} ../volto/contributing/install-docker.md
```


(project-add-ons-label)=

# Project Add-Ons

After having initially built frontend and backend using the command `make install`,
you will have the configuration file {file}`volto.config.js` (and other stuff) inside your top add-on folder:
```js
const addons = ['youraddon'];
const theme = '';

module.exports = {
  addons,
  theme,
};
```

In {file}`volto.config.js` you can add add-ons like this:
```js
const addons = ['youraddon','@kitconcept/volto-light-theme'];
```

You also have to add it to the `dependencies` section of {file}`packages/youraddon/package.json`:
```json
  "dependencies": {
    "@plone/components": "1.7.0",
    "@kitconcept/volto-light-theme" : "^3.2"
  },
```

If your desired add-on is a theme addon, you should also change following line in {file}`volto.config.js`:
```js
const theme = '@kitconcept/volto-light-theme';
```

After all that, you have to execute `make install` again in order to install the new add-on.

(start-frontend-and-backend)=

# Start frontend and backend
Now you are ready to run your project.
You can start frontend and backend in separate terminal sessions in the same project directory:

```shell
make start-backend-docker
```

```shell
pnpm start
```

(change-the-logo-label)=

## Change the Logo

You can change the logo locally or by overriding Logo component of an installed theme add-on e.g. `kitconcept/volto-light-theme`.

`````{tab-set}
````{tab-item} local
In order to override the Logo component, you will have to add following file:
{file}`packages/youraddon/src/customizations/components/Logo/Logo.jsx`

Then you only have to change the line where the logo gets imported to:
```js
import LogoImage from '../../../../../images/Logo.svg';
```

Assuming you got your Logo ready in an local images folder like {file}`packages/youraddon/src/images/Logo.svg`
````

````{tab-item} volto-light-theme
Target Add-On Component: `src/components/Logo/Logo.jsx` of `kitconcept/volto-light-theme`

Of course, this only works if you have already installed the `kitconcept/volto-light-theme` add-on.

In order to override the Logo component of the volto-light-theme package, you will have to add following file:
{file}`packages/youraddon/src/customizations/@kitconcept/volto-light-theme/components/Logo/Logo.jsx`

Then you only have to change the line where the logo gets imported to:
```js
import LogoImage from '../../../../../images/Logo.svg';
```

Assuming you got your Logo ready in an local images folder like {file}`packages/youraddon/src/images/Logo.svg`
````
`````
