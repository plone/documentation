---
myst:
  html_meta:
    "description": "Create a project with cookiecutter-volto (experimental)"
    "property=og:description": "Create a project with cookiecutter-volto (experimental)"
    "property=og:title": "Create a project with cookiecutter-volto (experimental)"
    "keywords": "Plone, Plone 6, create, project, install, cookiecutter-volto, pnpm"
---

(create-a-project-with-cookiecutter-volto-experimental-label)=

# Create a project with `cookiecutter-volto` (experimental)

This chapter describes the usage of the currently experimental {term}`cookiecutter` project [`cookiecutter-volto`](https://github.com/plone/cookiecutter-volto/).
The development of this add-on is done in isolation using {term}`pnpm` workspaces, {term}`mrs-developer`, and other Volto core improvements.


(create-a-project-with-cookiecutter-volto-experimental-prerequisites-label)=

## Prerequisites

The following items are required to create a project with `cookiecutter-volto`.

```{include} ../volto/contributing/install-operating-system.md
```

-   Python {SUPPORTED_PYTHON_VERSIONS}
-   {term}`pipx`
-   {term}`nvm`
-   {term}`Node.js` LTS 20.x
-   {term}`GNU make`
-   {term}`Docker`
-   {term}`Git`

(create-a-project-with-cookiecutter-volto-experimental-installation-pipx-label)=

### pipx

Install pipx.

```shell
pip install pipx
```

(create-a-project-with-cookiecutter-volto-experimental-installation-gnu-make-label)=

### GNU make

```{include} ../volto/contributing/install-make.md
```




### nvm

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

(create-a-project-with-cookiecutter-volto-experimental-installation-node.js-label)=

### Node.js

```{include} ../volto/contributing/install-nodejs.md
```


(create-a-project-with-cookiecutter-volto-experimental-installation-make-label)=

### Make

```{include} ../volto/contributing/install-make.md
```
(create-a-project-with-cookiecutter-volto-experimental-installation-docker-label)=

### Docker

{term}`Docker` is needed later to start the plone backend inside a container.

```{include} ../volto/contributing/install-docker.md
```




(create-a-project-with-cookiecutter-volto-experimental-create-the-project-label)=

## Create the project

After satisfying the prerequisites, create the project.

```shell
pipx run cookiecutter gh:plone/cookiecutter-volto
```


## Build the frontend and backend

To work on your project, you need to build both the frontend and backend.

```shell
make install
```


(project-add-ons-label)=

## Project add-ons

Now that you have a project and built both the frontend and backend, you will have the configuration file {file}`volto.config.js` (and other stuff) inside your top add-on folder:

```js
const addons = ['youraddon'];
const theme = '';

module.exports = {
  addons,
  theme,
};
```

In {file}`volto.config.js`, you can add add-ons like this:

```js
const addons = ['youraddon','@kitconcept/volto-light-theme'];
```

You also have to add it to the `dependencies` section of {file}`packages/<YOUR_ADD_ON>/package.json`:

```json
  "dependencies": {
    "@plone/components": "1.7.0",
    "@kitconcept/volto-light-theme" : "^3.2"
  },
```

If your desired add-on is a theme add-on, you should also change the following line in {file}`volto.config.js`:

```js
const theme = '@kitconcept/volto-light-theme';
```

After all that, you need to run `make install` again to install the new add-on.

(start-frontend-and-backend)=

## Start frontend and backend
Now you are ready to run your project.
You must start the frontend and backend in separate terminal sessions from the same working directory, at the root of your project.

```shell
make start-backend-docker
```

```shell
pnpm start
```

(change-the-logo-label)=

## Change the Logo

You can change the logo locally, or by overriding the `Logo` component of an installed theme's add-on, for example, `kitconcept/volto-light-theme`.

`````{tab-set}
````{tab-item} local
To override the `Logo` component, you will have to add a file {file}`packages/youraddon/src/customizations/components/Logo/Logo.jsx`.

Then change the line where the logo gets imported:

```js
import LogoImage from '../../../../../images/Logo.svg';
```

This assumes your logo is in a local `images` folder, such as {file}`packages/<YOUR_ADD_ON>/src/images/Logo.svg`.
````

````{tab-item} volto-light-theme
Target add-on component: `src/components/Logo/Logo.jsx` of `kitconcept/volto-light-theme`

Of course, this only works if you have already installed the `kitconcept/volto-light-theme` add-on.

To override the `Logo` component of the `volto-light-theme` package, add the file {file}`packages/youraddon/src/customizations/@kitconcept/volto-light-theme/components/Logo/Logo.jsx`.

Then change the line where the logo gets imported:
```js
import LogoImage from '../../../../../images/Logo.svg';
```

This assumes your logo is in a local `images` folder, such as {file}`packages/<YOUR_ADD_ON>/src/images/Logo.svg`.
````
`````
