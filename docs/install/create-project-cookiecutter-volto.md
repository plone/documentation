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

In this chapter the usage of the currently experimental {term}`cookiecutter` project for creating Plone 6 projects with a new build setup using {term}`pnpm` is described.
In order to get started you will need {term}`pipx` - as described in the prerequisites section of `plone/cookiecutter-volto` - {term}`Make`, {term}`Node.js` and {term}`Docker`.
After that you can run following command to create your project:
```shell
pipx run cookiecutter gh:plone/cookiecutter-volto
```

(create-a-project-with-cookiecutter-volto-experimental-installation-label)=

## Installation

(create-a-project-with-cookiecutter-volto-experimental-installation-gnu-make-label)=

### pipx

See the prerequisites section of `plone/cookiecutter-volto`.

(create-a-project-with-cookiecutter-volto-experimental-installation-pipx-label)=

### GNU make

```{include} ../volto/contributing/install-make.md
```

(create-a-project-with-cookiecutter-volto-experimental-installation-node.js-label)=

### Node.js

You can use nvm to install the latest LTS version of {term}`Node.js` (LTS 20.x).

(create-a-project-with-cookiecutter-volto-experimental-installation-docker-label)=

### Docker

{term}`Docker` is needed later to start the plone backend inside a container.
Install {term}`Docker` according to the [official documentation](https://docs.docker.com/get-docker/).


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