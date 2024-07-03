---
myst:
  html_meta:
    "description": "Create a frontend project with cookieplone (experimental)"
    "property=og:description": "Create a frontend project with cookieplone (experimental)"
    "property=og:title": "Create a frontend project with cookieplone (experimental)"
    "keywords": "Plone, Plone 6, create, project, frontend, install, cookieplone, pnpm"
---

(create-a-frontend-project-with-cookieplone-experimental-label)=

# Create a frontend project with `cookieplone` (experimental)

This chapter describes the usage of the currently experimental {term}`cookiecutter` project [`cookieplone`](https://github.com/plone/cookieplone/).
The development of this add-on is done in isolation using {term}`pnpm` workspaces, {term}`mrs-developer`, and other Volto core improvements.
It only works with pnpm and Volto 18 (currently alpha) and only supports frontend development. So you can develop your Plone 6 frontend using latest and advanced technologies.


(create-a-frontend-project-with-cookieplone-experimental-prerequisites-label)=

## Prerequisites

The following items are required to create a frontend project with `cookieplone`.

```{include} ../volto/contributing/install-operating-system.md
```

-   Python {SUPPORTED_PYTHON_VERSIONS}
-   {term}`pipx`
-   {term}`nvm`
-   {term}`Node.js` LTS 20.x
-   {term}`GNU make`
-   {term}`Docker`
-   {term}`Git`

(create-a-frontend-project-with-cookieplone-experimental-installation-pipx-label)=

### pipx

Install pipx.

```shell
pip install pipx
```

(create-a-frontend-project-with-cookieplone-experimental-installation-gnu-make-label)=

### GNU make

```{include} ../volto/contributing/install-make.md
```


(create-a-frontend-project-with-cookieplone-experimental-installation-nvm-label)=

### nvm

```{include} ../volto/contributing/install-nvm.md
```


(create-a-frontend-project-with-cookieplone-experimental-installation-node.js-label)=

### Node.js

```{include} ../volto/contributing/install-nodejs.md
```


(create-a-frontend-project-with-cookieplone-experimental-installation-make-label)=

### Make

```{include} ../volto/contributing/install-make.md
```
(create-a-frontend-project-with-cookieplone-experimental-installation-docker-label)=

### Docker

{term}`Docker` is needed later to start the plone backend inside a container.

```{include} ../volto/contributing/install-docker.md
```




(create-a-frontend-project-with-cookieplone-experimental-create-the-project-label)=

## Create the project

After satisfying the prerequisites and having activated a LTS version of Node, create the project.

```shell
pipx install cookieplone
pipx run cookieplone frontend_addon
```

## Build the frontend and backend

To work on your project, you need to build both the frontend and backend. As already mentioned, only frontend development is supported. The Plone backend is Docker-based.

```shell
corepack enable
make install
```

```{tip}
We need to use pnpm with corepack. So it is necessary to activate the use of pnpm in corepack before using `corepack enable` with following command:

`corepack prepare pnpm@latest --activate`

If you like to specify the version of pnpm, you need to run this after `corepack enable`:

`corepack use pnpm@latest`

This will add a "packageManager" field in your local package.json which will instruct corepack to always use a specific version on that project.
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
