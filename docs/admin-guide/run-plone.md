---
myst:
  html_meta:
    "description": "Run Plone"
    "property=og:description": "Run Plone"
    "property=og:title": "Run Plone"
    "keywords": "Plone 6, run, start, command, Cookieplone, Buildout, pip, cookiecutter-plone-starter"
---

(run-plone-label)=

# Run Plone

This chapter shows the commands to run Plone after it is installed.

There are different commands to run Plone, depending on which method you used to install Plone.

## Run Plone in foreground mode

Running Plone in foreground mode will show output in the terminal.
This is recommended while developing a Plone site.
The command you use depends on the installation method you used.

Cookieplone:
:   ```shell
    make backend-start
    ```

Buildout:
:   ```shell
    bin/instance fg
    ```

pip:
:   ```shell
    bin/runwsgi instance/etc/zope.ini
    ```

`cookiecutter-plone-starter`:
:   ```shell
    make start-backend
    ```

For any of these commands, press {kbd}`ctrl-c` to stop the process.


## Run Volto

If you use the Volto frontend, you need to run the frontend in a separate process and terminal session.

Cookieplone:
:   ```shell
    make frontend-start
    ```

`cookiecutter-plone-starter`:
:   ```shell
    make start-frontend
    ```

For any of these commands, press {kbd}`ctrl-c` to stop the process.


## Start Plone as a background service

Buildout:
:   ```shell
    bin/instance start
    ```

## Stop Plone as a background service

Buildout:
:   ```shell
    bin/instance stop
    ```

## Run a debug console

The debug console gives you a Python prompt with the Plone site's configuration loaded.
Use this for troubleshooting.

Cookieplone:
:   ```shell
    make -C backend console
    ```

Buildout:
:   ```shell
    bin/instance debug
    ```

pip:
:   ```shell
    bin/zconsole debug instance/etc/zope.conf
    ```

`cookiecutter-plone-starter`:
:   ```shell
    make -C backend debug
    ```

For any of these commands, press {kbd}`ctrl-d` to stop the process.

### Set a "fake" request

To make sure that the request is fully set up for any code that uses `zope.globalrequest.getRequest`, you might need to use the following code.

```python
from Testing.makerequest import makerequest
from zope.globalrequest import setRequest

app = makerequest(app)
setRequest(app.REQUEST)
```
