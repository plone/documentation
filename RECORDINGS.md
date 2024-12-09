# Recordings

This file describes the steps needed to set up an environment to record images and videos for Plone 6 Documentation.


## Set up the environment

Open a terminal session and issue the following command.

```shell
make recording-init
```

The command will run Cookieplone, generator a project, and install it.

Next edit the file `recordings/project-title/frontend/cypress.config.js`, inserting the emphasized line.

```{code-block} js
:emphasize-lines: 11
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  viewportWidth: 1280,
  viewportHeight: 1280,
  retries: {
    runMode: 3,
  },
  e2e: {
    baseUrl: 'http://localhost:3000',
    experimentalStudio: true,
    specPattern: 'cypress/tests/**/*.cy.{js,jsx,ts,tsx}',
  },
});
```

Copy all the tests from {file}`submodules/volto/packages/volto/cypress` to {file}`recordings/project-title/frontend/cypress` so you have something to start from.

Now you will start the backend, frontend, and acceptance test servers, one each in its own terminal session.

```{note}
None of these commands are documented anywhere.
You could run `make help`, and get a dump of the commands, but that lacks context for usage.
See https://github.com/plone/documentation/issues/1758.
```

In the current session, issue the following command to start the backend server.

```shell
make acceptance-backend-dev-start
```

In the second session, issue the following command to start the frontend server.

```shell
make acceptance-frontend-dev-start
```

In the third session, issue the following command to start the acceptance test server.

```shell
make acceptance-test
```

A new browser window will pop up.

Select {guilabel}`E2E Testing`.

Select {guilabel}`Chrome`, because it is the only browser that supports Cypress Studio.

Click {guilabel}`Start E2E Testing in Chrome`.

And that's pretty much as far as I got.
Even though I created a page, `/document`, and ran the sample test, it failed.
