Through the Web or on the File System?
======================================

How to decide whether to build your theme through the web or on the file
system.

Sooner or later with Plone you'll be faced with a decision. Plone is
sufficiently flexible that there is often more that one way of doing
things, and the conundrum is, usually, not *how* to do it, but *which
way*.

You can customize Plone Default through the web very easily -
particularly the skin and the configuration building blocks; further
sections of this manual will point you in the direction of the relevant
places in the Zope Management Interface to do this. However, if you want
to move these customizations to a new site, undertake quite extensive
customizations, or build a completely new theme, then it is advisable to
move your work to the file system.

In this case you will need to create an installable module (also known
as a theme product or  egg). This can be a daunting prospect, but there
are tools available to simplify this process, providing you with a
ready-made package into which to drop all the elements of your theme
building blocks. We explain these tools on the next few pages.

If you are just starting out, then it is a good idea to get familiar
with the building blocks and techniques by working through the web. It
isn't difficult to move what you've done to the file system later. Once
you start rewiring or moving components around you'll find the file
system a more convenient way to work.

Through the Web
---------------

+-------------------------------+---------------------------------------------------------------------------------------------------------+
| Pros                          | Cons                                                                                                    |
+===============================+=========================================================================================================+
| Quick and easy                | Difficult to replicate or move from one site to another                                                 |
+-------------------------------+---------------------------------------------------------------------------------------------------------+
| Results immediately visible   | Large customizations can get complicated                                                                |
+-------------------------------+---------------------------------------------------------------------------------------------------------+
|                               | Some customizations of components aren't possible (e.g. can't move viewlets between viewlet managers)   |
+-------------------------------+---------------------------------------------------------------------------------------------------------+

On the File System
------------------

+------------------------------------------------------------------+---------------------------------------------------+
| Pros                                                             | Cons                                              |
+==================================================================+===================================================+
| Portable and reusable                                            | Steeper learning curve when you first start out   |
+------------------------------------------------------------------+---------------------------------------------------+
| Complete flexibility, can write your own viewlets and portlets   | Need access to the file system                    |
+------------------------------------------------------------------+---------------------------------------------------+
| Bundles your changes up into your own theme / skin               | Will sometimes need to restart to see changes     |
+------------------------------------------------------------------+---------------------------------------------------+

