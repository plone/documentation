============================
Creating a Dexterity project
============================

Dexterity is covered in detail in the `Dexterity Developer Manual <http://docs.plone.org/external/plone.app.dexterity/docs/>`_, which includes an extensive tutorial on setting up a Dexterity development environment and creating Dexterity add-on packages.

Here, we'll just add a few details on setting up and using the bobtemplates.plone package creator for use with Dexterity.

The only prerequisite is a working Plone buildout and to have added mr.bob and bobtemplates.plone part described in :doc:`bootstrapping </develop/addons/bobtemplates.plone/README>`.


Create a dexterity product
==========================

Use bobtemplates.plone to create a Python package which contains a Dexterity-based product.

.. code-block::

    mrbob -O collective.myaddon bobtemplates:plone_addon

    Welcome to mr.bob interactive mode. Before we generate directory structure, some questions need to be answered.

    Answer with a question mark to display help.
    Values in square brackets at the end of the questions show the default value if there is no answer.


    --> What kind of package would you like to create? [Basic]: Dexterity

    --> Content type name [Task]:

    --> Author's name [$NAME]:

    --> Author's email [$EMAIL]:

    --> Author's github username:

--> Package description [An add-on for Plone]:

--> Plone version [4.3.4]:


Generated file structure at $/collective.myaddon


Add your package to buildout
============================

Edit your ``buildout.cfg`` file to add the package to your ``egg`` list and your ``develop`` list. Run buildout.
