How to customise view or edit on archetypes content items
=========================================================

Explains one way to customise the view or edit templates without having
to change the action of an object.

Reasons/Use Cases
-----------------

I usually like to customise as little as possible so that more of my
page templates are just like the plone default templates. I find this
helps when I move to a new version and also makes doing styling using
CSS easier.

Another use case is if I want to generate a form using the schema but I
need it to do different things based on which button is pushed, you can
accomplish this with putting named buttons on the form in combination by
using portal\_formcontroller to override what happens on a submit. E.g.
importing data from CSV, in a seperate schemata I have a
form.button.Import button and on this schemata I only show this button
and the cancel button (instead of save, nex previous etc.) and then I
customise the portal\_formcontroller action (and validation) so
content\_edit (the script that does the saving) goes to a script that
does the importing before going back to the view action.

Archetypes base\_view and base\_edit
------------------------------------

Both of these templates have several macros which are gotten by from
other page templates. They are setup in such a way that they will look
for a template named with the content type for these macros and then
default to the generic archetypes macros. I.e. say you have a content
type 'Newsletter' base\_view looks for a template named
'newsletter\_view' if it finds it and it contains the right macros it
will use those instead of the default 'view\_macros' (found in
'portal\_skins/archetypes' skin folder.

Below is a skeleton example of a custom view template showing the
different things you can customise. See base.pt

::

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"

          lang="en"

          metal:use-macro="here/main_template/macros/master"

          i18n:domain="plone">

    <body>



    <metal:main fill-slot="main">

            <!-- header, H1 with title in it -->

            <metal:header define-macro="header">

            

            </metal:header>

            

            <!-- body macro where all the fields are -->

            <metal:body define-macro="body">

                    

            </metal:body>

            

            <!-- folderlisting that shows sub-objects if there are any -->

            <metal:folderlisting define-macro="folderlisting">

                    

                    

            </metal:folderlisting>

            

            <!-- footer, by line created date etc. -->

            <metal:footer define-macro="footer">

                    

            </metal:footer>

            

    </metal:main>

    </body>

    </html>

Below is an skeleton of a custom edit template:

::

    <html xmlns="http://www.w3.org/1999/xhtml"

          xml:lang="en"

          lang="en"

          xmlns:tal="http://xml.zope.org/namespaces/tal"

          xmlns:metal="http://xml.zope.org/namespaces/metal"

          xmlns:i18n="http://xml.zope.org/namespaces/i18n"

          i18n:domain="plone">



      <metal:head define-macro="topslot">

      </metal:head>

      

      <metal:head define-macro="javascript_head">

      </metal:head>



      <body>

            <!-- header, h1 of Edit <Type>, schemata links and webdav lock message -->

            <metal:header define-macro="header">



            </metal:header>

            

            <!-- typedesription, typeDescription from the content type -->

            <metal:typedescription define-macro="typedescription">



            </metal:typedescription>



            <!-- body, editform , fields, buttons, the default macro 

                 contains a number of slots which usually provide enough

                 ways to customise so often I use that macro and just 

                 fill the slots

            -->

            <metal:body define-macro="body">

                <metal:default_body use-macro="here/edit_macros/macros/body">

                  <!-- inside the fieldset but above all the fields -->

                  <metal:block fill-slot="extra_top">

                  </metal:block>

                  

                  <!-- listing of the fields, usually I won't customise this

                  <metal:block fill-slot="widgets">

                  </metal:block>

                  -->



                  <!-- below the fields above the formControls (hidden fields for refernce stuff is above buttons) -->

                  <metal:block fill-slot="extra_bottom">

                  </metal:block>



                  <!-- within the formControls these are the default previous, next, save, cancel buttons -->

                  <metal:block fill-slot="buttons">

                  </metal:block>



                  <!-- within the formControls a slot for extra buttons -->

                  <metal:block fill-slot="extra_buttons">

                  </metal:block>



                </metal:default_body>

            </metal:body>



            

            <!-- footer, by line created date etc. -->

            <metal:footer define-macro="footer">

            

            </metal:footer>



      </body>



    </html>


See the templates into Products.Archetypes:skins/archetypes for examples
about how does Archetypes work by default: get the field lists, hook up
translation, handle form processing and more. Using them as a base and
customizing only the neccessary bits can make the job much easier than
starting from scratch.

How to do it
------------

Lets say your content type is '**Newsletter**\ '

Steps for View
~~~~~~~~~~~~~~

#. Create a page template (either file system of in ZMI) called
   'newsletter\_view'
#. Use the skeleton and comment out the macros you wish to keep the
   same. I.e. the ones you want to use from view\_macros template (in
   portal\_skins/archetypes)
#. Put your code into the relevant macros/slots.
#. Test and you are done.

Steps for Edit
~~~~~~~~~~~~~~

#. Create a page template called 'newsletter\_edit'
#. Use the skeleton and then comment out the macros you wish to use the
   default for. (from edit\_macros).
#. Put your code into the relevant macros/slots.
#. Test and you are done.

