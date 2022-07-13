# Install Plone Using A Minimal Buildout

```{note}
This example is adequate for a quick evaluation.

**Do not use it in production !**
```

Create a directory called `Plone-5` and enter it:

```shell
mkdir Plone-5
cd Plone-5
```

Create a virtual python environment ([virtualenv](https://virtualenv.pypa.io/en/stable/)) and install [zc.buildout](https://pypi.python.org/pypi/zc.buildout):

```shell
virtualenv-2.7 zinstance
cd zinstance
bin/pip install zc.buildout
```

Create a buildout.cfg file:

```ini
echo """
[buildout]
extends =
    http://dist.plone.org/release/5-latest/versions.cfg

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8080
eggs =
    Plone

""" > buildout.cfg
```

Run buildout:

```shell
./bin/buildout
```

This will start a long download and build process.

You can ignore Errors like `SyntaxError: ("'return' outside function"..."`.

After it finished you can start Plone in foreground-mode with:

```shell
./bin/instance fg
```

You can stop it with `ctrl + c`.

Start and stop this Plone-instance in production-mode like this;

```shell
./bin/instance start

./bin/instance stop
```

Plone will run on port 8080 you can access your install via <http://localhost:8080>.

Use login id "admin" and password "admin" for initial login so you can create a site.
