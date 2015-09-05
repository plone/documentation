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

The recommended and best supported way to deploy Plone, both for laptops as well as servers, is the Universal Installer.
It can provide you both with a single instance with developer tools installed, as well as with multiple failover clients running against a database server.

What this means it that it will scale from quick evaluation to development to deployment, which will make your experience easier.

The catch is that the Universal Installer works on Linux and Unix-like systems (including OS X and other BSD's), not Windows.
For Windows, there is a binary installer available.
In all honesty, though, this is not the ideal way to work with Plone if you want to develop with it.
A large portion of the toolchain is not readily available on Windows environments.

There is a highly workable alternative, though: Using virtual machines.
The latest release of Plone also comes as a Virtualbox / Vagrant image.
This will install a fully-working Plone for you in a virtual machine, but integrated with the host so that all your favourite Windows editing and development tools work.
If you want to develop with Plone on a Windows machine, that would be your easiest option.

For OS X users there is a also a binary installer available.
The Universal Installer works just fine under OS X, but does require use of the terminal. If that is something you'd like to avoid, the binary installer is your friend.

You can find all information on using these different options at the :doc:`Installation </manage/installing/index>` chapter in the "Managing, Administration" section of these docs.

Or, head straight to `plone.org/download <https://plone.org/download>`_ to get started now!



Deployment
==========

Any deployment of Plone as a real-world site will usually entail setting up some more software.
In almost all cases, you will want to have a webserver like NGINX or Apache in front, and a cache like Varnish to optimize response times.

Depending on your needs, you might also want redundant, high-availability options like ha-proxy, and monitoring tools to keep an eye on things and notify you when trouble arises.

A good selection of these tools is described  in the :doc:`Guide to deploying and installing Plone in production </manage/deploying/index>`.


Alternative ways to deploy
--------------------------

The Universal Installer itself is based on `buildout <http://www.buildout.org>`_. If you're working with Plone a lot, it is a good idea to get familiar with this tool and the relation with other Python module management tools.

Buildout can be used in a variety of ways, and many people use it to tweak their own development-instances and/or deployment instances. See `starzel.buildout <https://github.com/starzel/buildout>`_ for a rather maximalized example.

Note however, that your chances of :doc:`getting help </askforhelp>` on setup questions in the Plone support channels (IRC, community.plone.org, mailinglists) increase when other people can reproduce your outcomes, which is most efficiently done with the Universal Installer.

Besides that, there are many people deploying Plone as part of other deployment tools, be they Ansible, Salt, Chef, Puppet or the like. If you are familiar with these, you will most likely find others in the Plone community that share your enthusiasm.

There is an :doc:`Ansible playbook </external/ansible-playbook/docs/index>`, maintained by the Plone community, that can completely provision a remote machine to run a full-stack, production-ready Plone server with all the bells and whistles.
