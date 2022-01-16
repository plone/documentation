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


Possible setup for first chapters
---------------------------------

This is only a suggestion/inspiration based on discussions with
Volto frontender on what they first have to create (task oriented)
or modify on the backend when they work on Volto sites. These
could map to chapters

----

* scaffold  plone server setup/buildout with add-on directory

* scaffold a content type

(use plonecli in below example for scaffolding, then explain directory structure/files? ) 

* contenttype: create xml schema or jkcreate the interface  zope.schema for the fields

* Create the  Item/Container python class

* register the content type in the types xml

* generic setup upgrade step

* upgrade step definition in ZCML to register the generic upgrade step

