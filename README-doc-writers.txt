 Training vs Reference
---------------------

The Mastering Plone training contains a lot of explanation and is
a 'story telling' version of the reference documentation we have here.
It has been well maintained and also has been updated to have chapters
on the new React Frontend. Because of the purpose (training) It might
however not have the right order for the happy path and much more 
verbose than the level we want to achieve here.  But please take a look
at the explanation there if you work on documentation a task here.



Scaffolding
-----------

There has been some discussing about bootstrapping during the 2021
PloneConf at the fanzone. The reference documentation should contain
the first steps to generate a working Zope/Plone app server
configuration that requires scaffolding.  The current scaffolding tool
that has been well supported updated and used in the community is
plonecli. This tool internally depends on bobtemplates, but we 
shouldn't mention that (implementation detail).

To avoid having a too strict dependency on plonecli but also not
having to write out/document every single file I propose we use/
describe plonecli, but after running discuss/document the files 
created and why they are there. 

Happy doc writing!

Fred van Dijk
Nov 1st 2021

