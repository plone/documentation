---
myst:
  html_meta:
    "description": "Troubleshoot development issues in Plone"
    "property=og:description": "Troubleshoot development issues in Plone"
    "property=og:title": "Troubleshoot development issues in Plone"
    "keywords": "Troubleshoot, development issues, Plone"
---

# Troubleshoot

This chapter describes how to troubleshoot development issues in Plone.


## Buildout issues

This section describes issues you might experience with using buildout.


### `bootstrap.py` errors

When attempting to run buildout via the {file}`bootstrap.py`, the script exits with a `VersionConflict` error message.

```shell
 File "/usr/local/lib/python2.6/site-packages/distribute-0.6.13-py2.6.egg/pkg_resources.py", line 556, in resolve
    raise VersionConflict(dist,req)
 pkg_resources.VersionConflict: (zc.buildout 1.5.1 (/usr/local/lib/python2.6/site-packages/zc.buildout-1.5.1-py2.6.egg), Requirement.parse('zc.buildout==1.5.2'))
```

Buildout has noticed that the version of buildout required by the file `bootstrap.py` does not match the version of buildout in your Python path.
In the error above, your system has buildout 1.5.1 installed and the `bootstrap.py` file wants to run with 1.5.2.

You have two options to resolve the issue.

1.  You can force buildout to run with the version you already have installed by invoking the version tag.
    This tells your Plone {file}`bootstrap.py` file to play nicely with the version that you already have installed.
    In the case of the error pasted above, that would be:

    ```shell
    python bootstrap.py --version=1.5.1
    ```

1.  The other option is to delete your current egg and force the upgrade.
    In the case of the error above, delete the egg the system currently has, for example:

    ```shell
    rm -rf /usr/local/lib/python3.10/site-packages/zc.buildout-1.5.1-py3.10.egg
    ```

    When you rerun {file}`bootstrap.py`, it will look for the buildout of the egg, note that there isn't one, and then go fetch a new egg in the version that it wants for you.

Do one of those and re-run {file}`bootstrap.py`.

When you run {file}`bootstrap.py`, it effectively ties that Python executable and all of its libraries to your buildout.
If you have several Python installs, and want to switch which Python is tied to your buildout, rerun {file}`bootstrap.py` with the new Python, and then rerun buildout.
