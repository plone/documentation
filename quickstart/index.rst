==========
Quickstart
==========

.. admonition:: Description

	A quick overview to get you up and running with Plone.


Online Demo Sites
=================

Online demo sites allow users to experience the look and feel of Plone as well as check out its ease of use and features.

These sites let users log in using a variety of roles so they can see the difference between what users, editors,
and administrators see when working in Plone.

You can find a list of available online demo sites at the `Try Plone section <https://plone.com/try-plone>`_ on `plone.com <https://plone.com>`_.

Another interesting approach to try out Plone is to install it in a cloud service.

That way, you can set up your own demo (or even very-light-weight production) Plone,
which makes it a good fit to have Plone with your choice of add-ons be tested by your department or other group.

Here are two blog posts that show you how to do this: `Plone on a free-tier Heroku <http://blog.niteoweb.com/dear-plone-welcome-to-year-2014/>`_
by Nejc Zupan and `Installing Plone 5 on Cloud9 IDE <http://blog.dbain.com/2015/09/installing-plone-5-on-cloud9-ide.html>`_ by David Bain.


Plone On Your Own Machine
=========================

You can find the download options at `plone.org/download <https://plone.org/download>`_

The recommended and best supported way to deploy Plone, both for laptops as well as servers, is the Unified Installer.
It can provide you both with a single instance with developer tools installed, as well as with multiple failover clients running against a database server.

What this means it that it will scale from quick evaluation to development to deployment, which will make your experience easier.

The catch is that the Unified Installer works on Linux and Unix-like systems (including macOS and other BSD's), not Windows.

For Windows, there is a currently no binary installer for Plone 5 available, though we anticipate to have one in the future.

In all honesty it must be said that this is not the ideal way to work with Plone if you want to *develop* with it.

A large portion of the toolchain is not readily available on Windows environments.

There is a highly workable alternative: Using **virtual machines**.

The latest release of Plone also comes as a VirtualBox / Vagrant image.

This will install a fully-working Plone for you in a virtual machine,
but integrated with the host so that all your favorite Windows editing and development tools work.

If you want to develop with Plone on a Windows machine, that would be your easiest option.

For macOS users we also advise to use virtual machines for casual testing, and the installation of the Universal.

The Unified Installer works just fine under macOS.

You can find all information on using these different options at the :doc:`Installation </manage/installing/index>` chapter in the "Managing,
Administration" section of these docs.

Or, head straight to `plone.org/download <https://plone.org/download>`_ to get started now!



Deployment
==========

Any deployment of Plone as a real-world site will usually entail setting up some more software.
In almost all cases, you will want to have a webserver like Nginx or Apache in front, and a cache like Varnish to optimize response times.

Depending on your needs, you might also want redundant, high-availability options like ha-proxy,
and monitoring tools to keep an eye on things and notify you when trouble arises.

A good selection of these tools is described  in the :doc:`Guide to deploying and installing Plone in production </manage/deploying/index>`.


Alternative Ways To Deploy
--------------------------

The Unified Installer itself is based on `buildout <http://www.buildout.org>`_.

If you're working with Plone a lot, it is a good idea to get familiar with this tool and the relation with other Python module management tools.

Buildout can be used in a variety of ways, and many people use it to tweak their own development-instances and/or deployment instances.
See `starzel.buildout <https://github.com/starzel/buildout>`_ for a rather maximized example.

Note however, that your chances of :doc:`getting help </askforhelp>` on setup questions in the Plone support channels
(IRC, community.plone.org, mailinglists) increase when other people can reproduce your outcomes, which is most efficiently done with the Unified Installer.

Besides that, there are many people deploying Plone as part of other deployment tools, be they Ansible, Salt, Chef, Puppet or the like.

If you are familiar with these, you will most likely find others in the Plone community that share your enthusiasm.

There is an :doc:`Ansible playbook </external/ansible-playbook/docs/index>`, maintained by the Plone community,
that can completely provision a remote machine to run a full-stack, production-ready Plone server with all the bells and whistles.
