======================================
Install Plone Using A Minimal Buildout
======================================

With complete requirements in place, a Plone install may be created with a few steps.

Create a directory called Plone-5 and enter it:

.. code-block:: shell

   mkdir Plone-5
   cd Plone-5

Run the steps to create a virtual python environment (virtualenv) and install zc.buildout:

.. code-block:: shell

   virtualenv-2.7 zinstance
   cd zinstance
   bin/pip install zc.buildout

Create a buildout.cfg file:

.. code-block:: ini

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
      Pillow

  """ > buildout.cfg

Run buildout:

.. code-block:: shell

   /bin/buildout

This will start a long download and build process ...

Errors like SyntaxError: ("'return' outside function"..." may be ignored.

After it finished you can start Plone in foreground-mode with:

.. code-block:: shell

   bin/instance fg

You can stop it with ctrl + c.

Start and stop this Plone-instance in production-mode like this;

.. code-block:: shell

   bin/instance start

   bin/instance stop

Plone will run on port 8080 and can be accessed via http://localhost:8080. Use login id "admin" and password "admin" for initial login so you can create a site.

This build would be adequate for a quick evaluation installation. For a production or development installation, use one of Plone's installers.

