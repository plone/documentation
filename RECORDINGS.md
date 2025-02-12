# Recordings

This file describes the steps needed to set up an environment to record images and videos for Plone 6 Documentation.


## Set up the environment

Open a terminal session and issue the following command.

```shell
make recording-init
```

The command will run Cookieplone, generator a project, and install it.

This project will serve as baseline for the tests. Eventually, we could pull a specific branch for generating the tests.

Now you will start the backend, frontend, and acceptance test servers, one each in its own terminal session.

```{note}
None of these commands are documented anywhere.
You could run `make help`, and get a dump of the commands, but that lacks context for usage.
See https://github.com/plone/documentation/issues/1758.
```

In the current session, issue the following command to start the backend server.

```shell
make acceptance-backend-start
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
