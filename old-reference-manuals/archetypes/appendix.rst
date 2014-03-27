====================
Appendix: Practicals
====================

.. admonition:: Description

    Plone Developer Manual is a comprehensive guide to Plone programming.

1. How-To Extend A Basic Archetype Content Type
===============================================

This How-To describes what to do next after you've gotten the basic
Archetype examples working. You can add functions, views, actions,
and edit-page validation.

Ok, so you've got the Archetype examples to work, and now you'd
like to know how to flesh out the basic example into something
useful. (That's how I started; I knew I needed to make new Content
Types, but didn't know how they worked. I got the examples going,
then tried to figure out how to modify them to do what I wanted.) I
found learning Plone/Zope very frustrating until I got to this
point. Then, once I figured out how to make Content Types do what I
wanted, it all made sense.

**Adding Functions**
This is probably one of the first things on your mind. Where do I
add functions to my Content Type? How do I call them? What syntax
do I use? Well, these were the things that I wondered about. I
figured out how to do them after some trial and error. I never made
a real website before, where I had to write scripts (a blog doesn't
count). So even though I had a lot of python experience, I was
confused at first.
[*First, know that the Zope server converts a URL path into an object path, to find the object that will render your page. This is covered in the Zope Developer's guide. The key point you need to know is that there's a parallel between the URL and your object hierarchy, but it's not exactly the same*.]

To cut to the chase, Zope figures out which object/function the URL
is pointing to, and it takes the query string (?arg=val,arg2=val2,
etc.) and uses it to figure out all the right arguments for the
function call. So, you define your function in the ususal way,
i.e.,

::

    class MyExample (BaseContent):
      """ My example Archetype Content Type. """
    
      # define the schema
      # override the default actions
    
      def my_function (self, foo1, foo2):
        """ You need a doc string here!! I lost a lot of time finding this out.
            Archetypes needs this when registering the function in the framework.
            You'll get a 404 error if you forget the doc string. """
        temp1 = "foo"  # this is not persisted in the ZODB
        self.this_is_a_persisted_member_in_the_ZODB = "I'm here to stay %s" % (foo1,)
        # if you don't return anything, then the Zope server will not re-render a page
        # anything you return will be rendered
        # return "got here" will show up as text
        # return context.index_html() will return the default page (should be reasonable in any content; people won't get lost)
        # return context.base_edit() has the effect of "jumping" to the edit page

**Adding Actions**
I was confused when I saw the description of *actions* in the Plone
manual. Here's how I think of them: they're just the hyper-linked
tabs along the top of the Content Type (content actions) or
horizontal site navagation (site actions). The links are typically
to a Content Type function (that returns a page), or to a page
template (I only know how to make .pt and .cpt types so far). The
actions for the Content Type are defined (overriden) using the
Factory Type Information format, and the process well described in
the Archetype tutorials. I'll just add that you can make most of
the tabs (actions) visible=True or visible=False. You can append
your own actions that show up as tabs for your content type.

**Changing Page Views**
You can change the various views of your content type by defining
new page templates to display your data. Typically, these page
templates (.pt) are placed within the skins/ directory of your
product. I can't fill you in on exactly how Zope maps the URL
(http://.../myArchExample/my\_view) to the my\_view.pt, but the
details are taken care of (by the Install.py script?) and you
should put your page templates in the skins/ directory.
*[This section needs updating, as soon as I learn how it's done.]*

**Validating the Edit Form**
You probably have a need to validate the data that users enter on
the edit page. This process is called *validation*, and the scripts
that implement the rules are called *validators*. There's a clean
way to do this in Archetypes using built-in field validators and
your own post\_validation() function for the Content Type. You
don't have to write any (.cpt,.cpy,.vpy) form templates, or
controller scripts. Of course, validation is optional, so you can
skip either step.


#. Use field validators on individual entries (see the validator =
   (,) field attribute). This is the first-line of validation.
#. Define a post\_validation() function. This allows you to
   validate fields in the context of the entire class, and set error
   (re-do) flags for individual fields.

After the user hits the 'submit' button on the edit page, the field
validators are run first. If any validators fail, the input field
is highlighted, and the user is sent back to the edit page to fix
the errors.

If all the field validators pass, then your post\_validate(self,
REQUEST, errors) is called. The form keys and data are passed to
you in the REQUEST dictionary. Your code will validate the edit
form values in the REQUEST dictionary. If you see errors that
require fixing, you'll set them in the errors dictionary (using the
corresponding key in the REQUEST). For example, here's a

::

    class MyExample (BaseContent):
      """ My example Archetype Content Type. """
    
      # define the schema
      # override the default actions
    
      def post_validate (self, REQUEST, errors):
        """ This function checks the edit form values in context.
            It's called after the field validation passes.  """
        if REQUEST['type'] == 'buy' and REQUEST['quantity'] == 0:
          error['quantity'] = "Quantity must be non-zero."

**Adding Child Members**
If your content type is a folder-like object, you can write
functions that will add child objects. This may be useful, for
example, if your Content Type is a ledger, and you need to add new
transactions when the user hits an action. The following example
code shows how to do this.

::

    class MyExample (BaseFolder):
      """ My example Archetype Content Type. """
    
      # define the schema
      # override the default actions
    
      def addTransaction (self, type, quantity):
        """ This function creates a new MyTransaction object in the folder. """
        # create a unique id for this transaction
        newId = self.generateUniqueId('MyTransaction')
        # create a new MyTransaction object
        self.invokeFactory(id=newId, type_name='MyTransaction')
        myTransaction = getattr(self, newId)
        return myTransaction.base_edit()     # send the user to the edit page

2. Implement Archetypes ComputedField and ComputedWidget on your Product and reference other Fields
===================================================================================================

A simple use of ComputedField and ComputedWidget referencing other
fields, built-in or 3rd party, in the same Plone product

Motivation
----------

There are many reasons why this how-to exists:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


-  Almost no Archetypes examples using ComputedField and
   ComputedWidget
-  We want our product to process some data on itself, but reload
   isn't a matter of concern
-  We love PZP (Python-Zope-Plone)!

What do we need?
~~~~~~~~~~~~~~~~


-  A Plone installation
-  A nice text editor (my wintel box runs SciTE)
-  Some product (for real dummies like me, try
   http://plone.org/documentation/tutorial/anonymously-adding-custom-content-types-with-argouml-and-archgenxml/view)

**What we are going to achieve?**


-  Make a page process it's own information

Let's say you created a product, maybe using ArgoUML (an UML
editor) and ArchGenXML. One thing you might realize it's missing on
creating UML's is that: we create classes (Plone products), their
types are also classes (Archetypes' fields and widgets) and
Attributes (Fields and Widgets' properties) as TD's (tagged data)
for Archetypes' types, but we have no *methods*!
But we could do more if we inserted code: classes are made of
attributes and methods (code). But as UML editors are not that
Python friendly, we do that by hand.

So, how?
~~~~~~~~

If you already have navigated the path of a product, you've
stumbled on some source files (.py) inside, so take some time to
read their source (*Read the source, Luke!*). Probably you've seen
some like this (for example, MyOrder.py):

::

    from AccessControl import ClassSecurityInfo
    from Products.Archetypes.atapi import *
    from Products.Laborde.config import *
    
    from Products.DataGridField import DataGridField, DataGridWidget # we talk about this later
    from Products.DataGridField.Column import Column #really!
    
    schema = Schema((
        StringField(
            name='PurchaseOrderID',
            widget=StringWidget(
                label="PurchaseOrderID",
                description="Enter this purchase order unique identification number.",
                label_msgid='MyOrder_label_PurchaseOrderID',
                description_msgid='MyOrder_help_PurchaseOrderID',
                i18n_domain='MyOrder',
            ),
            required=True,
            searchable= True
        ),
        DataGridField(
            name='PurchaseOrderItems',
            required=True,
            searchable=True,
            widget=DataGridWidget(),
            allow_empty_rows = False,
            columns=(
                "Maker",
                "Model",
                "Description",
                "UnitaryCost",
                "Quantity"
            ),
        ),
    
        ComputedField(
            name='TotalCost',
            searchable=True,
            expression="context.calculateTotal()",
            widget=ComputedWidget(
                label="Total",
                modes=('view')
            ),
        ),
    
    ),
    )
    
    PurchaseOrder_schema = BaseSchema.copy() + \
        schema.copy()
    
    class PurchaseOrder(BaseContent):
        """
        """
    
        # some class defitnitions
    
        # a function that calculates total
        # but it doesn't even check (try-except) data it uses
    
        def calculateTotal(self):
            Total = 0.0
            for n in self.PurchaseOrderItems:
                Quantity = float(n['Quantity'])
                UnitaryCost = float(n['UnitaryCost'])
                Total = Total + Quantity * UnitaryCost
            Total = '%1.2f' % Total # this makes our total have 2 decimals for display
            return Total
    
    registerType(PurchaseOrder, PROJECTNAME)

 

Aargh! I've just core dumped and almost killed 30!
The above code can be divided in two parts: Schema and Class
(Product). We have declared 3 different fields in the schema: the
first is a bultin trivial Archetype field; the second is imported
from the Product DataGridField (you need it installled on your
Plone instance to work); the third is our the field we want to
change as someone changes values on the form.

::

    expression="dir()" # useful to check avaible objects

,

::

    expression="1+1" # 10 if you have two neurons, like me. Otherwise, 2.

,

::

    expression="dir(context)" # avaible context child objects

or

::

    expression="context.calculateTotal()" # VoilÃ¡! Reference to some real(?) code!

We've just called something (a function, in fact) named
*calculateTotal*.
But smart as we are, we realized that expresssions called this way
must be somewhere in our context scope. I mean, inside our class
definition.
The function definition itself isn't that simple: it adds up the
total and returns its value. What isn't simple? Our generous
DataGridField returns a tuple of dictionaries like:

::

    (
        {"Maker":"HP","Model":"scanjet 4670","Description":"scanner","UnitaryCost":"99.00","Quantity":"1"},
        {"Maker":"LG","Model":"L173SA","Description":"17 LCD monitor","UnitaryCost":"299.95","Quantity":"2"},
        {"Maker":"Seagate","Model":"SA32300","Description":"Hard drive","UnitaryCost":"134.50","Quantity":"2"}
    )

 

The *for* loop iterates over every item on the tuple and searches
for two dictionary items. Other field are rather simple to retrieve
data: just use field's name attribute.
The *widget=SomeWidget(modes='view',...)* realizes the feat of
showing this field only on the view mode: not when adding the item
and editting, nor when editting an existing item.

What's next?
~~~~~~~~~~~~


-  What could we do with PhotoField (ImageWidget)?
-  try-except is always recomended
-  Could this better than *mutate* ?
-  Can we make a file avaible for download with some strange mime
   type based on the information of this product?

3. Making the view page of a content type use your schemata declarations
========================================================================

How to make the schemata declarations in a Archetypes schema be
used in the view page of a content type.

Introduction
============

Declaring schematas in your Archetype schema has the nice effect of
displaying the fields of the different schemas on different edit
pages (very much like a "wizard" for adding a new content type
instance). Often times you might like to also have the view page be
divided according to the different schemas you have declared. This
is not done automatically by Archetypes so in this document I'll
show you how to do it yourself. Don't worry! It's really quite
easy.

Python class and schema
=======================

I'll be using a simple article content type I have constructed for
this how-to to show you how the schematas can be used on your
content type's view page. The example type is really not very
usable, but just complex enough to show you how to do this. It has
a schema of four fields in addition to the default id and title
fields: abstract, body, firstname, lastname. The abstract and body
fields are in a schemata named article and the firstname and
lastname field in a schemata named author.

I have also defined the title and id fields to be in schemata
article. This was done so I won't have an extra schemata called
default and so I can use the title field for the title of the
article. (Remember to use ``BaseSchema.copy()``!)

The class itself has just the schema declaration and a new view
action definition. I have defined the view action to use a template
called article\_view that we'll be getting to shortly.

Here is the file in it's entirety:

 

::

    from Products.Archetypes.public import *
    
    from Products.CMFCore import CMFCorePermissions
    
    
    
    from config import PKG_NAME
    
    
    
    schema = BaseSchema.copy() + Schema((
    
            TextField('abstract',
    
                    required=1,
    
                    searchable=1,
    
                    widget = TextAreaWidget(description="Abstract", label="Abstract"),
    
                    schemata = 'article'),
    
            TextField('body',
    
                    required=1,
    
                    searchable=1,
    
                    widget = TextAreaWidget(description="Body", label="Body"),
    
                    schemata = 'article'),
    
            TextField('firstname',
    
                    required=1,
    
                    searchable=1,
    
                    widget = StringWidget(description="First name", label="First name"),
    
                    schemata = 'author'),
    
            TextField('lastname',
    
                    required=1,
    
                    searchable=1,
    
                    widget = StringWidget(description="Last name", label="Last name"),
    
                    schemata = 'author'),
    
            ))
    
    
    
    schema['title'].schemata = 'article'
    
    schema['id'].schemata = 'article'
    
    
    
    class Article(BaseContent):
    
            schema = schema
    
    
    
            actions = (
    
                            {'id': 'view',
    
                            'name': 'View',
    
                            'action': 'string:${object_url}/article_view',
    
                            'permissions': (CMFCorePermissions.View,)
    
                            },
    
            )
    
    
    
    registerType(Article, PKG_NAME)

View template
=============

The view template article\_view is the main part of this how-to. It
has the page template code to generate the different pages for the
different schematas.

First you should copy the base.pt file from the Archetypes skins
folder (on my Debian GNU/Linux unstable it's in
/usr/share/zope/Products/Archetypes:1.3/skins/archetypes) to your
product's skins folder. It has most of the template code you'll
need ready, so you'll only need to make some minor changes to make
this work. Also it uses all the default macros and such, so you'll
view page will look like a real plone page.

The base.pt template just goes through all the fields of your
content type and shows their widgets. What we want to do is to have
it only go through the fields of one schemata at a time and give us
links to see the others. This will be done using REQUEST parameters
to the scripts.

I'll go though the changes from the top of the file downwards so
you'll have a easier time keeping up and making the changes to your
own template.

Links to the different schematas
--------------------------------

We'll want the list of different schematas to be at the top of the
page, so that'll go in first. Find the line that says
'``<metal:main_macro define-macro="main">``'. This is where the
body of the template starts. After this line is the header with the
title and the little icons for edit, print and such, and I want to
have my links to show up above that. So after the beginning of the
body and above the header add the following code:

 

::

            <div style="margin-bottom: 1em">
    
                    <span tal:repeat="schemata python: here.Schemata().keys()">
    
                            <b tal:condition="python: schemata != 'metadata'">[<a tal:attributes="href string:?page=${schemata}"><span tal:replace="schemata" /></a>]</b>
    
                    </span>
    
            </div>

This just repeats over our schematas' names (we get them with
``here.Schemata().keys()``) and prints all of them on one line as
links, each one in square brackets. The links are to the same view
page, but they all set a parameter in REQUEST called page that
points to the schemata we are linking to. This isn't very pretty so
you'll probably want to make them look nicer if you like. The
'``schemata != 'metadata'``' part is because there's a schemata
called metadata created automatically for your content type to
support default standard metadata which can be set via the
properties tab and that we do not want to include here.

Showing only the schemata we want
---------------------------------

In the next part we'll be diving deeper into the code. You're
looking for a part that says
'``tal:repeat="field python:here.Schema().filterFields(isMetadata=0)"``'.
This repeats through the fields of your content type and the
following parts show their widgets. What we want to do here is to
have it repeat through the fields of the schemata we want instead
of all of them. In the previous part we set a parameter in REQUEST
called page that points to the schemata we want to see, and here we
want to use that to pick which schemata's fields to loop over. So
just go ahead and replace the part with
'``tal:repeat="field python:here.Schemata()[here.REQUEST.get('page', here.Schemata().keys()[0])].filterFields(isMetadata=0)"``'.
This just gets the page parameter from REQUEST (if page is not
found, ie. the template is called with no parameters, then first
schemata, in this case article, is used) and loops through the
fields of the schemata with that name.

The completed article\_view.pt looks like this:

 

::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
    
          lang="en"
    
          xmlns:tal="http://xml.zope.org/namespaces/tal"
    
          xmlns:metal="http://xml.zope.org/namespaces/metal"
    
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    
          metal:use-macro="here/main_template/macros/master">
    
    
    
      <head><title></title></head>
    
    
    
      <body>
    
    
    
        <div metal:fill-slot="main">
    
    
    
          <metal:main_macro define-macro="main">
    
    
    
            <div style="margin-bottom: 1em">
    
                    <span tal:repeat="schemata python: here.Schemata().keys()">
    
                            <b tal:condition="python: schemata != 'metadata'">[<a tal:attributes="href string:?page=${schemata}"><span tal:replace="schemata" /></a>]</b>
    
                    </span>
    
            </div>
    
    
    
            <metal:header_macro define-macro="header">
    
              <div metal:use-macro="here/document_actions/macros/document_actions">
    
                Document actions (print, rss, etc)
    
              </div>
    
              <h1 tal:content="title_string | here/title_or_id" />
    
              <tal:has_document_byline tal:condition="exists:here/document_byline">
    
                <div metal:use-macro="here/document_byline/macros/byline">
    
                  Get the byline - contains details about author and modification date.
    
                </div>
    
              </tal:has_document_byline>
    
            </metal:header_macro>
    
    
    
            <metal:body_macro metal:define-macro="body"
    
                              tal:define="field_macro field_macro | here/widgets/field/macros/view;"
    
                              tal:repeat="field  python:here.Schemata()[here.REQUEST.get('page', here.Schemata().keys()[0])].filterFields(isMetadata=0)">
    
              <tal:if_visible define="mode string:view;
    
                                      visState python:field.widget.isVisible(here, mode);
    
                                      visCondition python:field.widget.testCondition(here, portal, template);"
    
                              condition="python:visState == 'visible' and visCondition">
    
                <metal:use_field use-macro="field_macro" />
    
              </tal:if_visible>
    
            </metal:body_macro>
    
    
    
            <metal:folderlisting_macro metal:define-macro="folderlisting"
    
                                       tal:define="fl_macro here/folder_listing/macros/listing | nothing;
    
                                                   folderish here/isPrincipiaFolderish | nothing;">
    
                <tal:if_folderlisting condition="python:folderish and fl_macro">
    
                    <metal:use_macro use-macro="fl_macro" />
    
                </tal:if_folderlisting>
    
            </metal:folderlisting_macro>
    
    
    
            <metal:footer_macro define-macro="footer">
    
            </metal:footer_macro>
    
    
    
          </metal:main_macro>
    
    
    
        </div>
    
    
    
      </body>
    
    
    
    </html>

Conclusion
==========

So that was it. I told you it was going to be easy!

Happy hacking!

4. Enabling versioning on your custom content-types
===================================================

Plone 3 includes a robust versioning system as well as a tool for
viewing diffs, which allows you to easily see the changes between
two revisions. This document explains how to integrate versioning
and diff functionality with your custom Archetypes-based
content-types.

Prerequisites
-------------

You'll need a Plone 3 instance and a custom product which contains
at least one Archetypes-based content-type on which you want to
enable versioning.  

You'll also need to have the **Working Copy Support (Iterate)**
product installed.  This product is part of the Plone core so to
install it, all you need to do it visit
the **Add-on Products** section (a.k.a. Quickinstaller) of the
**Plone control panel** and select it for installation.

Creating a setup handler script for GenericSetup
------------------------------------------------

The integration code we'll be writing here is best run as a setup
handler using GenericSetup. If your product doesn't already have a
GenericSetup profile and a custom setup handler,
`this tutorial <https://plone.org/tutorial/borg/setup-using-genericsetup>`_
provides instructions on how to create those.

Declaring versionable types in your setup handler
-------------------------------------------------

The portal\_repository tool stores a list of content-types on which
version is enabled.  With the following code we create a list of
the custom types on we which we want to activate versioning and
then notify the repository tool to start versioning the types in
this list.

If you copy the code below, make sure to edit the
TYPES\_TO\_VERSION setting so that it contains a list of the types
on which you want to activate versioning.

::

    from Products.CMFCore.utils import getToolByName
    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
    
    # put your custom types in this list
    TYPES_TO_VERSION = ('Scientist', 'Article', 'Presentation')
    
    def setVersionedTypes(portal):
        portal_repository = getToolByName(portal, 'portal_repository')
        versionable_types = list(portal_repository.getVersionableContentTypes())
        for type_id in TYPES_TO_VERSION:
            if type_id not in versionable_types:
                # use append() to make sure we don't overwrite any
                # content-types which may already be under version control
                versionable_types.append(type_id)
                # Add default versioning policies to the versioned type
                for policy_id in DEFAULT_POLICIES:
                    portal_repository.addPolicyForContentType(type_id, policy_id)
        portal_repository.setVersionableContentTypes(versionable_types)

Now we call this function from the importVarious() function in our
setup handler script.  Make sure to pass the portal object as a
parameter.



::

    def importVarious(context):
        """Miscellanous steps import handle"""
        portal = context.getSite()
        setVersionedTypes(portal)

Enabling visual diffs on your versioned types
---------------------------------------------

Now that you've enabled versioning, you'll probably want to enable
visual diffs so you can compare the changes made between different
versions of an object.

Starting in Plone 3.2 the diff tool can be configured via a
GenericSetup configuration file.  You'll want to create or edit the
**diff\_tool.xml** file in the /profiles directory of your product.
 Here's an example confirmation file that enables compound diffs on
the 3 content-types used in the example above.

::

    <?xml version="1.0"?>
    <object>
      <difftypes>
        <type portal_type="Scientist">
          <field name="any" difftype="Compound Diff for AT types"/>
        </type>
    
        <type portal_type="Article">
          <field name="any" difftype="Compound Diff for AT types"/>
        </type>
    
        <type portal_type="Presentation">
          <field name="any" difftype="Compound Diff for AT types"/>
        </type>
      </difftypes>
    </object>

For Plone versions earlier than 3.2, there is not a GenericSetup
handler for configuring the diff tool, but you can create these
settings through the ZMI using the **portal\_diff** tool.  In the
**Portal Type** drop-down menu select the content-type on which you
want to enable diffs.  In the **Field name** box type "any".  For
the **Diff Type** select "Compound Diff for AT Types".  Finally
click the **Add Field** button.  Repeat these steps for each
content-type.

Deploying your new versioning and diffs policy
----------------------------------------------

To deploy these changes you'll need to re-run you product's
GenericSetup policy.  If your instance is not running in debug
mode, you'll first need to restart your Zope instance to make your
new filesystem code available. 

Assuming you've used paster to create your product package,
reinstalling your product in the **Add-on Products** section of the
**Plone control panel** should be sufficient to re-run
your** GenericSetup policy** .  If your product's install method
does not run your GenericSetup policy, you may need to visit the
**portal\_setup** tool in the ZMI and run it manually.

Verifying that versioning and visual diffs are now enabled
----------------------------------------------------------

Visit an instance of one of the types on which you've enabled
versioning.  Make some edits to one or more of the fields save
those changes.  Next, visit the **history** tab for the item you
just edited. You should see a list showing two versions.  Click the
link to compare versions you should see a diff showing you what has
been changed between the two revisions.

5. b-org: Creating content types the Plone 2.5 way
==================================================

Plone 2.5 brings us closer to the promised land of Zope 3. Zope 3
brings us a new way of working. This tutorial will show how to
marry the old and the new, to make Plone products that are more
extensible, better tested and easier to maintain.

5.1. Introduction
=================

What is b-org, and what will you learn here?

b-org stands for "base-organisation". The name had nothing
whatsoever to do with my desire to get an svn URL of
`http://svn.plone.org/svn/collective/borg <http://svn.plone.org/svn/collective/borg>`_.
Promise. In fact, it used to be called *company* , which some people
rightly pointed out is a bit too generic and opens up the
possibility of conflicts with other people's code. It just proves
that naming generic components is difficult.

**Generic** is the key word here. Functionally, b-org provides
infrastructure to help you manage **Departments** , **Employees**
and **Projects** in a natural way. Departments are containers for
employees, employees are linked to projects by references. Using
*membrane* , these objects become sources for users and groups, so
that a department is a group for all the employees in it, and
employees become real users of the system, with usernames and
passwords. Projects manage local roles, so that employees that have
been associated with the project are able to add and modify content
in it. Other users may or may not be able to view content in a
project, depending on its workflow state.

However, b-org makes no assumptions about which metadata you want
to associate with departments, employees or projects. For that, it
expects you to plug in your own content schema. It also delegates
almost all its functionality to smaller components, so that if you,
for example, want to store authentication details via LDAP or
change the way in which users are employees to projects, you can do
so by implementing small, isolated components rather than
sub-classing and re-implementing large chunks of the three basic
content types.

That's all well and good, but you're probably not going to want to
read a lengthy tutorial just about how great b-org is. As the title
promises, this tutorial is about
**leveraging new technologies available in Plone 2.5** to write
better content types and other software in Plone. Hopefully, you
will find the techniques described here useful whether you are
writing a member management module using membrane (mmmm), or other
code. I for one, want to go and rewrite several of my products
(like Poi) to make them more extensible and flexible after having
adopted these techniques. Hopefully, you will also learn something
about the **development process** , in particular
**test-driven development** , that I followed, and how the future of
Plone is entangled in **Zope 3** .

This tutorial should be viewed as complementary to, rather than
superceding, my earlier tutorial entitled
`*RichDocument - Creating Content Types the Plone 2.1 way* <https://plone.org/documentation/manual/developer-manual/archetypes/appendix-practicals/richdocument>`_.
The techniques of RichDocument, in particular relating to extending
ATContentTypes, are still valid in Plone 2.5. What Plone 2.5 allows
us to do, however, is to achieve better separation of concerns
between content storage, business logic and view logic, due to the
added spices of Zope 3. For RichDocument, the gain wouldn't be that
great since it's relatively simple (and focuses on doing as little
as possible by re-using as much as possible from ATContentTypes).
Hence, I didn't update the RichDocument tutorial, nor do I feel as
compelled to update RichDocument itself (yet). b-org is a more
ambitious example which allows us to illustrate the new techniques
more fully.

One thing to note is that this tutorial is still centered on
**Archetypes** , and assumes you know the basics of Archetypes
development on the filesystem. Archetypes is rooted in a pre-Zope 3
world, and there are times when we have to accommodate it in ways
that make our clean patterns a bit messier - luckily, not too
often. There are ways of managing content in Zope 3 that can be
applied to Plone, for example by way of
`zope.formlib <https://plone.org/documentation/manual/developer-manual/archetypes/appendix-practicals/using-zope-formlib-with-plone>`_,
but these are generally not quite ready to replace what we can do
today with Archetypes. In the future, they may be, but more likely
Archetypes will converge a bit more with its Zope 3 equivalents and
blur the lines between the two approaches. The upshot is that what
you know about Archetypes today continues to be relevant, and is
augmented by the Zope 3-inspired techniques you will find here.

5.2. A whirlwind tour of Zope 3
===============================

Zope 3 is still fairly new. After reading this tutorial, it should
hopefully start to feel a bit more familiar. In this section, we
will give a brief overview of what is different in Zope 3 and how
it fits into Plone.

The name Zope 3 is a lie. True - it is brought to you by many of
the same clever people who built Zope 2, one of the most advanced
open source app servers of its day. True, it is still Python, it
still publishes things over the web, and there are still Zope Page
Templates. However, Zope 3 is about small, re-usable components
orchestrated into a flexible framework. It is this flexibility that
allows us to use Zope 3 technologies in Zope 2 applications like
Plone.

A piece of wizardry called *Five* (Zope 2 + Zope 3 = Five, geddit?)
makes a number of Zope 3 components directly available in Zope 2,
and since Zope 2.8, almost all of Zope 3 has shipped with Zope 2 as
a python library. Plone 2.5's primary purpose was to lay the
foundations for taking advantage of Zope 3 technologies in Plone.

Zope 3 may seem a bit alien at first, because it uses strange
concepts such as **adapters** and **utilities** . Luckily, these are
not so difficult to understand, and once you do, you will find that
they help you focus your development on smaller and more manageable
components. You will also find that these basic concepts underpin
most of the innovative parts of Zope 3.

Interfaces
-----------

Everything in Zope 3 starts with interfaces. Unlike Java or C#,
say, Python does not have a native type for an interface, so an
interface in Zope 3 is basically a class that contains only empty
methods and attributes, and inherits from *Interface* . Here is a
basic example:

::

    from zope.interface import Interface, Attribute
    
    class IShoe(Interface):
        """A shoe
        """
    
        color = Attribute("Color of the shoe")
        size = Attribute("Shoe size")
    
    class IShoeWearing(Interface):
        """An object that may wear shoes
        """
    
        def wear(left, right):
            """Wear the given pair of shoes
            """

Interfaces are primarily documentation - everything has docstrings.
Also note that the *wear()* method lacks a body (there is not even
a *pass* statement - the docstring is enough to keep the syntax
valid), and does not take a *self* parameter. That is because you
will never instantiate or use an interface directly, only use it to
specify the behaviour of an object.

An object can be associated with an interface in a few different
ways. The most common way is via its class. We say that the class
*implements* an interface, and objects of that class *provide* that
interface:

::

    from zope.interface import implements
    
    class Shoe(object):
        """A regular shoe
        """
    
        implements(IShoe)
        
        color = u''
        size = 0

The *implements(IShoe)* line means that objects of this class will
provide IShoe. Further, we fulfill the interface by setting the two
attributes (we could have implemented them as properties or used a
an \_\_init\_\_() method as well). The *IShoeWearing* interface
will be implemented in the section on adapters below.

We use interfaces to model components. Interfaces are normally the
**first stage of design** , in that you should define clear
interfaces and write actual classes to fulfill those interfaces.
This formalism makes for great documentation - interfaces are
conventionally found in an *interfaces* module, and this is
typically the first place you look after browsing a package's
documentation. It also underpins the adapter and utility system -
otherwise known as the Component Architecture - as described
below.

Note that you can use common OOP techniques in designing
interfaces. If one interface describes a component that has an
"is-a" or "has-a" relationship to another component, you can let
interfaces subclass or reference each other. An object will provide
the interfaces of its class, and all its base-classes, and all
base-interfaces of those interfaces. Don't worry about untangling
that - it works the way you would expect.

You can also apply interfaces directly to an object. Of course, if
that interface has methods and attributes, they must be provided by
the object, and unless you resort to crazy dynamic programming, the
object will get those from its class, which means that you may as
well have applied the interface to the class. However, some
interfaces don't have methods or attributes, but are used as
markers to distinguish a particular feature of an object. Such
**marker interfaces** may be used as follows:

::

    class IDamaged(Interface):
        """A shoe that is damaged
        """

::

    >>> from zope.interface import alsoProvides
    >>> boot = Shoe()
    >>> IDamaged.providedBy(boot)
    False
    >>> alsoProvides(boot, IDamaged)
    >>> IDamaged.providedBy(boot)
    True

Marker interfaces are very useful for things that change at
run-time in response to some event (e.g. some user action), and
thus cannot be determined in advance. In a moment, you see that
what you will learn about adapters and adapter factories below also
applies to marker interfaces - it is possible to alter which
adapter factory is invoked by applying a different marker
interface.

It's also possible to apply interfaces directly to classes (that is
the *class itself* provides the interface, as opposed to the more
usual case where the class implements the interface so that objects
of that class provides it - this is useful because it allows you to
group those classes together and describe the *type* of class they
are) and to modules (where you want to describe the public methods
and variables of a module). These constructs are less common, so
don't worry about them for now. Look at the documentation and
interfaces (!) in the *zope.interface* package for more.

Adapters
--------

The most important thing that Zope 3 promises is
**separation of concerns** . In Zope 2, almost everything has a base
class that pulls in a number of mix-in classes, such as
*SimpleItem* (surely, the most ironically named class in Zope 2)
and its plethora of base classes that include *RoleManager* ,
*Acquisition.Implicit* and many others. This means that a class
written for Zope 2 is nearly impossible to re-use outside of Zope.

Furthermore, in Zope 2 we are tightly wedded to the *context* (aka
*here* ) because it is so convenient to use in page templates,
workflow scripts etc. For example, people often write an Archetypes
class that contains a schema (storage logic), methods for providing
various operations (business logic) and methods for preparing
things to display in a page template (view logic). Often, people do
this simply because they can't think of a better place to put
things, but it does mean that re-using any part of the
functionality becomes impossible without importing the whole class
- and its base classes, which include Archetypes' BaseObject, CMF's
DynamicType, and Zope's SimpleItem - to name a few!

Think about the example above. The *Shoe* class is well-contained
and only concerned with one thing - storing the attributes of
shoes. It can be used as an abstraction of shoe anywhere, and is
very lightweight. Now let's consider that we may want to wear shoes
as well. We can create a pair of shoes easily enough:

::

    >>> left = Shoe()
    >>> right = Shoe()
    >>> left.size = right.size = 10
    >>> left.color = right.color = u"brown"

Now we want someone to wear these shoes. Let's say we have a
person:

::

    class IPerson(Interface):
        """A person
        """
    
        name = Attribute("The person's name")
        apparel = Attribute("A list of things this person is wearing")
    
    class Person(object):
    
        implements(IPerson)
    
        name = u''
        apparel = ()

In a Zope 2 world, we may have required Person to mix in some
*ShoeWearingMixin* class that specified exactly how shoes should be
worn. That makes for fat interfaces that are difficult to
understand. In a Zope 3 world, we would more likely use an
adapter.

An adapter is a glue component that can adapt an object providing
one interface (or a particular combination of interfaces, in the
case of a multi-adapter) to another interface. We already have a
specification for something that wears shoes, in the form of
*IShoeWearing* . Here is a snippet of code that may use this
interface:

::

    >>> wearing = ...
    >>> wearing.wear(left, right)

The question is what to do with the '...' - how do we obtain an
object that provides IShoeWearing? Code like this is normally
operating on some context, which in this case may be a *Person* . If
that Person implemented IShoeWearing (or at least the
*wear()*method), it would work, but then we are making undue
demands on Person. What we need is a way to *adapt* this IPerson to
something that is IShoeWearing. To do that, we need to write an
adapter:

::

    from zope.interface import implements
    from zope.component import adapts
    
    class PersonWearingShoes(object):
        """Adapter allowing a person to wear shoes
        """
        implements(IShoeWearing)
        adapts(IPerson)
    
        def __init__(self, context):
            self.context = context
    
        def wear(self, left, right):
            self.context.apparel += (left, right)

Here, we implement the IShoeWearing interface. Note how the
*wear()* method now has a *self* parameter, since this is a real
object. Also note the *\_\_init\_\_()* method, which takes a
parameter conventionally called *context* . This is
*the thing that is being adapted*, in this case an object providing
IPerson. We store this as an instance variable and then reference
it later. Note that adapters are almost always transient objects
that are created on the fly (we will see how in a second).

We could now do something like this:

::

    >>> wearing = PersonWearingShoes(person)
    >>> wearing.wear(left, right)

However, this still requires that we know exactly which adapter to
invoke for the particular object (*person* in this case),
effectively creating a tight coupling between the adapter, the
thing being adapted, and the code using the adapter.

Luckily, the Zope 3 Component Architecture knows how to find the
right adapter if you only tell it about the available adapters. We
do that using **ZCML** , the Zope Configuration Markup Language.
This is an XML dialect that is used to configure many aspects of
Zope 3 code, such as permissions and component registration. You
can do what ZCML does in Python code as well, but typically it's
more convenient to use ZCML because it allows you to separate your
logic from your configuration.

ZCML directives are stored in file called *configure.zcml*, which
itself may include other files. A *configure.zcml* file in your
product directory (Products/myproduct/configure.zcml) will be
picked up automatically by Five. Here is a snippet that will
register the above adapter:

::

    <adapter factory=".shoes.PersonWearingShoes" />

You will sometimes see a fuller form of this directive, like:

::

    <adapter
        factory=".shoes.PersonWearingShoes"
        for=".interfaces.IPerson"
        provides=".interfaces.IShoeWearing"
        />

Here, we are specifying full dotted names to interfaces in the
*for* or *provides* attributes. These are equivalent to the
*adapts()* and *implements()* calls we used when defining the
adapter. Note that *adapts()* did not work prior to Zope 2.9 (so
the ZCML *for* attribute is mandatory), and that if your adapter
class for some reason implements more than one interface (e.g.
because it's inheriting another adapter that has its own
*implements()* call), you may need to specify *provides* to let
Zope 3 know which interface you're really adapting to.

Notice here that the dotted names begin with dot. This means
"relative to the current package". You can write *"..foo.bar"* to
reference the parent package as well. You could specify an absolute
path instead, e.g. *Products.Archetypes.interfaces.IBaseObject*or
*zope.app.annotation.interfaces.IAttributeAnnotatable*. Typically,
you use the full dotted name for things in other packages and the
relative name for things in your own package.

The *factory* attribute normally references a class. In Python, a
class is just a callable (taking the parameters specified in its
*\_\_init\_\_()*method) that returns an instance of itself. You can
reference another callable as well if you need to, such as a
function that takes the same parameters (only *context* in this
case - obviously there is no *self* for functions), finds or
constructs and object (which must provide *IShoeWearing* ) and then
returns it. This is rarely used, but can be very powerful (for
example, it could find an object providing the given interface in
the adapted object's annotations - but don't worry if you don't
understand that for now).

With this wiring in place, we can now find an adapter for an
IPerson to IShoeWearing. The Component Architecture will ensure
that we find the correct adapter:

::

    >>> wearing = IShoeWearing(person)
    >>> wearing.wear(left, right)
    >>> person.apparel == (left, right,)
    True

We are "calling" the interface, which is a convenience syntax for
an adapter lookup. If an adapter cold not be found, you will get
a *ComponentLookupError* . There are plenty of functions in
*zope.component* to discover adapters and other components - see
*zope.component.interfaces* for the full story.

It is important to realise that the adapter lookup is essentially a
search. The Component Architecture will look at the interfaces
provided by *person* and look for a suitable adapter to
IShoeWearing. As mentioned before, it's possible for an object to
provide many interfaces, e.g. inherited from its base classes,
implemented explicitly by the object (by declaring
*implements(IFoo, IBar)*), via ZCML or because an object directly
provides an interface. It is therefore possible that there are
multiple adapters that could be applicable. In this case, Zope 3
will use the *interface resolution order* (IRO) to find
the**most specific** adapter. The IRO is much like you would expect
of polymorphism in traditional OOP:


-  an interface directly provided by the object is more specific
   than one provided by its class
-  an object provided by an object's class is more specific than
   that provided by a base class
-  if an object has multiple base classes, interfaces are inherited
   in the same order as methods are inherited
-  if a class implements multiple interfaces, the first one
   specified is more specific than the second one, and so on

Remember marker interfaces? One use of marker interfaces is to
imply a particular adapter. Think about the case where you may
have  specific adapter to IShoeWearing for some marker interface
IAmputee. If you mark a person as an IAmputee due to some
unforunate accident, the IShoeWearing adapter may raise a warning
rather than modify the apparel list.

All of this may seem a little roundabout and unfamiliar, but you'll
get to grips with it soon enough. Let's re-cap how we arrived at
this:


#. We modelled our application domain with some interfaces -
   IPerson, IShoe
#. We modelled an aspect of a person (or other object) for wearing
   shoes - IShoeWearing
#. We wrote some simple classes that implemented the domain
   interfaces IPerson and IShoe
#. We wrote and registered a simple adapter that could adapt an
   IPerson to IShoeWearing

Then we showed how this could be used by some hypothetical client
code. The upshot is that the client code only needed to know about
IPerson and IShoeWearing, not how the aspect of a person that
involves wearing shoes is implemented. The Component Architecture
will ensure that the appropriate adapter is found, regardless of
whether the person is a vanilla IPerson, a sub-class with a more
specific sub-interface, or an instance with a marker interface
applied.

 

Multi-adapters, named adapters and views
-----------------------------------------

In the example above, we used an adapter with a single context.
That is the most common form of adapter, but sometimes there is
more than one object that forms the context of an adapter. As a
rule of thumb, if you find yourself passing a particular parameter
into every method of an adapter, it should probably be a
multi-adapter.

The most common example of a multi-adapter that you will come
across is that of a *view*, which incidentally is also how Zope 3
solves the "where do I put my view logic" code. We will cover views
in detail later, but for now think of them as a python class that
is automatically instantiated and bound to a page template when
it's rendered. In the template, the variable *view* refers to the
view instance and can be used in TAL expressions to gain things to
render or loop on.

When dealing with a view, there are two things that make up its
context - the context content object (conventionally called
*context* ) and the current request (conventionally called
*request* ). Thus, a view class is a multi-adapter from the tuple
*(context, request)* to IBrowserView. As it happens, there are ZCML
directives called *browser:page*and *browser:view* that make it
easier to register a view and bind a page template to it, handle
security etc. However, abstractly a view looks like this:

::

    class PersonView(object):
        implements(IBrowserView)
        adapts(IPerson, IHttpRequest)
    
        def __init__(self, context, request):
            self.context = context
            self.request = request
    
        def name(self):
            return self.context.name
    
        def requested_shoes(self):
            return self.request.get('requested_shoes', [])

Notice how this adapts both IPerson and IHttpRequest, and thus
takes two parameters in its *\_\_init\_\_()*method. As you will
learn later, views typically inherit the *BrowserView* base class
for convenience, but the principle is the same.

To obtain a multi-adapter, you can't use the "calling an interface"
syntax that you use for a regular adapter. Instead, you must use
the *getMultiAdapter()* method:

::

    >>> from zope.component import getMultiAdapter
        ...
    >>> personView = getMultiAdapter((person, request,), IBrowserView)

You could use *queryMultiAdapter()* instead if you wanted it to
return None instead of raise a ComponentLookupError when it fails
to find the adapter.

The above code has a problem, however (apart from being an
incomplete example) - what if you have more than one view on the
same object, say for two different tabs? To resolve this ambiguity,
views are actually *named multi-adapters*. The names correspond to
the names used as part a URL, and are registered using the *name*
attribute in ZCML. This is used in *browser:page* and
*browser:view* directives, but can also be used in the standard
*adapter* directive:

::

    <adapter factory=".sampleviews.PersonView" name="index.html" />

To get this particular view, we can write:

::

    >>> personView = getMultiAdapter((person, request,), name=u'index.html')

conventionally, we leave off the required interface when we used
named adapters, although you can supply it if necessary.

Multi-adapters are useful for other things as well. If you have an
adapter and find that every method takes at a common parameter,
it's a good candidate for a multi-adapter. Also observe that in the
case above, we could register a different adapter for a different
type of request as well as for a different type of object. Again,
the Component Arhictecture will find the most specific one looking
at both interfaces.

Named adapters do not have to be multi-adapters, of course. They
are typically used in cases where something (e.g. the user) is
making a selection from a set of possible choices (such as choosing
the particular view among many possible views).

Utilities
-----------

In the CMF, we have *tools*, which are essentially singletons. They
contain various methods and attributes and may be found using the
ubiquitous *getToolByName()* function. The main problem with tools
is that they live in content space, as objects in the ZODB, and
require a lot of Zope 2 specific things.

Let's say we had a shoe locating service (very useful when you
can't find your shoes):

::

    class IShoeLocator(Interface):
        """A service for finding your shoes
        """
    
        def findShoes(owner):
            """Find all shoes for the given owner.
            """
    
    class DefaultShoeLocator(object):
        implements(IShoeLocator)
        
        def findShoes(self, owner):
            return ... 

The Component Architecture contains a very flexible
*utility registry*, which lets you look up things by interface and
possibly by name. Unlike adapters, utilities do not have context,
and they are instantiated only once, when Zope starts up. Global
utilities are not persistent (but local utilities are - see
below).

As with adapters, we register utilities with ZCML:

::

    <utility factory=".locator.DefaultShoeLocator" />

Alternatively, you could skip the *implements()* call on the
factory and set it in ZCML. This may also be necessary in order to
disambiguate if you have more than one interface being provided by
the utility component:

::

    <utility 
        factory=".locator.DefaultShoeLocator" 
        provides=".interfaces.IShoeLocator
        />

Now you can find the utility using *getUtility()*:

::

    >>> from zope.component import getUtility
    >>> locator = getUtility(IShoeLocator)
    >>> locator.findShoes(u"optilude")
        ...

The utility registry turns out to be a very useful generic
registry, because like the adapter registry, it can manage
*named utilities*. Let's say that you had a few different shoes you
wanted to keep around:

::

    >>> left = Shoe()
    >>> right = Shoe()
        ...
    
    >>> from zope.component import provideUtility
    >>> provideUtility(left, name=u'left-shoe')
    >>> provideUtility(right, name=u'right-shoe')

We can now find these utilities again using the *name* argument to
*getUtility()*.

::

    >>> to_put_on = getUtility(IShoe, name=u'left-shoe')

Of course, we are still using the transient global utility
registry, so these will diseappear when Zope is restarted. We could
use local components instead (see below), or we could register them
using ZCML. If we had defined the shoes *left* and *right* in a
module *shoes.py*, we could write:

::

    <utility
        component=".shoes.left"
        name="left"
        />
    
    <utility
        component=".shoes.right"
        name="right"
        />

An alternative would have been to define two classes *LeftShoe* and
*RightShoe* and use the *factory* attribute of the directive
instead of *component* (which refers to an instance, rather than a
class/factory).

Local components
--------------------

The examples above all use global, transient registries that are
reloaded each time Zope is restarted. That is certainly what you
want for code and functionality. Sometimes, you would like for
utilities to be a bit more like their CMF cousins and also manage
persistent state. To achieve that you need to use local components,
which are stored in the ZODB.

Prior to Zope 3.3, which is included in Zope 2.10, local components
were a bit of a black art. Then came the *jim-adapter* branch and
everything was greatly simplified. The theory is still the same,
the API is just much more sane. Each time Zope executes a request
(or if you implicitly invoke *zope.component.setSite()*, for
example in a test), it discovers which is the nearest *site* to the
context. In Plone, the site is normally the root of the Plone
instance, but in theory any folder could be turned into a site.

A *site* has a local component registry, where local utilities and
adapters may be defined. This means that a particular utility or
adapter can be specific to a particular Plone site, not affecting
other Plone instances in the same Zope instance. You cannot use
ZCML to register local components, since ZCML is inherently global
(at least for now) - it does not know anything about your
particular sites. However, you can register them with Python code,
e.g. in an Install.py or a GenericSetup profile, using calls like
*provideUtility()* (and its equivalent, *provideAdapter()*) called
on a local site manager instance:

::

    >>> from zope.component import getSiteManager
    
    >>> getUtility(IShoe, name=u'left-shoe) is left
    True
    
    >>> sm = getSiteManager(context)
    >>> sm.provideUtility(myShoe, name=u'left-shoe')
    >>> getUtility(IShoe, name=u'left-shoe) is myShoe
    True

Unfortunately, Plone 2.5 does not run on Zope 2.10. We won't cover
local components here, because, well, I never learnt how to do it
the Zope 2.9 way, and what I saw of it scared me. I'm told it's not
that bad, and there is documentation in *Five* and in Zope 3
itself. Local components will become more important in Plone 3.0,
where Zope 2.10 or later will be required and more things that use
local components will be part of the core.

b-org does not use local components yet, and we will see how the
extension mechanism would benefit from local components so that you
could have one b-org extension installed in one Plone instance and
another extension installed in another Plone instance, without the
two interfering. Luckily, to code that *uses* adapters and
utilities, it is completely transparent whether they are global or
local.

Conclusion
-------------

That's it! If you can master the concepts of interfaces, adapters
and utilities you will go far in a Zope 3 world. They will become
much more natural as you use them a few times, and you'll probably
wonder how you ever managed without them. Hopefully, that point
will come before the end of this tutorial, which is largely focused
on showing how the principle of separation of concerns can be
imposed upon your Archetypes and Plone code.

5.3. Overview of b-org
======================

The big picture

To the user, b-org presents itself as three content types:



Department 
    A container for employees, and a source of groups. That is, each
    department becomes a group, and the employees within that
    department become group members.
Employee 
    Information about employees, and a source of users. That is, each
    active employee object becomes a user who can log in and interact
    with the portal.
Project 
    A project workspace - a folder where employees can collaborate on
    content. Content inside the project folder has a custom workflow,
    and employees who are related to the project (by reference) have
    elevated permissions over this content.

Out of the box, these are not terribly interesting, because they
have only the minimum of metadata required to function. The task of
providing actual schema fields, view templates, content type names
(if Department, Employee and Project are not appropriate) and other
application-specific facets is left up to simpler third-party
products that plug into b-org. One example of such a product is
included, which models a hypothetical charity use case and is
called *charity*.
This seemingly innocuous orchestration of functionality is achieved
by a variety of means:

Archetypes 
    Used to build the actual content types and their schemata.

The Zope 3 Component Architecture 
    Is used to make all this exensibility possible - you will see lots
    of examples of interfaces, adapters and utilities.

Membrane 
    The content types are registered with *membrane* to be able to act
    as groups and users

PAS and PlonePAS 
    The Pluggable Authentication Service is used by membrane to
    actually provide user sources. A custom PAS plug-in is also used to
    manage local roles for members and managers within projects and
    departments.

GenericSetup 
    The next-generation set-up and installation framework is used to
    install and configure b-org. *charity* demonstrates how
    GenericSetup XML profiles can be used directly, without depending
    on the actual GenericSetup import mechanism.

Zope 3 events
    Zope 3's event dispatch mechanism is used to ensure employee users
    actually own their own Employee objects, among other things.

Zope 3 views 
    The *charity* demo uses views for its display templates.

Annotations 
    Employees' passwords are hashed and stored in an annotation

Placeful workflow 
    To let content inside projects have a different workflow to that of
    the rest of the site, each project uses a *CMFPlacefulWorkflow*
    policy.

On the following pages, you will learn about each of these
components and how it fits together. Meanwhile, you can follow
along the code by looking in the
`subversion repository <http://svn.plone.org/svn/collective/borg/trunk>`_,
or getting b-org from its
`product page <https://plone.org/documentation/manual/developer-manual/products/borg>`_.

5.4. To Archetype or not to Archetype
=====================================

Archetypes is still the most complete framework for building
content types quickly. With the advent of Zope 3, there is an
alternative in Zope 3 schemas. Here's why b-org doesn't use them.

There is a growing consensus that Archetypes has grown a little too
organically. On the one hand, Archetypes has given us a lot of
flexibility, and made many of us more productive than we would ever
have thought possible (for those who remember the heady days of
plain Zope 2, and then plain CMF development). On the other hand,
Archetypes has become fairly monolithic. The reference engine, for
example, is woven tightly into the field type machinery, and the
way that views are composed from widgets makes these almost
impossible to re-use outside of Archetypes.

In practical terms, the biggest headache that arises from
Archetypes' evolution is the very same problem we identified when
introducing Zope 3 concepts - it's hard to re-use Archetypes-based
components without sub-classing and repeating a large portion of a
type's configuration. Take
`the Poi issue tracker <https://plone.org/products/poi>`_, for
example - I frequently get requests from people who want to add a
few use-case specific fields to each issue, or add some new
functionality such as having private issues or issues submitted on
behalf of someone else. The problem is that I don't want to put all
this functionality in Poi itself, because this would increase the
complexity of the product and thus the maintenance burden and
probably impact the intuitiveness of the UI, when in reality not
everyone would benefit from such new features.

Ideally, someone would be able to plug in their own schema fields
and add some logic in well-defined places without having to
re-invent all of Poi. However, this is difficult, because, for
example, the "add issue" button assumes you are adding a *PoiIssue*
object, which has a schema defined wholly in
*Products/Poi/content/PoiIssue.py*. There are custom form
controller scripts to handle saving of issues, and a lot of methods
are found in the various content classes to do things like send
mail notifications or perform issue searches for various lists.
Again, changing the logic of who gets an email notification or how
a particular list of open issues is calculated may involve
subclassing one or all of Poi's content types, re-registering view
templates and other content type information, and possibly
customise a number of templates and scripts to reference the new
subclassed types. Of course, when Poi itself changes, keeping these
customisations up-to-date becomes difficult.

Zope 3 has, in keeping with its philosophy, approached these
problems by promising separation of concerns. In Zope 3, you would
typically define an interface that specifies the *schema* of a
content type, and then create a class that is only concerned with
holding and persisting the data for this schema:

::

    from zope.interface import Interfacefrom zope import schemaclass IIssue(Interface):    """A tracker issue    """    title = schema.TextLine(title=u"The short title of this issue", required=True)    severity = schema.Int(title=u"The severity of this issue", required=True, default=3)...from persistent import Persistentfrom zope.interface import implementsclass Issue(Persistent):    implementS(IIssue)    title = u""    severity = 0

The actual functionality for sending notifications etc would be in
various adapters (e.g to *INotifying*), the view logic in views.
Forms can be created from schema interfaces like *IIssue* above,
using *zope.formlib*. This can handle proper add forms (so the
object is not created until the form has been filled in, which is
another headache with CMF content types and therefore also
Archetypes), validation, edit forms etc. Each form, adapter and
menu entry (for the "add" menu, say) is registered separately,
meaning that they can also be overridden and customised separately.
Rocky Burt has written an excellent tutorial on
`how to use formlib in a Plone context <https://plone.org/documentation/manual/developer-manual/archetypes/appendix-practicals/using-zope-formlib-with-plone>`_ that
may be enlightening.

There are voices that say we should dump Archetypes entirely in
favour of Zope 3-style content objects. Other voices (including my
own) say that this may be a bit premature. Certainly, Zope 3
schemas and content objects are not yet fully integrated into CMF
and Plone, so you end up depending on some CMF base classes at the
very least. Moreover, the number and richness of widgets available
for Zope 3 forms does not yet match that of Archetypes.
Fundamentally, Archetypes has been around for a long time and has
grown to meet a wide variety of use cases, whereas in the context
of Plone at least, Zope 3 schemas are a new kid on the block.

The point is - Archetypes is not going to go away, not for a long
time anyway, and are still the right choice for many types of
applications. Almost all of Plone's add-on products use Archetypes,
and it is well-understood by our developer community. The more
likely scenario is that Archetypes will evolve in the same way that
Zope 2 is evolving, by seeing its internals refactored piecemeal
and pragmatically to take advantage of Zope 3 equivalents and
concepts, until theoretically an Archetypes schema and content
object is just a different spelling for what Zope 3 is doing, and
Zope 3's content type story offers the same richness as Archetypes
does (and more).

In the meantime, Archetypes is the right choice for b-org (and for
other membrane-based systems). What we will try to do, however, is
to alleviate the aforementioned problems by making use of Zope 3
design techniques, in order to make b-org extensible and flexible.

5.5. The extension story
========================

One of the main drivers behind the componentisation of b-org is
that it should be easy to extend and customise for third party
developers. We'll take a look at how such customisations may look,
before considering how we made it possible.

b-org ships with an example called *charity*, found in the
*examples/charity* directory, which demonstrates one use-case
specific implementation of b-org. This is quite simple, consisting
of the following top-level files and directories:



configure.zcml
    Registers the schema extension adapters (see below) and references
    the browser package
Extensions/ 
    Contains an *Install.py* script that configures the Factory Type
    Information for the Department, Employee and Project content types.
    It does so by using GenericSetup XML files, but invokes the import
    handlers explicitly rather than through a GenericSetup profile.
Â browser/
    Contains Zope 3 views for the charity department, employee and
    project content types, and a *configure.zcml* to register these.
    More on views in a later section.
schema/ 
    Contains adapters that extend the schemas for Departments,
    Employees and Projects with use-case specific fields.



To use *charity* you should copy or symlink it from
*Products/borg/examples/charity*to *Products/charity*. It can be
installed as normal, but you must install b-org first. See
*borg/README.txt* for the full install instructions!

A key aim is to make it possible to meaningfully extend b-org
without needing to subclass all its types. Of course, you *can* do
that, but in most cases it's not necessary. Unfortunately, the
mechanisms and techniques described here will be "global" in
nature. That is, you will not be able to have two different modes
of customisation for two different Plone instances in the same Zope
instance. This is because prior to Zope 2.10 (which Plone 2.5 does
not support - it wasn't out until several months after Plone 2.5
was released), the "local" components story in Zope 3 was not fully
developed. There is also a specific problem with the way the schema
extension mechanism works which makes it inherently global.

When Plone 3.0 rolls around, it will support local components much
better, and Archetypes 1.5, in conjunction with a third-party
product called ContentFlavors (or possibly another similar tool),
will enable the kind of extension story described here to work on
almost any type. At that point, the forerunner you see in b-org now
will be obsolete.

Of course, if you don't need two different b-org customisations for
two different Plone sites in the same Zope instance (which I
suspect most people can work around - having two separate Zope
instances of course isolates you from all of this), you should be
fine.

The schemas extenders
------------------------

If you look at *charity/configure.zcml* you will see the following
registrations:

::

    <adapter factory=".schema.department.DepartmentSchemaExtender" />
    <adapter factory=".schema.employee.EmployeeSchemaExtender" />
    <adapter factory=".schema.project.ProjectSchemaExtender" />

These schema extenders are adapters that hook into a specific part
of b-org. We will describe this in more detail later, but here is
how they look from the point of view of the extending product:

::

    from zope.interface import implementsfrom zope.component import adaptsfrom Products.Archetypes.atapi import *from Products.borg.interfaces import IEmployeeContentfrom Products.borg.interfaces import ISchemaExtenderCharityEmployeeSchema = Schema((    StringField('title',        accessor='Title',        required=True,        user_property='fullname',        widget=StringWidget(            label=u"Full name",            description=u"Full name of this employee",        ),    ),    StringField('email',        validators=('isEmail',),        required=True,        searchable=True,        user_property=True,        widget=StringWidget(            label=u"Email address",            description=u"Enter the employee's email address",        ),    ),    StringField('phone',        required=False,        searchable=True,        user_property=True,        widget=StringWidget(            label=u"Phone number",            description=u"Enter the employee's phone number",        ),    ),    StringField('mobilePhone',        required=False,        searchable=True,        user_property=True,        widget=StringWidget(            label=u"Mobile phone number",            description=u"Enter the employee's mobile phone number",        ),    ),    StringField('location',        searchable=True,        user_property=True,        widget=StringWidget(            label=u"Location",            description=u"Your location - either city and country - or in a company setting, where your office is located.",        ),    ),    StringField('language',        user_property=True,        vocabulary="availableLanguages",        widget=SelectionWidget(            label=u"Language",            description=u"Your preferred language.",        ),    ),    TextField('description',        required=True,        searchable=True,        user_property=True,        default_content_type='text/html',        default_output_type = 'text/x-html-safe',        allowable_content_types = ('text/html', 'text/structured', 'text/x-web-intelligent',),        widget=RichWidget(            label=u"Biography",            description=u"Enter a short biography of the employee",        ),    ),    ))class EmployeeSchemaExtender(object):    """Extend the schema of an employee to include additional fields.    """    implements(ISchemaExtender)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def extend(self, schema):        schema = schema + CharityEmployeeSchema        # Reorder some fields        schema.moveField('description', after='mobilePhone')        schema.moveField('location', before='description')        schema.moveField('language', before='description')        schema.moveField('roles_', after='description')        return schema

This example is *employee.py*. The other extensions are simpler,
and work on the exact same principle. When calculating the schema
of a content type, the b-org types (by virtue of
*Products.borg.content.schema.ExtensibleSchemaSupport*, a mix-in
class that all the b-org types uses, and which the aforementioned
changes to Archetypes should make obsolete) will look up an adapter
from the content object (which is marked with *IEmployeeContent*,
in this case), to *ISchemaExtender*. This will be given the chance
to extend (and modify) the schema of the type.

The returned value is cached (to avoid an expensive re-calculation
each time the schema is used). This cache can be invalidated upon
an event, which you will see in *charity/Extensions/Install.py*:

::

    from zope.event import notify
    from Products.borg.content.schema import SchemaInvalidatedEvent
    from Products.borg.content.employee import Employee
    ...

    def install(self, reinstall=False):
        ...
        notify(SchemaInvalidatedEvent(Employee))

The event is an instance of a class that implements
*ISchemaInvalidatedEvent*, and takes a class as an argument to know
which class the schema is being invalidated for.

Defining new views and type information
-----------------------------------------

We have now managed to add new schema fields to Department,
Employee and Project. The auto-generated edit form will pick these
up for editing, but we probably also want some custom views. We may
also want to change other aspects of the Factory Type Information
(FTI) which controls how the type is presented within Plone's UI
(an FTI is an object in *portal\_types*).
First, we define some views in the *browser* package. These are
described in a later section, but lookin at
*charity/configure.zcml*, you will see:

.. code-block:: xml

    <include package=".browser" />

This will bring in *charity/browser/configure.zcml*, which contains
several directives like:

.. code-block:: xml

      <page
          name="charity_employee_view"
          for="Products.borg.interfaces.IEmployeeContent"
          class=".employee.EmployeeView"
          template="employee.pt"
          permission="zope2.View"
          />

This, along with the class
*Products.charity.browser.employee.EmployeeView*and the
template*charity/browser/employee.pt* will make a view
*@@charity\_employee\_view* (the @@ is optional, but serves to
disambiguate views from content objects, for example) available on
any employee (or rather, any object providing *IEmployeeContent*).
We then need to tell Plone that this view should be invoked when
you view an Employee object or click its 'View' tab. This is done
by setting the *(Default)* and *view* method aliases for the
Employee type. See
`this page of the RichDocument tutorial <https://plone.org/documentation/tutorial/richdocument/actions-and-aliases>`_
for some background.
To achieve this, we could modify *portal\_types/Employee* in Python
during the *Install.py* script. However, to make it easier to
define the FTI, we use a GenericSetup XML file instead. Take a look
at *charity/Extensions/setup/types/Employee.py*, for example:

.. code-block:: xml

    <object name="Employee" meta_type="Factory-based Type Information"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n">
      <property name="title">Employee</property>
      <property name="description">A charity employee or
      volunteer.</property>
      <property name="content_icon">employee.gif</property>
      <property name="content_meta_type">Employee</property>
      <property name="product">borg</property>
      <property name="factory">addEmployee</property>
      <property name="immediate_view">base_edit</property>
      <property name="global_allow">False</property>
      <property name="filter_content_types">False</property>
      <property name="allowed_content_types" />
      <property name="allow_discussion">False</property>
      <alias from="(Default)" to="@@charity_employee_view" />
      <alias from="view" to="@@charity_employee_view" />
      <alias from="edit" to="base_edit" />
      <alias from="properties" to="base_metadata" />
      <alias from="sharing" to="folder_localrole_form" />
      <action title="View" action_id="view" category="object"
      condition_expr="" url_expr="string:${object_url}" visible="True">
        <permission value="View" />
      </action>
      <action title="Edit" action_id="edit" category="object"
      condition_expr="" url_expr="string:${object_url}/edit"
      visible="True">
        <permission value="Modify portal content" />
      </action>
      <action title="Properties" action_id="metadata" category="object"
      condition_expr="" url_expr="string:${object_url}/properties"
      visible="True">
        <permission value="Modify portal content" />
      </action>
      <action title="Sharing" action_id="local_roles" category="object"
      condition_expr="" url_expr="string:${object_url}/sharing"
      visible="True">
        <permission value="Modify portal content" />
      </action>
    </object>

To learn more about HTML Tidy see http://tidy.sourceforge.net
Please fill bug reports and queries using the "tracker" on the Tidy web site.
Additionally, questions can be sent to html-tidy@w3.org
HTML and CSS specifications are available from http://www.w3.org/
Lobby your company to join W3C, see http://www.w3.org/Consortium

This defines the various aspects of the FTI, and is basically a
modified copy of the equivalent file from the b-org extension
profile. You'll learn more about these in the section on
GenericSetup, but for now observe that we invoke this explicitly in
Install.py, via some boilerplate utility code:
::

    from Products.charity.Extensions.utils import updateFTIdef install(self, reinstall=False):    ...    if not reinstall:        updateFTI(self, charity, 'Department')        updateFTI(self, charity, 'Employee')        updateFTI(self, charity, 'Project')

This will update the FTIs by examing
*Products/charity/Extensions/setup/types*. Each file there is named
corresponding to the name of the FTI it modifies.

Adding new functionality
---------------------------

Extending the schema and modifying the FTI to support different
views is probably enough for a large number of use cases. If you
find yourself thinking "I wish I could add a method to the Employee
class to support ...", take your left hand, hold it out, raise you
right hand and slap your left wrist sternly, then read the section
on adapters again.
For example, let's say you wanted to send an email to
administrators when a particular button in the view was clicked.
You could do that in an adapter. For examples, in your
*interfaces* module, you could could have:
::

    from zope.interface import Interfaceclass IAdministratorNagging(Interface):    """Someone who will nag the admin    """    def nag(message):        """Send nagging email        """

Then, an adapter from IEmployee in module *nag.py*:

::

    from zope.interface import implementsfrom zope.component import adaptsfrom interfaces import IAdministratorNaggingfrom Products.borg.interfaces import IEmployeeContentfrom Products.CMFCore.utils import getToolByNameclass NaggingEmployee(object):    implements(IAdministratorNagging)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def nag(self, message):        mailHost = getToolByName(self.context, 'MailHost')        ...

And finally, in your *configure.zcml*:

::

    <adapter factory=".nag.NaggingEmployee" />

Then, in the form handler that is about to nag the employee, you
would do:

::

    from Products.myproduct.interfaces import IAdministratorNaggingnagger = IAdministratorNagging(employee)nagger.nag("Give me more disk space!")

Obviously, this is a somewhat contrived example, but hopefully you
get the gist.

Modifying workflow and other configuration
----------------------------------------------

The b-org workflows are not special. In your Install.py, you could
modify them or change the workflow assignments as you would any
other content type. You can also use *CMFPlacefulWorkflow* to
assign different workflows depending on context, if need be.

Similarly, if you need to modify the behaviour of the Department,
Employee and Project types in other ways, for example by modifying
settings in *portal\_properties*, you are of course free to do so.
The intended pattern is that your b-org customisation product
encapsulates the various settings and extensions that describe your
use case.

Changing fundamental b-org behaviour
---------------------------------------

Lastly, as you learn about b-org you will see how it uses adapters
to hook into membrane. If you need to override its behaviour, you
can add an *overrides.zcml* to your product, which is otherwise
identical to a *configure.zcml* in format, but is able to override
earlier registrations (such s those in b-org). For example, you
could override the adapter from *IEmployeeContent* to *IUseRelated*
to change the way in which user ids is assigned, or the adapter to
*IUserAuthentication* to change the way in which authentication is
performed.

5.6. Filesystem organisation
============================

b-org attempts to adhere to modern ideal about how code should be
laid out on the filesystem.

In the Zope 3 world, the *Products* pseudo-namespace is frowned
upon. In Zope 2, every extension module lives in the Products/
folder. This raises some obvious namespace clash concerns, but also
separates Zope modules further from plain-Python modules. In Zope
3, you can install a module anywhere in your *PYTHONPATH*. For
example, in Plone 3.0, there will be a module called
*plone.portlets*, normally installed in
*lib/python/plone/portlets*.

For modules that need to act like Zope products (i.e. they need an
*initialize()* method, they install content types, they register a
GenericSetup profile or CMF skins or use an *Extensions/Install.py*
method, say), this works in Zope 2.10 and later. It can also be
made to work in earlier version of Zope using a product
(ironically) called *pythonproducts*.

For the purposes of borg, we stick with the traditional *Products/*
installation. It's nice to have imports like
*from borg import ...*, but fundamentally, b-org is very closely
tied to Zope (2) and Plone, so the re-use argument goes away, and
that nice import syntax is not really worth the extra dependency
and configuration.

One thing you may notice, though, is that the *borg* product is
named in lowercase, in keeping with Zope 3 and Python naming
conventions. Looking inside it, you will see the following key
files and directories:

 

\_\_init\_\_.py 
    Initialises the Zope 2 product machinery, registers content types,
    the skin layer and the GenericSetup extension profile that is used
    to install b-org.
config.py 
    Holds various constants
configure.zcml 
    Starts the Zope 3 snowball going. This references other packages
    with their own *configure.zcml* files.
content/ 
    Contains the Archetypes content types for Department, Employee and
    Project. Also contains some utilities, like *EmployeeLocator*, an
    adapter to find employees, two utilities used to provide
    vocabularies *AddableTypesProvider* and *ValidRolesProvider*, and
    the the schema extension mechanism in *schema.py*.
events/ 
    Contains event subscribers which modify ownership of an Employee
    object so that the employee user owns it (and can thus edit their
    own profiles, for example), as well as to set up the local workflow
    when a Project is created.
interfaces/ 
    Contains all the interfaces that b-org defines, in various
    sub-modules like *interfaces/employee.py* for the Employee-related
    interfaces. All of these are imported into
    *interfaces/\_\_init\_\_.py*, so that you can write
    *from Products.borg.interfaces import ...*.
membership/
    Contains various adapters for plugging into membrane which enable
    b-orgs user-and-group functionality.
pas/ 
    Contains a custom PAS plug-in which is used to manage the local
    roles for Project members
permissions.py 
    Contains custom add-content permissions, so that the ability to add
    Department, Employee and Project content objects can be controlled
    by different permissions.
profiles/ 
    Contains the GenericSetup extension profile that sets up b-org.
    This is registered in the *borg/*\_\_init\_\_.py*.*
setuphandlers.py 
    Defines a custom GenericSetup "import step" which configures
    aspects of b-org that cannot be expressed in the existing
    GenericSetup XML formats.
skins/ 
    Contains the borg skin layer, which is registered in
    *borg/\_\_init\_\_.py*. This contains only the b-org icons. These
    could potentially have been defined in a *browser* package using
    Zope 3 resources, but are included in a traditional skin layer to
    make them easier to customise using conventional methods. See the
    section on Zope 3 views for more details.
 tests/
    Contains unit and integration tests.
zmi/ 
    Defines a ZMI page for adding the PAS plug-in, for completeness'
    sake.

You will notice that there are many directories, and many of these
directories contain the same set of files - *employee.py*,
*department.py* and *project.py*. This is a side-effect of the
finer-grained components and increased separation of concerns that
stem from Zope 3 design concepts. For products that act less as
framework, the degree of separation may be lower, and thus the
product may appear smaller. However, as you browse b-org's source
code, it should become obvious why things are placed where they
are, and how code is grouped together by logical functionality
rather than a tight coupling to Archetypes content types.

 

5.7. Interfaces
===============

In Zope 3, everything is connected to an interface in some way.
Sure enough, b-org has a slew of them. Getting the interface design
right is often more than half the battle, so pay attention to this
part.

If you were trying to understand b-org without a comprehensive
tutorial to hand, you would do well to look at the *interfaces*
package. You will notice that this is subdivided into various
files



interfaces/department.py 
    Contains a description of a department (*IDepartment*) and a marker
    interface for the content object that stores the department
    (*IDepartmentContent*).
interfaces/employee.py 
    Contains the equivalent interfaces, *IEmployee* and
    *IEmployeeContent*, as well as the definition of a specific event
    interface, *IEmployeeModified.*
interfaces/project.py 
    Again contains *IProject* and *IProjectContent*, as well
    *ILocalWorkflowSelection*, which is used to denote a utility that
    defines the placeful workflow policy that projects will use.
interfaces/workspace.py 
    Holds the interface *IWorkspace*, which is used by the local-role
    PAS plug-in to extract which users should have which local roles in
    a project.
interfaces/schema.py 
    Contains interfaces relevant to the custom schema extension
    mechanism - *ISchemaExtender*, *IExtensibleSchemaProvider* and
    *ISchemaInvalidatedEvent*.
interfaces/utils.py 
    Defines interfaces that are used as input to various vocabularies -
    *IEmployeeLocator*, *IAddableTypesProvider* and
    *IValidRolesProvider*.



In order to understand what each of these interfaces describes in
more detail, look at the files above. Recall that interfaces are
mainly documentation - these interfaces are accompanied by
docstrings and generally self-documenting code.

The various interfaces intended for public consumption are imported
to *interfaces/\_\_init\_\_*.py, so that client code can write,
e.g.:

::

    from Products.borg.interfaces import IEmployee

This is a common idiom. If you find yourself with too many
interfaces to manage in *interfaces/\_\_init\_\_.py*, you don't
necessarily need to do this, but it's probably a sign that you
should be breaking your code into smaller packages!
Remember that unless you have a particular need to depend on Zope
2, then you don't need to pollute the *Products* namespace with
such components! (and even if you do, with *PythonProducts* or Zope
2.10, you can do without the Products/ namespace too). For example,
we could have placed the employee functionality in a package
*borg.employee*, found in *lib/python/borg/employee* as a
plain-python library, possibly depending on Zope 3 components (i.e.
packages in the *zope.*\* namespace).
Conversely, if you have relatively few interfaces, you can simply
have an *interfaces.py* module without a directory.

Separating Archetypes from real components
----------------------------------------------

One thing you may notice is that we have split the interface
describing the concept of e.g. an employee (*IEmployee*) from the
interface that describes the employee content object in the ZODB
(*IEmployeeContent*). Whether this is always the right thing to do
is debatable, but the reasoning goes something like this:
Archetypes objects contain a very large API. Archetypes *schemas*
and the infamous *ClassGen* generate methods on the content objects
corresponding to schema fields, so that a field *name* gets an
accessor called *getName()* and a mutator called *setName()*. This
is all rather Archetypes-specific, and in Zope 3 schemas, we
typically prefer simple properties (a *name* attribute) to pairs of
methods. To avoid being constrained by the Archetypes when defining
interfaces (Archetypes is just one implementation choice), we
created *IEmployee* as follows:
::

    class IEmployee(Interface):    """An employee, which is also a user.    """    id = schema.TextLine(title=u'Identifier',                         description=u'An identifier for the employee',                         required=True,                         readonly=True)    fullname = schema.TextLine(title=u'Full name',                               description=u"The employee's full name for display purposes",                               required=True,                               readonly=True)

To support this, we could put the relevant properties into the
Archetypes content object, but this is cumbersome, since the
*property()* declaration normally used to convert methods to
properties will only work when those methods actually exist, not
when they are created by *ClassGen*.
Instead, we mark the content object with a marker interface,
*IEmployeeContent* and then register an adapter to *IEmployee*.
Strictly speaking, this is cheating, since the adapter makes
assumptions about its context (such as which methods are available,
and the fact that it uses Archetypes) that are not formally defined
in the interface. To save excessive typing and retain some sanity
in the interface definitions, it's not a terrible compromise
though. Here's the adapter, from *membership/employee.py*:
::

    class Employee(object):    """Provide department information.    """    implements(IEmployee)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    @property    def id(self):        return self.context.getId()    @property    def fullname(self):        return self.context.Title()

Now, you can write:

::

    emp = IEmployee(some_employee_content_object)print emp.fullname

Another side-effect of this pattern is that we can separate things
that are Archetypes-dependent from things that operate on the more
general notion of an employee. For example, membrane generally
makes assumptions about operating on Archetypes content objects, so
the various membrane adapters adapt IEmployeeContent, whereas the
view for charity employees is only concerned with "real" employees
and so adapts the context to IEmployee.

This pattern is repeated for Departments and Projects as well.

Interfaces intended for utilities and adapters
-------------------------------------------------

Although interface design should generally not be too concerned
with how those interfaces are implemented, you will often think
"this is going to be used a a utility" or "this will most likely be
an adapter". In this case, you may want to make some reference in
the doc-string at least. For example, the *ILocalWorkflowSelection*
interface states:
::

    class ILocalWorkflowSelection(Interface):    """A selection of a local workflow for projects.    This will normally be looked up as a utility.    """    workflowPolicy = schema.TextLine(title=u'Workflow policy identifier',                                    description=u'The id of the placeful workflow policy to use',                                    required=True,                                    readonly=True)

Conversely, many interfaces are context-dependent, which means that
most likely they will either be directly provided by a particular
object or adaptable to it. Take the *IAddableTypesProvider*:
::

    class IAddableTypesProvider(Interface):    """A component capable of finding addable types in a given context.    """    availableTypes = schema.Tuple(title=u'Available types',                                  description=u'A list of all addable types',                                  value_type=schema.Object(ITypeInformation))    defaultAddableTypes = schema.Tuple(title=u'Default addable types',                                       description=u'A list of types to be addable by default',                                       value_type=schema.Object(ITypeInformation))        

The implication here is that client code will do something like:
::

    from Products.borg.interfaces import IAddableTypesProvideraddableTypes = IAddableTypesProvider(context).availableTypes

Whether IAddableTypesProvider was provided directly by the context
or (more likely) provided via an adapter is not important. The only
time this distinction is really useful is in the case of marker
interfaces, such as *IEmployeeContent*:
::

    class IEmployeeContent(Interface):    """Marker interface for employee content objects"""

These are often checked with *providedBy()*:
::

    assert IEmployeeContent.providedBy(employeeContentObject)# we've got an employee, good

Again, the guiding principle here is *separation of concerns*. The
aspect of a component that can provide a list of addable types
(*IAddableTypesProvider*) is logically distinct from (and could be
varied independently of) the aspect of a component that specifies
it represents a project (*IProject*), even though it so happens
that at present projects are the only time we concern ourselves
with restricting addable types.
In the olden days, we would probably have put methods like
*getAvailableProjectAddableTypes()*into the *Project* content type.
Hopefully, you'll see why this is less optimal than having it in a
separate component (hint: what if you in your customisation of
b-org wanted to be much more particular about which types were
addable?). You will hopefully start to pick up "fat" interfaces
during interface design - if you had a neat *IProject* interface
that described attributes of a project that were to be saved
alongside the project object, and then found a couple of methods
about defining addable types that were related to one another but
not so much to the data of a project in general, you would
hopefully reach for a new interface. If so - well done, you're
getting there.

5.8. Test-driven development
============================

Testing should come first, not last, when doing development.

One of the greatest things that Zope 3 has established is a culture
of test-driven development. Because Zope 3 components tend to be
small and not dependent on a large framework or (typically) a
running application server, tests are easier to write and execute
faster. Most Zope 3 testing happens in the form of testable
documentation - DocTests - which tell the story of how a component
should be used along with testable examples.

The
`testing tutorial <https://plone.org/documentation/tutorial/testing>`_
explains the philosophy behind test-driven development and the
tools and techniques available in Zope. It is **required reading**
if you are not familiar with testing in Zope, and probably quite
useful even if you are.

Testing strategy
------------------

Tests were (largely) written against interfaces and stub
implementations, before the actual functionality was written. One
of the first test cases to be created was *test\_adapters.py*,
which simply verifies that the various adapter registrations are in
effect. This is obviously an integration test (using
PloneTestCase), since it is verifying what happens on a "normal"
Zope start-up.
You will also notice tests named after the three content types,
*test\_department.py*, *test\_employee.py* and *test\_project.py*.
Each of these contains tests that verify the given type is
available and can be instantiated and edited. This catches errors
in Archetypes registrations or schemas. There are then further
tests for the *membrane*integration and for the adapters to the
canonical interfaces *IDepartment*, *IEmployee* and *IProject*.
Lastly, non-trivial methods in content types and relevant adapters
are given their own test fixtures.
By being systematic and diligent with tests, many, many bugs were
caught and dealt with before they ever hit a live system. Of
course, this does not replace in-browser acceptance testing, which
was also performed regularly.
At the time of writing, there are no *zope.testbrowser* based
functional tests for the user interface. That is regrettable - and
this is an open source project after all, so feel free to
contribute some!

Test set-up
--------------

You will find b-org's tests in the *tests* module. Most of these
use are DocTest integration tests, using PloneTestCase. Make sure
you use a recent version of PloneTestCase (or svn trunk) since
there have been some recent changes in how Zope 3 components (or
rather, ZCML registrations) are loaded for test runs. The upshot is
that with PloneTestCase, things should "just work" for integration
testing - components you have defined in ZCML in your products will
be loaded as they would when Zope is started.

The file *base.py* contains an insulating base class for b-org
tests, called *BorgTestCase* and its sister-class
*BorgFunctionalTesetCase*. When imported, this file will trigger
the setup of a Plone site with the *membrane* and *borg* extension
profiles installed, as such:

::

    from Testing import ZopeTestCase# Let Zope know about the two products we require above-and-beyond a basic# Plone install (PloneTestCase takes care of these).ZopeTestCase.installProduct('membrane')ZopeTestCase.installProduct('borg')# Import PloneTestCase - this registers more products with Zope as a side effectfrom Products.PloneTestCase.PloneTestCase import PloneTestCasefrom Products.PloneTestCase.PloneTestCase import FunctionalTestCasefrom Products.PloneTestCase.PloneTestCase import setupPloneSite# Set up a Plone site, and apply the membrane and borg extension profiles# to make sure they are installed.setupPloneSite(extension_profiles=('membrane:default', 'borg:default'))

Integration and unit tests
----------------------------

Most of the tests are integration test that are set up like so:

::

    import unittestfrom Testing.ZopeTestCase import ZopeDocTestSuitefrom base import BorgTestCasefrom utils import optionflagsdef test_creation():    """Test that departments can be created an initiated.    >>> self.setRoles(('Manager',))    >>> id = self.portal.invokeFactory('Department', 'dept')    >>> dept = self.portal.dept    Set roles.    >>> dept.setRoles(('Reviewer',))    >>> tuple(dept.getRoles())    ('Reviewer',)    Add an employee and set it as a manager.    >>> id = dept.invokeFactory('Employee', 'emp')    >>> dept.setManagers((dept.emp.UID(),))    >>> tuple(dept.getManagers())    (<Employee at ...>,)    """...def test_suite():    return unittest.TestSuite((            ZopeDocTestSuite(test_class=BorgTestCase,                             optionflags=optionflags),        ))

There is also a plain-python (no loading of Zope necessary, which
is much faster) unit test for the password digest in
*test\_passwords.py*. This is appropriate because the functionality
under test does not depend on the Zope application server or
database being loaded. Use plain-python (or perhaps rather, plain
Zope 3) tests whenever you can to reduce interdependencies and test
load times:

::

    import unittestfrom zope.testing.doctestunit import DocTestSuitefrom utils import configurationSetUp, configurationTearDown, optionflagsdef test_passwords_hashed():    """Check that passwords are hashed    We expect that the password will be saved as a SHA-1 digest.    >>> import sha    >>> digest = sha.sha('secret').digest()    Set a password.    >>> from Products.borg.content.employee import Employee    >>> e = Employee('emp')    >>> e.setPassword('secret')    The value is stored in an annotation, and there is no direct way to    access it (deliberately). Thus, check the annotation directly.    >>> from zope.app.annotation.interfaces import IAnnotations    >>> from Products.borg.config import PASSWORD_KEY    >>> annotations = IAnnotations(e)    >>> password = annotations[PASSWORD_KEY]    Ensure it is what we expected:    >>> password == digest    True    """...def test_suite():    return unittest.TestSuite((            DocTestSuite(setUp=configurationSetUp,                         tearDown=configurationTearDown,                         optionflags=optionflags),        ))

The functions *configurationSetUp()* and *configurationTearDown()*
are defined in *utils.py* and are used to load specific ZCML files
that enable the test environment to function. This is necessary
because without PloneTestCase's integration test layer in effect,
there will be no compnent registrations when the tests are run!
This may be more cumbersome (though in reality, the same set of
components tend to be used), but also allows better control over
the environment in which test are run, in addition to (much) faster
test execution times.

From *utils.py*:

::

    import doctestfrom zope.app.tests import placelesssetupfrom zope.configuration.xmlconfig import XMLConfig# Standard options for DocTestsoptionflags =  (doctest.ELLIPSIS |                doctest.NORMALIZE_WHITESPACE |                doctest.REPORT_ONLY_FIRST_FAILURE)def configurationSetUp(self):    """Set up Zope 3 test environment    """    placelesssetup.setUp()    # Ensure that the ZCML registrations in membrane and borg are in effect    # Also ensure the Five directives and permissions are available    import Products.Five    import Products.membrane    import Products.borg    XMLConfig('configure.zcml', Products.Five)()    XMLConfig('meta.zcml', Products.Five)()    XMLConfig('configure.zcml', Products.membrane)()    XMLConfig('configure.zcml', Products.borg)()def configurationTearDown(self):    """Tear down Zope 3 test environment    """    placelesssetup.tearDown()

You will also find a regular unit test in *test\_setup.py*, simply
because this was quicker to write:

::

    from base import BorgTestCasefrom Products.membrane.interfaces import ICategoryMapperfrom Products.membrane.config import ACTIVE_STATUS_CATEGORYfrom Products.membrane.utils import generateCategorySetIdForTypefrom Products.borg.config import LOCALROLES_PLUGIN_NAME, PLACEFUL_WORKFLOW_POLICYclass TestProductInstall(BorgTestCase):    def afterSetUp(self):        self.types = ('Department', 'Employee', 'Project',)    def testTypesInstalled(self):        for t in self.types:            self.failUnless(t in self.portal.portal_types.objectIds(),                            '%s content type not installed' % t)    ...def test_suite():    from unittest import TestSuite, makeSuite    suite = TestSuite()    suite.addTest(makeSuite(TestProductInstall))    return suite

Finally, there is an docstring DocTest for the
*ExtensibleSchemaSupport* class. This is because this class if
largely standalone (it probably shouldn't be b-org at all, but in a
more general module, except Archetypes will gain similar
functionality of its own for Plone 3.0) and the test provided
important documentation in the class' docstring.

The class looks like this:

::

    class ExtensibleSchemaSupport(Base):    """Mixin class to support instance-based schemas.    Note: you must mix this in before BaseFolder or BaseContent, e.g.:    class Foo(ExtensibleSchemaSupport, BaseContent):        ...    This is based on Archetype's VariableSchemaSupport.    Define a content type with a marker interface:    >>> from zope.interface import Interface, implements    >>> class IMyType(Interface):    ...     pass    >>> from Products.Archetypes.atapi import *    >>> from Products.borg.content.schema import ExtensibleSchemaSupport    >>> class MyType(ExtensibleSchemaSupport, BaseObject):    ...     implements(IMyType)    ...     schema = BaseSchema.copy() + Schema((StringField('foo'),))    >>> registerType(MyType, 'testing')    Create a schema extender:    ...    """    implements(IExtensibleSchemaProvider)    ...

And the test runner, in *test\_schema.py*, contains:

::

    import unittestfrom Testing.ZopeTestCase import ZopeDocTestSuitefrom base import BorgTestCasefrom utils import optionflagsdef test_suite():    return unittest.TestSuite((            ZopeDocTestSuite('Products.borg.content.schema',                             test_class=BorgTestCase,                             optionflags=optionflags),        ))

5.9. Setup using GenericSetup
=============================

b-org uses GenericSetup to impose itself on your Plone instance.
Here's how it works.

Hands up if you have ever written a workflow definition in Python
and tried to figure out how to install it in your *Extensions.py*
and thought, this is the least useful API I have ever had to deal
with. Actually, the API is not that bad, it's just not very good
for performing set-up. Similarly, it may start to make your
separation-of-concerns-brainwashed mind a little uneasy that we
tend to define aspects of the type's configuration as class
attributes in an Archetypes class (though of course it's better
than using a CMF FTI dict or mangling *portal\_types* directly).

The fine folks who gave us the CMF came up with another way, called
*GenericSetup* (after a few name changes - you may see the names
*CMFSetup* and *ContentSetup* as well, which refer to predecessors
of what is not GenericSetup). This is based on a declarative XML
syntax that can represent site configuration. The configuration of
an entire site is called a *profile* and can be imported and
exported to replicate state across multiple Plone (or CMF) sites.
There is a smaller version of a profile called an
*extension profile* which can be used to extend a base profile.
Both membrane and b-org use extension profiles to install
themselves.

GenericSetup is described a
`tutorial <https://plone.org/documentation/tutorial/understanding-and-using-genericsetup-in-plone>`_
by Rob Miller, cheif GenericSetup protagonist, so we won't repeat
too much of the detail here. However, you should be aware that in
Plone 2.5, GenericSetup has a slightly awkward user experience and
does not have any well-defined way of performing uninstall, which
stems from the fact that it was originally designed for the use
case of taking a snapshot of the configuration of an entire site,
not for installing and uninstalling products and extensions!

The other main shortcoming at the moment is that there is no way to
specify interdependencies between profiles. It is important that
membrane is installed before b-org, but if you're not careful it
will happen the other way around. When you create a Plone site, you
will be able to choose a number of extension profiles to apply
(including meaningless ones like *Archetypes* - meaningless because
Plone already invokes those when you set up a site). In this list,
"Base organisation" comes before "membrane" by virtue of
alphabetical sorting. Therefore, you can't just choose both and
click "Add". Instead, you should select "membrane" first, and then
add "Base organisation" via portal\_setup, as described in the
b-org *README.txt:*


#. Go to *portal\_setup* in the ZMI
#. Click the *Properties* tab
#. Select "Base organisation" as the active profile (since this is
   an extension profile, it won't override the base profile that set
   up your Plone site) and click *Update*.
#. Go to the *Import* tab and click *Import all steps* at the
   bottom. Note that although it seems like this will re-install a
   whole bunch of stuff, it will only execute those steps that are
   actually listed in the *import\_steps.xml* for the
   *active profile*, which in this case is b-org's.

If you didn't already set up membrane and you created a Plone site
without the membrane extension profile, follow the same steps to
install membrane *before* you install b-org.
So why did we do all this? Firt of all, both membrane and b-org are
really infrastructure that fundamentally influence how you build
your site, so the lack of uninstall isn't as bad as it would have
been for more user-facing products. Secondly, with Plone 3.0, this
will become easier, as the QuckInstaller (and hence the
*Add/Remove Products* control panel page) becomes Extension Profile
aware and gives some uninstall support.
At the end of this section, you will see how you can use a
traditional QuickInstaller *Install.py* method and still get the
nice XML syntax, with a bit of extra work.

Import steps
--------------

To GenericSetup, the installation of a third party product via an
extension profile is considered to be the *importing* of that
profile. A file *import\_steps.xml* is used to determine which
actual import steps will be executed. First, we need to tell
GenericSetup where the import steps are defined, though, by
registering the extension profile. This is done in the product's
*\_\_init\_\_.py*:

::

    from Products.CMFPlone.interfaces import IPloneSiteRootfrom Products.GenericSetup import EXTENSION, profile_registry...def initialize(context):    ...    profile_registry.registerProfile('default',                                     'Base organisation',                                     'Organisation and project infrastructure',                                     'profiles/default',                                     'borg',                                     EXTENSION,                                     for_=IPloneSiteRoot)

This references the directory *profiles/default*, which contains
various files:



import\_steps.xml 
    Lists the steps to be performed during import (set-up)
export\_steps.xml 
    Lists the steps to be performed during export - that is, if the
    configuration is changed in the ZODB and the site admin wishes to
    export the configuration to a file, these steps will be performed.
membrane\_tool.xml 
    Configuration for membrane tools
skins.xml 
    Sets up skins in portal\_types
types.xml 
    Configures FTIs (Factory Type Information settings) for the content
    types that b-org ships with. Each of the types listed here has a
    corresponding file in *profiles/default/types* (the name of the
    type and the name of the file should match). This file contains all
    the various FTI settings, such as friendly name, meta type, actions
    and aliases.
workflows.xml 
    Configures workflows. This works in the same way as *types.xml* -
    the main file configures the names of the workflows and the
    bindings of workflows to content types. The actual workflow
    definitions, including states and transitions, are found in
    *profiles/default/workflows*.

The *import\_steps.xml* which orchistrates all this looks like
follows:


::

    <?xml version="1.0"?><import-steps>  <import-step id="borg_various" version="20060803-01"               handler="Products.borg.setuphandlers.importVarious"               title="Various base-org Settings">    <dependency step="typeinfo"/>    <dependency step="skins"/>    <dependency step="workflow"/> </import-step></import-steps>

Note that we don't actually specify most of the files - they are
referenced by the *base profile* that was used to set up Plone or
the extension profile for membrane. GenericSetup knows all the
registered profiles' steps, and looks for the corresponding files.

Various setup handlers
--------------------------

The one setup handler you do see is the "various" handler. This is
dependent on the set-up of type info, skins and workflow.
Ordinarily, setup handlers will utilise GenericSetup base classes,
adapters and utility functions to parse XML files. However, it's
not always convenient to invent a generic XML syntax for all types
of configuration. The *importVarious* pattern is used by many
products that need to perform some custom set-up in Python. It is
invoked as if it were a handler for an XML file, but it just
happens to have different side-effects. The main caveat with this
type of set-up, of course, is that it cannot symmetrically export
(and then re-import) the configuration, and it is more difficult to
re-use.

*importVarious* looks as follows:

::

    from StringIO import StringIO...def setupPlugins(portal, out):    """Install and prioritize the project local-role PAS plug-in.    """    ...def setupPortalFactory(portal, out):    """Add borg types to portal_factory    """    ...def addProjectPlacefulWorkflowPolicy(portal, out):    """Add the placeful workflow policy used by project spaces.    """    ....def importVarious(context):    """    Import various settings.    Provisional handler that does initialization that is not yet taken    care of by other handlers.    """    site = context.getSite()    out = StringIO()    setupPlugins(site, out)    setupPortalFactory(site, out)    addProjectPlacefulWorkflowPolicy(site, out)    logger = context.getLogger("borg")    logger.info(out.getvalue())

We set up the PAS plugins, register our types with
*portal\_factory*and add a placeful workflow policy. The exact code
to perform each of these steps is not listed here to save space,
but they use the same techniques you would use in an *Install.py*
file. Note that the *portal\_factory* setup is available in a more
friendly XML format in Plone 2.5.1 and later, which was released
after b-org.

GenericSetup without portal\_setup
-------------------------------------

When Plone 3.0 arrives, it will make the *Add/Remove Products*
control panel aware of extension profiles, and thus provide a more
user friendly way of performing install using GenericSetup. It will
also support uninstall. Until that time, however, it is possible to
re-use the GenericSetup XML handlers to parse files like
*types.xml*Â  and *workflow.xml* from a regular *Install.py*
installation. We do this in the *charity* example.
When importing, GenericSetup requires a setup environment, and
usually an object to work on. A simple *SetupEnviron* is found in
*charity/Extensions/utils.py*, along with a method called
*updateFTI()* which can take an FTI object and update its settings
based on a *types.xml*-like file. This method takes a module and
the id of an FTI to update, and finds the corresponding file.
It is used in *charity/Extensions/Install.py* as follows:
::

    from Products import charityfrom Products.charity.Extensions.utils import updateFTIdef install(self, reinstall=False):    ...        if not reinstall:        updateFTI(self, charity, 'Department')        updateFTI(self, charity, 'Employee')        updateFTI(self, charity, 'Project')

The relevant files may be found in
*charity/Extensions/setup/types/*.

5.10. Using membrane to provide membership behaviour
====================================================

How b-org uses membrane to let employees be users and departments
be groups

Since version 2.5, the user management infrastructure in Plone has
been replaced by PAS, the Zope Pluggable Authentication Service,
and PlonePAS, a Plone integration layer for this. PAS offers
several advantages over plain user folders, mainly in terms of
flexibility. Unfortunately, it is also more difficult to work with
through-the-web and has a very decentralised API, based on the
notion of plugin components, that can be difficult to understand at
first.

Membrane (or rather, *membrane* with a lowercase m) is a component
first developed by Plone Solutions and later improved by Rob Miller
and others. It is similar to *CMFMember* in that it can turn
content objects into users, although it is less concerned with
replicating existing Plone functionality and more concerned with
making a thin integration layer to plug into. It therefore fits
b-org very well.

Membrane works on Archetypes objects (though theoretically it could
be used with other objects as well). It adds a tool called
*membrane\_tool* which contains a registry of content types that
are member- or group-sources, as well as a special catalog. Using
the Archetypes catalog multiplex, it is able to catalog objects
(which may also be cataloged in *portal\_catalog*) and find them
again based on various interfaces (that is, it catalogs the
interfaces provided by an object). membrane provides a number of
PAS plug-ins that will search this catalog when looking for users
and delegate to the content objects (or rather, adapters on the
content object) for obtaining user information, performing
authentication and so on.

Registering with membrane
---------------------------

*membrane\_tool* contains an API for registering content types as
membership providers, but the easiest option is to use a
GenericSetup profile (see the section on GenericSetup for the full
story). In *profiles/default/membrane\_tool.xml*, you will find:
::

    <?xml version="1.0"?><object name="membrane_tool" meta_type="MembraneTool">  <membrane-type name="Department">    <active-workflow-state name="active" />  </membrane-type>  <membrane-type name="Employee">    <active-workflow-state name="active" />  </membrane-type>  <membrane-type name="Project">    <active-workflow-state name="published" />    <active-workflow-state name="private" />  </membrane-type></object>

This registers the three content types (by their portal type), and
specifies the workflow states in which they are "active" as member
and group sources.

Applying marker interfaces
-----------------------------

When looking for content objects that provide group and member
information, membrane will use a number of marker interfaces that
indicate support for various types of behaviour. These are
implemented by the three content type classes.
In *content/department.py*, you will find:
::

    from Products.membrane.interfaces import IPropertiesProvider...class Department(ExtensibleSchemaSupport, BaseFolder):    """A borg department.    Departments can contain other employees.    """    implements(IDepartmentContent, IPropertiesProvider)

All this means is that the Department's schema is capable of
providing properties to PAS. Properties (normally related to users,
but groups can have properties as well) are just metadata about the
user or group. Membrane supports as PAS properties plugin that will
look for Archetypes schema fields with *member\_property=True* set
and report these back as user properties. Although *Department*
does not use any such properties at the moment, we add this marker
so that extension modules that use the schema extension mechanism
can benefit from this.
The equivalent setup for Employees, in *content/employee.py*, is a
little more interesting.
::

    from Products.membrane.interfaces import IUserAuthProviderfrom Products.membrane.interfaces import IPropertiesProviderfrom Products.membrane.interfaces import IGroupsProviderfrom Products.membrane.interfaces import IGroupAwareRolesProvider...class Employee(ExtensibleSchemaSupport, BaseContent):    """A borg employee.    Employees are also users.    """    implements(IEmployeeContent,               IUserAuthProvider,               IPropertiesProvider,               IGroupsProvider,               IGroupAwareRolesProvider,                IAttributeAnnotatable)

Here, we are saying that:

-  An Employee can be used as a source of authentication (i.e. as a
   user), since it is marked with *IUserAuthProvider*. Note that the
   actual authentication is performed by a different adapter.
-  An Employee can provide user properties to PAS via membrane,
   following *IPropertiesProvider*.
-  An Employee can be part of a group, because of
   *IGroupsProvider*.
-  An employee can be given roles. There is an *IRolesProvider*
   interface that we cold use for basic role awareness. The
   *IGroupAwareRolesProvider* is a sub-interface that will cause
   membrane to also look at the user's groups.

The *IAttributeAnnotatable* interface is part of Zope 3's
annotations framework, discussed in a later section.
Projects does not require any particular marker interfaces.

Providing membership behaviour
--------------------------------

When membrane looks for objects to provide membership-related
behaviour, it will not only look for objects directly providing a
particular interface, but also for objects that can be *adapted to*
that interface. For example, the presence of the interface *IGroup*
informs membrane that an object can act as a group, and contains
methods that describe the members of that group.
Of course, we could have declared that *Department* implemented
*IGroup* and written these methods directly in the Department
content object. Hopefully you'll agree now that this would not be
optimal, since it mixes the content-object aspect and the
group-behaviour aspect of Department into a single monolithic
object. Instead, we will use an adapter, which also means that if
you require different behaviour in an extension to b-org, you have
only to override the adapter, leaving the core content object
alone.
In *membership/department.py*, you will see:
::

    class Group(object):    """Allow departments to act as groups for contained employees    """    implements(IGroup)    adapts(IDepartmentContent)    def __init__(self, context):        self.context = context    def Title(self):        return self.context.Title()    def getRoles(self):        """Get roles for this department-group.        Return an empty list of roles if the department is in a workflow state        that is not active in membrane_tool.        """        mb = getToolByName(self.context, MEMBRANE_TOOL)        wf = getToolByName(self.context, 'portal_workflow')        reviewState = wf.getInfoFor(self.context, 'review_state')        wfmapper = ICategoryMapper(mb)        categories = generateCategorySetIdForType(self.context.portal_type)        if wfmapper.isInCategory(categories, ACTIVE_STATUS_CATEGORY, reviewState):            return self.context.getRoles()        else:            return ()    def getGroupId(self):        return self.context.getId()    def getGroupMembers(self):        mt = getToolByName(self.context, MEMBRANE_TOOL)        usr = mt.unrestrictedSearchResults        members = {}        for m in usr(object_implements=IMembraneUserAuth.__identifier__,                     path='/'.join(self.context.getPhysicalPath())):            members[m.getUserId] = 1        return tuple(members.keys())

Mostly, this is about examining the Department content object to
find roles (which are listed in an Archetypes field, editable by
the Manager role). When calculating roles, we make sure that we
don't give roles if the Department group-source is actually
disabled (by virtue of its workflow state and the settings in
membrane\_tool). The group title and id are taken from the object
as well.
The most interesting method is *getGroupMembers()*. Here, we
perform a search in the *membrane\_tool* catalog for objects
adaptable to*IMembraneUserAuth*. This interface is the basic
interface in membrane describing things that can act as users -
there is an adapter from *IUserAuthProvider* to
*IMembraneUserAuth*. We restrict this to objects inside the
Department object. The net effect is that all Employee objects
inside the Department are returned.
Now, let's say you had a need for a Department which in addition to
acting as a group for all members inside it, also allowed some
members from other departments to be in that group. In this case,
you could use a schema extender to add a *ReferenceField* to the
schema of Department that allowed the Department owner to reference
other Employees. You would then provide an override adapter,
perhaps subclassing *Products.borg.membership.department.Group* but
overriding *getGroupMembers()* to append the ids of the referenced
users as well as the contained ones ... or instead of, depending on
your needs.
As it happens, Projects also act as groups, with members being
assigned by reference, using two reference fields - one for project
members, and one for project manangers. Here is the equivalent
adapter from *membership/project.py*:
::

    class Group(object):    """Allow projects to be groups for related members and managers    """    implements(IGroup)    adapts(IProjectContent)    def __init__(self, context):        self.context = context    def Title(self):        return self.context.Title()    def getRoles(self):        # The project does not imply any special roles *globally*, although        # the IWorkspace adapter above enables some local roles        return ()    def getGroupId(self):        return self.context.getId()    def getGroupMembers(self):        return [IUserRelated(m).getUserId() for m in                                 self.context.getRefs(PROJECT_RELATIONSHIP) +                                 self.context.getRefs(PROJECT_MANAGER_RELATIONSHIP)]

As may be expected, the membrane adapters for *Employee* are a bit
more involved. They consist of the following:

IUserRelated adapter
    Provides a user id for employees. Note that user ids and user names
    are possibly different when PAS is used: the user id must be
    globally unique; the user name is the named used for logging in.

IUserAuthentication adapter 
    Used to perform actual authentication by validating a supplied
    username and password.

IUserRoles adapter
    Used to determine which roles the particular user is given.

IMembraneUserManagement 
    Used by membrane and Plone's UI to deal with changes to the user,
    such as the adding of a new user (not implemented here, since we

All these adapters are found in *membership/employee.py*.
The *IUserRelated* adapter is the simplest, as it simply invokes
the user name. Note that by default, membrane will use the
Archetypes *UID()* function as the user id. This is sensible, but
unfortunately Plone's UI (and that of third party products) is not
always aware of the distinction between user id and user name.
Ideally, only the user name would ever be displayed, the user id
being an internal concept, but in practice you may end up with
things like member folder names that are long, unfriendly UID
strings. Sometimes this may even be unavoidable in the general
case, because it's possible that two different sources of users
could use the same user name for two different user ids! For the
purposes of b-org, however, we assume user names are unique and
well-defined. The adapter is therefore quite trivial:
::

    class UserRelated(object):    """Provide a user id for employees.    The user id will simply be the id of the member object. This overrides the    use of UIDs    """    implements(IUserRelated)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def getUserId(self):        return self.context.getId()

The id of the content object that represents the employee is used
as the user id. This is also used as the user name, as defined in
the *IUserAuthentication* adapter:
::

    class UserAuthentication(object):    """Provide authentication against employees.    """    implements(IUserAuthentication)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def getUserName(self):        return self.context.getId()    def verifyCredentials(self, credentials):        login = credentials.get('login', None)        password = credentials.get('password', None)        if login is None or password is None:            return False        digest = sha(password).digest()        annotations = IAnnotations(self.context)        passwordDigest = annotations.get(PASSWORD_KEY, None)        return (login == self.getUserName() and digest == passwordDigest)

In the *verifyCredentials()* method, the adapter is passed the
login and password as entered by the user in a dict (*credentials*)
and then compares those to the values stored on its context (the
Employee content object). The password is stored as a SHA1 digest
in an annotation to make sure it cannot be read back by examining
the content object - more on this in the section on annotations. Be
aware also that the *IUserAuthentication* adapter is called on
every request after a user is logged in and can deny access for
whatever reason by returning non-True. This means that it is
important that the method is as efficient as possible - expensive
database lookups, for example, are probably not a good idea here!
The *IUserRoles* adapter is trivial. Roles are stored on the
content object in a field that is editable only by managers. Of
course, we could have picked roles from some other rule if
necessary:
::

    class UserRoles(object):    """Provide roles for employee users.    Roles may be set (by sufficiently privilged users) on the user object.    """    implements(IUserRoles)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def getRoles(self):        return self.context.getRoles()

The *getRoles()* method returns an iterable of strings representing
applicable roles. Note that depending on group membership (and the
*IGroupAwareRolesProvider* marker as described above) and local
roles the user may in fact have more roles than what this method
returns! The *IUserRoles* interface is concerned only with global
roles intrinsic to the user.
Finally, we have the *IMembraneUserManagement* adapter. This lets
membrane know what to do when it is asked by Plone's UI to add,
edit or remove users. In particular, the *doChangeUser()* method
enables the *PasswordResetTool* to do its magic. Note that we have
not implemented *doAddUser()*, because there is no well-defined
global policy for where the actual *Employee* content object should
be added! Recently membrane has gained some functionality whereby a
site-local utility providing *IUserAdder*** from membrane can be
queried for this policy. That may be useful for b-org extension
products, but b-org is still not in a position to make a general
policy for this, so it is not implemented out of the box.
::

    class UserManagement(object):    """Provides methods for adding deleting and changing users    This is an implementation of IUserManagement from PlonePAS    """    implements(IMembraneUserManagement)    adapts(IEmployeeContent)    def __init__(self, context):        self.context = context    def doAddUser(self, login, password):        """This can't be done unless we have a canonical place to store users        some implementations may wish to define one and implement this.        """        raise NotImplementedError    def doChangeUser(self, login, password, **kw):        self.context.setPassword(password)        if kw:            self.context.edit(**kw)    def doDeleteUser(self, login):        parent = aq_parent(aq_inner(self.context))        parent.manage_delObjects([self.context.getId()])

That's it! Through these adapters, the three b-org content types
are able to act as sources of groups and users. Hopefully, you will
appreciate the flexibility of the separation of concerns into
adapters for things like editing user properties, determining user
id, calculating roles and performing authentication. If you extend
b-org, you can provide a more specific adapter to any of the above
interfaces to customise the membership behaviour.

5.11. Writing a custom PAS plug-in
==================================

Projects require that members are given particular local roles
within a project space. This is achieved using a custom PAS
plug-in.

PAS was introduced in the previous section on *membrane*. Truth be
told, it can be a bit of a jungle of plug-ins and delegation
because it is so very generic. Luckily, Plone (and membrane) takes
care of most of the complexity for us. Sometimes, however, it is
desirable to influence the authentication and role management at a
lower level.

Workspace adapters
----------------------

b-org ships with a bit of framework, adapted from some similar code
in an unreleased version of *teamspace* by Wichert Akkerman, which
can provide local roles in a "workspace" - in this case a Project.
It relies on an adapter to the *IWorkspace* interface to determine
the mapping of users and roles in the particular context. Before
showing how this plug-in is written and registered, however, let's
look at how it is used by a Project.
In *membership/project.py* you will find:
::

    class LocalRoles(object):    """Provide a local role manager for projects    """    implements(IWorkspace)    adapts(IProjectContent)    def __init__(self, context):        self.context=context    def getLocalRoles(self):        project = IProject(self.context)        roles = {}        for m in project.getManagers():            roles[m.id] = ('Manager',)        for m in project.getMembers():            if m.id in roles:                roles[m.id] += ('TeamMember',)            else:                roles[m.id] = ('TeamMember',)        return roles    def getLocalRolesForPrincipal(self, principal):        r = self.getLocalRoles()        return r.get(principal, ())

This queries the lists of managers and members assigned (by
reference) to the project and specifies that both managers and
members should get the role *TeamMember* and managers should also
get the role *Manager*.
As it turns out, this behaviour is also useful in Departments,
which can be given one or more department managers by reference.
The idea is that department managers should be allowed to add and
remove Employees within that Department (recall that *Department*
is a folderish container for *Employee* objects). The analogous
adapter in *membership/department.py* reads:
::

    class LocalRoles(object):    """Provide a local role manager for departments    """    implements(IWorkspace)    adapts(IDepartmentContent)    def __init__(self, context):        self.context = context    def getLocalRoles(self):        project = IDepartment(self.context)        roles = {}        for m in project.getManagers():            roles[m.id] = ('Manager',)        return roles    def getLocalRolesForPrincipal(self, principal):        r = self.getLocalRoles()        return r.get(principal, ())

Thus, a container wanting to use the PAS plug-in we're about to see
to manage local roles only need to be adaptable to *IWorkspace*. In
fact, this whole machinery ought to be factored out into a separate
component, possibly sharing code to *teamspace*, another product
which provides similar functionality. Mostly, this is down to
laziness - creating another product (with all its boilerplate) and
managing another dependency in the *Products* folder seemed too
onerous when b-org was being developed. Hopefully, with Zope
2.10/Plone 3.0 and a growing preference for plain-Python packages
and "eggs", it will seem a little less of an obstacle to split
products up into multiple smaller pieces. So much for making
excuses.

The plug-in
--------------

The PAS plug-in that uses the *IWorkspace* interface can be found
in *pas/localrole.py*. It looks like this:
::

    # Borrowed from Project pasification branch - written primarily by# Wichert Akkerman and Copyright Amaze Internet Services# This module is releasd under the Zope Public Licensefrom sets import Setfrom Globals import InitializeClassfrom Acquisition import aq_inner, aq_chain, aq_parentfrom AccessControl import ClassSecurityInfofrom Products.PageTemplates.PageTemplateFile import PageTemplateFilefrom Products.PluggableAuthService.utils import classImplementsfrom Products.PluggableAuthService.plugins.BasePlugin import BasePluginfrom Products.PlonePAS.interfaces.plugins import ILocalRolesPluginfrom Products.borg.interfaces import IWorkspacemanage_addWorkspaceLocalRoleManagerForm = PageTemplateFile(        "../zmi/WorkspaceLocalRoleManagerForm.pt", globals(),        __name__="manage_addProjectRoleManagerForm")def manage_addWorkspaceLocalRoleManager(dispatcher, id, title=None, REQUEST=None):    """Add a WorkspaceLocalRoleManager to a Pluggable Authentication Services."""    plrm = WorkspaceLocalRoleManager(id, title)    dispatcher._setObject(plrm.getId(), plrm)    if REQUEST is not None:        REQUEST.RESPONSE.redirect(                '%s/manage_workspace?manage_tabs_message=WorkspaceLocalRoleManager+added.'                % dispatcher.absolute_url())class WorkspaceLocalRoleManager(BasePlugin):    meta_type = "Workspace Roles Manager"    security  = ClassSecurityInfo()    def __init__(self, id, title=None):        self.id = id        self.title = title    #    # ILocalRolesPlugin implementation    #    security.declarePrivate("getRolesInContext")    def getRolesInContext(self, user, object):        roles = []        uid = user.getId()        obj, workspace = self._findWorkspace(object)        if workspace is not None:            if user._check_context(obj):                roles.extend(workspace.getLocalRolesForPrincipal(uid))        return roles    security.declarePrivate("checkLocalRolesAllowed")    def checkLocalRolesAllowed(self, user, object, object_roles):        roles = []        uid = user.getId()        obj, workspace = self._findWorkspace(object)        if workspace is not None:            if not user._check_context(obj):                return 0            roles = workspace.getLocalRolesForPrincipal(uid)            for role in roles:                if role in object_roles:                    return 1        return None    security.declarePrivate("getAllLocalRolesInContext")    def getAllLocalRolesInContext(self, object):        rolemap = {}        obj, workspace = self._findWorkspace(object)        if workspace is not None:            localRoleMap = workspace.getLocalRoles()            for (principal, roles) in localRoleMap.items():                rolemap.setdefault(principal, Set()).update(roles)        return rolemap    # Helper methods    security.declarePrivate("_findWorkspace")    def _findWorkspace(self, object):        """Find the first workspace, if any, in the acquistion chain of this        object. Returns a tuple obj, workspace where workspace is the adapted        IWorkspace.        """        for obj in self._chain(object):            workspace = IWorkspace(obj, None)            if workspace is not None:                return obj, workspace        return None, None    security.declarePrivate("_chain")    def _chain(self, object):        """Generator to walk the acquistion chain of object, considering that it         could be a function.        """        # Walk up the acquisition chain of the object, to be able to check        # each one for IWorkspace.        # If the thing we are accessing is actually a bound method on an        # instance, then after we've checked the method itself, get the        # instance it's bound to using im_self, so that we can continue to         # walk up the acquistion chain from it (incidentally, this is why we         # can't juse use aq_chain()).        context = aq_inner(object)        while context is not None:            yield context            funcObject = getattr(context, 'im_self', None)            if funcObject is not None:                context = aq_inner(funcObject)            else:                # Don't use aq_inner() since portal_factory (and probably other)                # things, depends on being able to wrap itself in a fake context.                context = aq_parent(context)classImplements(WorkspaceLocalRoleManager, ILocalRolesPlugin)InitializeClass(WorkspaceLocalRoleManager)

On first glance, there is quite a lot going on here, but it is not
so hard to understand. First, we define a good old-fashioned Zope 2
factory and ZMI add form. This is good practice, because PAS
plug-ins can be managed via *acl\_users* in the ZMI. If you find
yourself wandering there, however, remember to bring a torch and
keep a trail of breadcrumbs to find your way out. A backup wouldn't
hurt either if you try to change things. It is, unfortunately, not
the most intuitive of interfaces.
We will see how the plug-in is registered and activated in a
moment, but first notice that the plug-in implements an interface,
*ILocalRolesPlugin*,Â  which is defined by PlonePAS, the
PAS-in-Plone integration layer. This defines methods that will be
called by the PAS machinery to determine, in this case, local
roles. Note that this is *not* an adapter (perhaps it would have
been if PAS had been invented in Zope 3, though Zope 3 has its own
authentication machinery that is evolved from PAS and works
slightly differently). When created, the *ProjectLocalRoleManager*
is an Zope 2 object that lives in the ZODB in *acl\_users*.
The methods of the *ILocalRolesPlugin* interface are fairly
self-explanatory in purpose. They allow PAS to extract the local
roles for a particular user in a particular context
(*getRolesInContext()*), to check whether a user in fact has one of
the roles required to access a particular method attribute in a
particular context (*checkLocalRolesAllowed()*), and to get a map
of users-to-roles in a particular context.
The complex parts are, as often is the case, concerned with
acquistion. The helper method *\_findWorkspace()* attempts to walk
up the object hierarchy to find the first possible *IWorkspace* (it
will only consider one) to get hold of the appropriate *IWorkspace*
adapter that is then used to determine the actual roles that apply,
as above. Without walking up the content hierarchy, it would not be
possible to let the local roles of a particular project apply when
in the context of a piece of content *inside* that project (i.e. a
sub-object of the folderish *Project* object). There is some
reasonably hairy acqusition-juggling going on in the \_*chain()*
method to return this chain as a generator. The hairiness comes
from the fact that the thing that is being checked may in fact be a
method that is being accessed, and aqusition chains can get
themselves in all kinds of knots, especially when Five is in the
mix.
Lastly, we need to declare a *ClassSecurityInfo* and call
*InitializeClass* to get Zope 2 to play ball.

Registering the plug-in
--------------------------

To be able to use this plug-in, we must first register it with PAS.
This is done when the product is loaded, in *borg/\_\_init\_\_.py*:
::

    from Products.PluggableAuthService import registerMultiPlugin...from pas import localrole...registerMultiPlugin(localrole.WorkspaceLocalRoleManager.meta_type)def initialize(context):    context.registerClass(localrole.WorkspaceLocalRoleManager,                          permission = AddUserFolders,                          constructors = (localrole.manage_addWorkspaceLocalRoleManagerForm,                                          localrole.manage_addWorkspaceLocalRoleManager),                          visibility = None)    ...

This is similar to how CMF content types are initialised with
*ContentInit().initialize()* and *context.registerClass().* In
other words, copy-and-paste and the less you know the happier you
will be.
By registering the plug-in, we could now ask our users to
instantiate a *Workspace Roles Manager*within *acl\_users*....
er... somwhere. Like we said - not necessarily obvious. Better to
do it once, in the setup code for b-org. Please refer to the
section on GenericSetup to learn how b-org is actually installed,
but notice that the relevant code is in *setuphandlers.py*:
::

    from Products.CMFCore.utils import getToolByNamefrom Products.PlonePAS.Extensions.Install import activatePluginInterfacesfrom config import LOCALROLES_PLUGIN_NAME...def setupPlugins(portal, out):    """Install and prioritize the project local-role PAS plug-in.    """    uf = getToolByName(portal, 'acl_users')    borg = uf.manage_addProduct['borg']    existing = uf.objectIds()    if LOCALROLES_PLUGIN_NAME not in existing:        borg.manage_addWorkspaceLocalRoleManager(LOCALROLES_PLUGIN_NAME)        print >> out, "Added Local Roles Manager."        activatePluginInterfaces(portal, LOCALROLES_PLUGIN_NAME, out)

All we do here is get hold of the factory dispatcher for the user
folder (from *manage\_addProduct*, which has something to do with
that *registerClass* call for the *WorkspaceLocalRoleManager* seen
in the previous code example, but like we said, it's dont-ask,
don't-tell) and if it is not there already, we create an instance
of the plugin using the factory. We then need to activate it so
that it actually takes effect. *out* is a StringIO output stream
used for logging.

5.12. Placeful workflow
=======================

b-org uses CMFPlacefulWorkflow, which ships with Plone 2.5, to
manage the workflow of content objects inside a project.

Placeful workflows are based on the concept of policies. You can
think of a policy as a mapping of workflows to types, in the same
way as you could control from the *portal\_workflow* tool. Policies
are created, normally by copying an existing policy (possibly the
default, global policy), and then applied to a context. In Plone,
this can be done using the *policy*option in the *state* menu.

Placeful workflows are used in b-org Projects. Inside a project,
project members should have elevated view and modify permissions
over content. This is achieved using the following technique:


-  A new role *TeamMember* is made available within any Project*.*
-  A custom workflow, *borg\_project\_default\_workflow* is a
   customisation of the default Plone workflow that has a simplified
   set of states and actions, and is aware of the *TeamMember* role.
-  A placeful workflow policy sets the default workflow, as well as
   the workflow for folders, to this one.
-  When a Project is created, this placeful workflow policy is
   enabled for the project.

The custom workflow is defined using *GenericSetup*, in
*profiles/default/workflows/borg\_project\_default\_workflow/definition.xml*.
You can of course install your own workflow if necessary. The
workflow policy is set up in the *importVarious* setup step, in
*setuphandlers.py*:

::

    from Products.CMFCore.utils import getToolByNamefrom config import LOCALROLES_PLUGIN_NAME, PLACEFUL_WORKFLOW_POLICY...def addProjectPlacefulWorkflowPolicy(portal, out):    """Add the placeful workflow policy used by project spaces.    """    placeful_workflow = getToolByName(portal, 'portal_placeful_workflow')    if PLACEFUL_WORKFLOW_POLICY not in placeful_workflow.objectIds():        placeful_workflow.manage_addWorkflowPolicy(PLACEFUL_WORKFLOW_POLICY,                                                    duplicate_id='portal_workflow')        policy = placeful_workflow.getWorkflowPolicyById(PLACEFUL_WORKFLOW_POLICY)        policy.setTitle('[borg] Project content workflows')        policy.setDefaultChain(('borg_project_default_workflow',))        policy.setChainForPortalTypes(('Folder', 'Large Plone Folder',),                                       ('borg_project_default_workflow',))

Again, you could add a different policy if you needed different
settings.

Finally, we apply the policy when a project is created. We will see
how this is set up when events are covered in the next section, but
the relevant code is in *events/project.py*:

::

    from zope.interface import implementsfrom zope.component import getUtilityfrom Products.CMFCore.utils import getToolByNamefrom Products.borg.config import PLACEFUL_WORKFLOW_POLICYfrom Products.borg.interfaces import ILocalWorkflowSelectionclass DefaultLocalWorkflowSelection(object):    """Select the default local workflow policy.    Local adapters or overrides may supercede this.    """    implements(ILocalWorkflowSelection)    workflowPolicy = PLACEFUL_WORKFLOW_POLICYdef addLocalProjectWorkflow(ob, event):    """Apply the local workflow for project spaces when a project is added.    """    # Add the TeamMember role if necessary    if 'TeamMember' not in ob.validRoles():        # Note: API sucks :-(        ob.manage_defined_roles(submit='Add Role',                                REQUEST={'role': 'TeamMember'})    # Find out which workflow to use - this is looked up as a utility so    # that other components can override it.    workflowSelection = getUtility(ILocalWorkflowSelection, context=ob)    # Set the placeful (local) workflow    placeful_workflow = getToolByName(ob, 'portal_placeful_workflow')    ob.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()    config = placeful_workflow.getWorkflowPolicyConfig(ob)    config.setPolicyBelow(policy=workflowSelection.workflowPolicy)

Here, the local role is added to the newly created project instance
(it is not made global so as not to pollute the global roles list),
and the policy is associated with the contents of the (folderish)
project object.

Note that we do not hard-code the name of the workflow policy!
Instead, we ask a utility called *ILocalWorkflowSelection*. This
could be overridden using a local utility, but the global one
references the policy created above, as defined in
*DefaultLocalWorkflowSelection*. This utility is registered in
*events/configure.zcml* as follows:

::

      <utility provides="..interfaces.ILocalWorkflowSelection"           factory=".project.DefaultLocalWorkflowSelection" />

5.13. Sending and handling events
=================================

Events is undoubtedly one of the most useful things that Zope 3
brings to the Zope 2 world. Here's how b-org uses them.

In the previous section, you saw how an event handler was used to
apply a placeful workflow policy to newly created projects. This
pattern is quite powerful - instead of needing to subclass
*Project* just to add something to *at\_post\_create\_script()* or
*initializeArchetype()*, say, you simply register an appropriate
event handler. This pattern can of course apply to other
situations, such as when objects are modified, deleted, added to a
container, or on any other type of event that may occur in your
system. Events are synchronous, so when code emits an event, it
will block until all event handlers are finished.

Recall the event handler for adding projects. It can be found in
*events/project.py* and has the following signature:

::

    def addLocalProjectWorkflow(ob, event):
        ...

The first argument is the object the event was fired on, the second
is an instance of the event itself. In fact, this two-part event
dispatcher is a special case of events described with
*IObjectEvent* and its sub-interfaces. Internally, Zope 3 catches
all *IObjectEvent*s and re-dispatches the event based on the object
that is passed along the event instance. The registration for the
event handler in *events/configure.zcml* looks like this:

.. code-block:: xml

    <subscriber 
        for="..interfaces.IProjectContent
             zope.app.container.interfaces.IObjectAddedEvent"
        handler=".project.addLocalProjectWorkflow" />

Note that there are two interfaces the subscriber is registered
*for* - the object type and the event type. These must be separated
by whitespace, though a newline like above is customary. This is
the same syntax that is used to explicitly define multi-adapters
(if you are not using the *adapts()* syntax in an adapter class) -
in fact, the events machinery uses the adapter registry internally
to map subscribers to events when they are fired.

A more general-case event can be found in *events/employee.py*,
which takes care of assigning ownership of an *Employee* object to
the user that is tied to that employee. The code is borrowed and
adapted from *PloneTool*, but notice the signature which only
includes the event:

::

    def modifyEmployeeOwnership(event):
        """Let employees own their own objects.
        Stolen from Plone and CMF core, but made less picky about where
        users are found.
        """

The registration in *events/onfigure.zcml*is similar to the one
above, but only uses one *for* interface:

.. code-block:: xml

     <subscriber
         for="..interfaces.IEmployeeModifiedEvent"
         handler=".employee.modifyEmployeeOwnership" />

Sending custom events
------------------------

You will notice that the *IEmployeeModifiedEvent* is a custom
event. In Plone 3.0 (or rather, Archetypes 1.5) this won't be
necessary, because Archetypes will take care of sending an event
derived from *IObjectModifiedEvent*, which in turn derives from
*IObjectEvent* and thus is subject to the same registration as the
*IObjectAddedEvent* that includes the object type and the event
type. For now, though, we need to send the event ourselves.

The event is described by an interface in
*interfaces/employee.py*:

::

    from zope.interface import Interface, Attribute...

    class IEmployeeModifiedEvent(Interface):
        """An event fired when an employee object is saved.
        """
        context = Attribute("The content object that was saved.")

The implementation is trivial, and can be found in
*content/employee.py*:

::

    from zope.interface import implements...
    from Products.borg.interfaces import IEmployeeModifiedEvent...
    
    class EmployeeModifiedEvent(object):
        """Event to notify that employees have been saved.
        """
        implements(IEmployeeModifiedEvent)
        
        def __init__(self, context):
            self.context = context

It is of course the event *class* that we instantiate and send,
whilst we register the event handler for the event *interface*.
This means that we could provide alternative implementations for
the same event interface, if need be. It also means that event
handlers subscribed for a parent interface will be invoked for
events that provide a sub-interface.
Sending the event is very simple. In the definition of *Employee*
in *content/employee.py*, we have:

::

    from zope.event import notify...
    
    class Employee(ExtensibleSchemaSupport, BaseContent):
    ...

        security.declarePrivate(permissions.View, 'at_post_create_script')
        def at_post_create_script(self):
        """Notify that the employee has been saved.
        """
        notify(EmployeeModifiedEvent(self))

        security.declarePrivate(permissions.View, 'at_post_edit_script')
        def at_post_edit_script(self):
        """Notify that the employee has been saved.
        """
        notify(EmployeeModifiedEvent(self))

We construct an event instance and parameterise it with the right
object (i.e. self) before sending it with *notify()*, all on one
line.

5.14. Annotations
=================

Annotations are an elegant solution to the "where do I store this?"
problem, and are used in many Zope 3 applications.

It is often useful to be able to attach information to an object
even if you don't have control over that object's type and schema.
For example, a tagging solution may attach a list of tags to an
object, or a notification tool may want to add a list of
subscribers on a per-object basis. This is known in Zope 3 as
"annotations".

Annotations work like this:

-  A marker interface, normally *IAttributeAnnotatable* is applied
   to the class or object that is to be annotated. This particular
   marker means that annotations are stored in a persistent dict
   called *\_\_annotations\_\_* that is added to the object, though
   this should be considered an implementation detail.
-  An adapter exists from *IAttributeAnnotable*to *IAnnotations*.
   If you need a different annotation regime (e.g. one that stores the
   values keyed by object id in some local utility) you could provide
   a different adapter to *IAnnotations*.
-  The code that wishes to annotate an object will adapt it to
   *IAnnotations*. The annotations adapter acts like a dict.
   Conventionally, each package that uses annotations will store all
   its (arbitrary) information under a particular key in that dict.
   The key name is normally the same as the name of the package. This
   is mainly to avoid conflicts between different packages annotating
   a particular object.

In b-org, we don't have quite the same need for annotating objects
from other parts of Plone, but we use annotations to store users'
passwords. This ensures that they cannot be accessed
through-the-web (since Zope 2 won't publish the
*\_\_annotations\_\_* dict, as it begins with an underscore) and
keeps passwords out of the way. Strictly speaking, this is probably
overkill since the password is also hashed using the SHA1 one-way
hasing algorithm, but that never stopped anyone before.

First, look at the definition of the *Employee* class in
*content/employee.py*:

::

    from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations...

    class Employee(ExtensibleSchemaSupport, BaseContent):
    ...

        implements(IEmployeeContent,
            IUserAuthProvider,
            IPropertiesProvider,
            IGroupsProvider,
            IGroupAwareRolesProvider,
            IAttributeAnnotatable)

Here, we explicitly say that Employee is attribute annotatable. Of
course, this requires control over the class. If you are trying to
annotate another type that isn't already marked as annotatable, you
may be able to add the marker interface using *classProvides()* or
*directlyProvides()* from *zope.interface*, or use the ZCML
*<implements />* directive. You need to be a bit careful, though,
since the thing you are annotating should probably be persistent.
You should also be polite - you're stuffing your own information
onto someone else's object. Try not to break it.

Further down in *content/employee.py*, you will see the annotation
being set:

::

    security.declareProtected(permissions.SetPassword, 'setPassword')
    def setPassword(self, value):
    if value:
        annotations = IAnnotations(self)
        annotations[PASSWORD_KEY] = sha(value).digest()

PASSWORD\_KEY comes from *config.py*, and is simply a string. The
digest is verified in *membership/employee.py*, in the
*IUserAuthentication* adapter:

::

    class UserAuthentication(object):
        """Provide authentication against employees.
        """

        implements(IUserAuthentication)
        adapts(IEmployeeContent)
        def __init__(self, context):
            self.context = context

        def getUserName(self):
            return self.context.getId()

        def verifyCredentials(self, credentials):
            login = credentials.get('login', None)
            password = credentials.get('password', None)
            if login is None or password is None:
                return False
            digest = sha(password).digest()
            annotations = IAnnotations(self.context)
            passwordDigest = annotations.get(PASSWORD_KEY, None)
            return (login == self.getUserName() and digest == passwordDigest)

That's all there is to it. We get an *IAnnotations* adapter, and
then look up the *PASSWORD\_KEY* to find the digest. The
annotations adapter has the same contract as a Python dict, so we
can use functions like *get()* and *setdefault()*.

5.15. Zope 3 Views
==================

One of the nicest things that Zope 3 brought us is a way to manage
view logic.

In Zope 2, a view (be that a view of a content object, or a more
standalone template) typically consists of a Zope Page Template
that pulls in data from its context. The problem is that
non-trivial templates usually require some kind of "view logic" or
"display logic". People tend to put these in a few places:

-  Complex *python:* expressions in the ZPT. This is bad because it
   makes your templates hard to understand, and because there is a
   limit to what you can do with one-line Python expressions.
-  External Python Scripts in a skin layer that get acquired in the
   page template, e.g. *here/calculateDate.* This is bad because it is
   cumbersome to create a new file for something which may be quite
   trivial, because all such scripts are part of a global namespace
   (and thus there may be conflicts between two different scripts with
   the same name), and also because Python scripts in the skin layers
   (and *python:* expressions) are slower than filesystem Python code
   and more restricted.
-  A custom tool that provides some necessary functionality. This
   is bad because a tool is a singleton, so you will probably need to
   explicitly pass around a context. Tools are also part of that same
   global namespace (by way of acquisition from the portal root), and
   are a hassle to create and install.
-  Methods on the context content object (where applicable). This
   is bad because it mixes presentation logic and the model (the
   schema) and storage logic. This often leads to an explosion of
   methods on each content type that are highly specific to a
   particular template. This pattern also requiers that you have the
   ability to add new methods to the content type class, even if you
   are just adding a new view template for it.

As usual, these problems indicate a lack of separation of concerns.
Zope 3's answer is a view - a class (typically) which may be
associated with a template.

Views are multi-adapters
---------------------------

You will often hear that views are named multi-adapters of a
context and a request. In fact, the concept of a multi-adapter
originated in the need for views. For most practical purposes, you
can forget about this - it is an implementation detail. However,
you may sometimes need to look up views yourself, which can be done
using:

::

    from zope.component import getMultiAdapter
    myView = getMultiAdapter((context, request), name='my_view')

More importantly, you need to know that to access the context the
view is operating on inside that view, you can use *self.context*,
and to access the request (including form variables submitted as
part of that request, if applicable), using *self.request*.

Explicitly acquiring views
---------------------------

One of the easiest ways of using views with existing code is to
make page templates in a skin layer as you normally would, and then
acquire a view object that is used for rendering logic. One of the
main reasons for using this approach is that it allows page
templates to be customised using the normal skin layer mechanism.
This is approach is used extensively in Plone 2.5. Here's an
example from the "recent" portlet, starting with
*portlet\_recent.pt*:

.. code-block:: xml

    ...
    <tal:recentlist tal:define="view context/@@recent_view;
                                results view/results;">
        ...
        <tal:items tal:repeat="obj results">
            ...    
        </tal:items>
        ...
    </tal:recentlist>

The important line here is context*/@@recent\_view*. This will look
up a view named *recent\_view* relative to the current context
(*context* in page templates is a now-preferred alias for the
*here* variable that was used before - *here* still works in Zope 2
templates, but is gone in Zope 3).

This view is defined by a class and a ZCML directive. The ZCML
directive looks like this:

.. code-block:: xml

    <browser:view
          for="*"
          name="recent_view"
          class=".portlets.recent.RecentPortlet"
          permission="zope.Public"
          allowed_attributes="results"
          />

Actually, this is not exactly what's in the file in Plone, since
Plone is working around a few Zope 2.8 issues, but basically, this
says that the view is available on all types of contexts
(*for="\*"* - this could specify a dotted name to an interface if
needed, more on that below), has the name *recent\_view*, is public
(because of the magic permission *zope.Public*) and that when
acquired, the attribute (method) *results* is allowed - more
attributes could be specified separated by whitespace. The class
that is referenced contains the view implementation. Here it is,
again slightly modernised:

::

    from Products.Five.browser import BrowserView
    from Products.CMFCore.utils import getToolByName
    
    from Acquisition import aq_inner
    
    class RecentPortlet(BrowserView):
        """The recent portlet
        """
    
        def results(self):
            """Get the search results
            """
            context = aq_inner(self.context)
            putils = getToolByName(context, 'plone_utils')
            portal_catalog = getToolByName(context, 'portal_catalog')
            typesToShow = putils.getUserFriendlyTypes()
            return self.request.get(
                'items',
                portal_catalog.searchResults(sort_on='modified',
                                             portal_type=typesToShow,
                                             sort_order='reverse',
                                             sort_limit=5)[:5])

The use of *aq\_inner()* on self.context is not strictly necessary
always, but is a useful rule of thumb to make acquisition do what
you expect it to do (this is because the *BrowserView* base class
extends *Acquisition.Explicit*, which causes *self.context* to gain
an acquistion wrapper that can mess with its acqusition chain).

Views with templates
---------------------

Zope 3 does not use views in this way. Instead, you would bind the
template to the browser view explicitly. The main drawback of this
technique is that the template is not present in the
*portal\_skins* tool, and so cannot be customised through-the-web.
This may be possible in future versions of Zope and CMF, but for
now the full-blown view technique is best used when it is not
necessary to customise views through-the-web. Of course, you can
still override view registrations using ZCML on more specific
interfaces or an *overrides.zcml*.

Here is a view for departments in the *charity* example product,
under *charity/browser/configure.zcml.* Notice how this entire XML
file is in the *browser* namespace, and thus it is unnecessary to
prefix each directive with *browser:*

.. code-block:: xml

    <configure xmlns="http://namespaces.zope.org/browser"
               i18n_domain="charity">
    
      <page
          name="charity_department_view"
          for="Products.borg.interfaces.IDepartmentContent"
          class=".department.DepartmentView"
          template="department.pt"
          permission="zope2.View"
          />
          
      ...
      
    </configure>

Here, we explicitly state that this view is only available for
*IDepartmentContent* objects. This means that if you try to invoke
*@@charity\_department\_view* on anything that does not provide
this interface, you will get a lookup error. The view is protected
by the Zope 2*View* permission. Also note that there is no
*allowed\_attributes* (or *allowed\_interface*) attribute here.
This is because the view is not intended to be used by other
templates (if they tried, they would get an *Unauthorized* error
when trying to access any attribute of the view) - all the logic is
in the *department.pt* template.

The *department.pt* template is found in *charity/browser,*the same
directory as the *configure.zcml* file above. You can use relative
paths like *./templates/...* if necessary to point to the template
file on the filesystem. Here is the class:

::

    from Products.Five.browser import BrowserView
    from Products.borg.interfaces import IDepartment
    
    class DepartmentView(BrowserView):
        """A view of a charity department"""
    
        def __init__(self, context, request):
            self.context = context
            self.request = request
        
        def name(self):
            return self.context.Title()
            
        def managers(self):
            return self.context.getManagers()
            
        def details(self):
            return self.context.Description()

And here is the template that uses these methods:

.. code-block:: xml

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          lang="en"
          metal:use-macro="here/main_template/macros/master"
          i18n:domain="charity">
    <body>
    
    <metal:main fill-slot="main">
        
        <div metal:use-macro="here/document_actions/macros/document_actions">
            Document actions (print, rss etc)
        </div>
        
        <h1 class="documentFirstHeading" tal:content="view/name" />
        
        <table class="listing vertical" style="float:right" tal:condition="view/managers">
          <tr>
            <th>Manager(s)</th>
            <td>
              <div tal:repeat="obj view/managers">
                <a href="#" tal:attributes="href obj/absolute_url" tal:content="obj/Title" />
             </div>
            </td>
          </tr>
        </table>
    
        <div tal:content="structure view/details" />
    
        <metal:listing use-macro="here/folder_listing/macros/listing" />
        
        <div class="visualClear"><!----></div>
        
    </metal:main>
    
    </body>
    </html>

Now, you can go to a hypothetical URL
*/mydept/@@charity\_department\_view* to see this view rendered. In
fact, this is set as the *view* and *(Default)* aliases for the
Department content type when *charity* is installed, so the user
will never see this URL.

Views without templates
-------------------------

It is also possible to make views without templates. This is useful
if you need a URL to submit that does some processing. That
processing would normally be done in the *\_\_call\_\_()* method,
as in the hypothetical example below:

.. code-block:: xml

      <browser:view
          name="modify_customer"
          for=".interfaces.ICustomer"
          class=".customer.ModifyCustomerView"
          permission="cmf.ModifyPortalContent"
          />

Now, we could write a form that has *action="@@modify\_customer"*,
which would result in this being called:

::

    class ModifyCustomerView(BrowserView):
        """Modify a customer from a form
        """
    
        def __call__(self):
            name = self.request.form.get('name', None)
            dog = self.request.form.get('dog', None)
    
            self.context.name = name
            self.context.dog = dog
    
            self.request.response.redirect('@@customer_view')

This is obviously a simplified example, but the important thing to
realise is that the view will tend to use *self.context* and
*self.request* to interact with the rest of the portal.

 

5.16. The schema extension mechanism
====================================

How the Archetypes schema extension mechanism in b-org works

Text to follow


