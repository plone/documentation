==========
Quickstart
==========

.. admonition:: Description

	A quick overview to get you up and running with Plone.


Online demo sites
=================

If you're just curious to see how Plone looks, without any modifications, there are a few online demo sites that can help you.
Both `plone-demo.quintagroup.com <http://plone-demo.quintagroup.com/>`_ and `plonedemo.com <http://plonedemo.com/>`_ provide you with a Plone 4.3 site that is re-set every day.

You can also try out the upcoming Plone 5 release (do note though this is an early alpha release) at `plone5.veit-schiele.de <https://plone5.veit-schiele.de/>`_

An interesting approach was developed by Nejc Zupan: `Plone on a free-tier Heroku <http://www.niteoweb.com/blog/dear-plone-welcome-to-2014>`_ . That way, you can set up your own demo (or even very-light-weight production) Plone, which makes it a good fit to have Plone with your choice of add-ons be tested by your department or other group.



Plone on your own machine
=========================

You may find information on all methods of installing Plone at the :doc:`Installation </manage/installing/index>` chapter in the "Managing, Administration" section of these docs.
Or, head straight to `plone.org/download <https://plone.org/download>`_ to get started now!

A quick guide to installation options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For evaluation or demonstration
```````````````````````````````

For a quick install of Plone 5, you may install Plone in a virtual environment on nearly any computer. Just use the VirtualBox Appliance, found on our `Plone 5 download page <https://plone.org/products/plone/releases/5.0>`_.

For earlier versions of Plone, you may use the VirtualBox/Vagrant Install Kit to create a virtual machine.

On Linux, BSD and OS X machines, you also have the option to use our Unified Installer to install a complete demo/production/development Plone. See the :doc:`Installation </manage/installing/index>` chapter.

For development
```````````````

On Windows or OS X, you may use the VirtualBox/Vagrant kit to build Plone in a virtual machine running locally. This kit allows you to use host OS tools for editing.

On Linux, BSD, OS X, and many other Unix workalikes, use the Unified Installer.

For a production server
```````````````````````
See the :doc:`Installation </manage/installing/index>` chapter for complete details.
You'll generally wish to use the Unified Installer or our Ansible full-stack deployment kit.

The installation chapter details many security and efficiency issues you'll wish to consider for a production-server deployment.

Any deployment of Plone as a real-world site will usually entail setting up a full software stack.
In almost all cases, you will want to have a webserver like NGINX or Apache in front, and a cache like Varnish to optimize response times.

Depending on your needs, you might also want redundant, high-availability options like ha-proxy, and monitoring tools to keep an eye on things and notify you when trouble arises.

A good selection of these tools is described  in the :doc:`Guide to deploying and installing Plone in production </manage/deploying/index>`.


Alternative ways to deploy
^^^^^^^^^^^^^^^^^^^^^^^^^^

The Universal Installer itself is based on `buildout <http://www.buildout.org>`_. If you're working with Plone a lot, it is a good idea to get familiar with this tool and the relation with other Python module management tools.

Buildout can be used in a variety of ways, and many people use it to tweak their own development-instances and/or deployment instances. See  `collective.minimalplone4 <https://github.com/collective/minimalplone4>`_ for a very bare-bones example, and
`starzel.buildout <https://github.com/starzel/buildout>`_ for a rather maximalized example.

Note however, that your chances of :doc:`getting help </askforhelp>` on setup questions in the Plone support channels (IRC, community.plone.org, mailinglists) increase when other people can reproduce your outcomes, which is most efficiently done with the Universal Installer.

Besides that, there are many people deploying Plone as part of other deployment tools, be they Ansible, Salt, Chef, Puppet or the like. If you are familiar with these, you will most likely find others in the Plone community that share your enthusiasm.


