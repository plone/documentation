Macros and Slots
================

Macros
------

So far, you've seen how Page Templates can be used to add dynamic
behavior to individual web pages. Another feature of page templates is
the ability to reuse look and feel elements across many pages.

For example, with Page Templates, you can have a site that has a
standard look and feel. No matter what the "content" of a page, it will
have a standard header, side-bar, footer, and/or other page elements.
This is a very common requirement for web sites, and this is exactly how
Plone works.

You can reuse presentation elements across pages with **macros**. Macros
define a section of a page that can be reused in other pages. A macro
can be an entire page, or just a chunk of a page such as a header or
footer. After you define one or more macros in one Page Template, you
can use them in other Page Templates.

Using Macros
~~~~~~~~~~~~

You can define macros with tag attributes similar to TAL statements.
Macro tag attributes are called **Macro Expansion Tag Attribute Language
(METAL)** statements. Here's an example macro definition:

::

    <p metal:define-macro="copyright">
      Copyright 2008, <em>Foo, Bar, and Associates</em> Inc.
    </p>

This metal:define-macro statement defines a macro named "copyright". The
macro consists of the p element (including all contained elements,
ending with the closing p tag).

Macros defined in a Page Template are stored in the template's *macros*
attribute. You can use macros from other Page Templates by referring to
them through the *macros* attribute of the Page Template in which they
are defined. For example, suppose the *copyright* macro is in a Page
Template called "master\_page". Here's how to use the *copyright* macro
from another Page Template:

::

    <hr />
    <b metal:use-macro="container/master_page/macros/copyright">
      Macro goes here
    </b>

In this Page Template, the b element will be completely replaced by the
macro when Zope renders the page:

::

    <hr />
    <p>
      Copyright 2008, <em>Foo, Bar, and Associates</em> Inc.
    </p>

If you change the macro (for example, if the copyright holder changes)
then all Page Templates that use the macro will automatically reflect
the change.

Notice how the macro is identified by a path expression using the
metal:use-macro statement. The metal:use-macro statement replaces the
statement element with the named macro.

Macro Details
~~~~~~~~~~~~~

The metal:define-macro and metal:use-macro statements are pretty simple.
However there are a few subtleties to using them which are worth
mentioning.

A macro's name must be unique within the Page Template in which it is
defined. You can define more than one macro in a template, but they all
need to have different names.

It should also be noted that, despite the define-macro attribute, the
macro is anyway a regular section of the template; so, when you call the
whole template, the macro section is rendered in the output page just
like any other section in the template. By using the define-macro
attribute you are simply **adding** some sort of "anchor" to that
section, so that you can call it from outside; but you are not changing
anything regarding the behaviour of that same section in the template
itself.

Normally you'll refer to a macro in a metal:use-macro statement with a
path expression. However, you can use any expression type you wish so
long as it returns a macro. For example:

::

    <p metal:use-macro="python:context.getMacro()">
      Replaced with a dynamically determined macro,
      which is located by the getMacro script.
    </p>

In this case the path expression returns a macro defined dynamically by
the getMacro script. Using Python expressions to locate macros lets you
dynamically vary which macro your template uses.

You can use the default variable with the metal:use-macro statement:

::

    <p metal:use-macro="default">
      This content remains - no macro is used
    </p>

The result is the same as using default with tal:content and
tal:replace. The "default" content in the tag doesn't change when it is
rendered. This can be handy if you need to conditionally use a macro or
fall back on the default content if it doesn't exist.

If you try to use the nothing variable with metal:use-macro you will get
an error, since nothing is not a macro. If you want to use nothing to
conditionally include a macro, you should instead enclose the
metal:use-macro statement with a tal:condition statement.

Zope handles macros first when rendering your templates. Then Zope
evaluates TAL expressions. For example, consider this macro:

::

    <p metal:define-macro="title"
       tal:content="template/title">
      template's title
    </p>

When you use this macro it will insert the title of the template in
which the macro is used, not the title of the template in which the
macro is defined. In other words, when you use a macro, it's like
copying the text of a macro into your template and then rendering your
template.

Using Slots
-----------

Macros are much more useful if you can override parts of them when you
use them. You can do this by defining **slots** in the macro that you
can fill in when you use the template. For example, consider a side bar
macro:

::

    <div metal:define-macro="sidebar">
      Links
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/support">Support</a></li>
        <li><a href="/contact">Contact Us</a></li>
      </ul>
    </div>

This macro is fine, but suppose you'd like to include some additional
information in the sidebar on some pages. One way to accomplish this is
with slots:

::

    <div metal:define-macro="sidebar">
      Links
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/support">Support</a></li>
        <li><a href="/contact">Contact Us</a></li>
      </ul>
      <span metal:define-slot="additional_info"></span>
    </div>

When you use this macro you can choose to fill the slot like so:

::

    <p metal:use-macro="container/master_page/macros/sidebar">
      <b metal:fill-slot="additional_info">
        Make sure to check out our <a href="/specials">specials</a>.
      </b>
    </p>

When you render this template the side bar will include the extra
information that you provided in the slot:

::

    <div>
      Links
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/support">Support</a></li>
        <li><a href="/contact">Contact Us</a></li>
      </ul>
      <b>
        Make sure to check out our <a href="/specials">specials</a>.
      </b>
    </div>

Notice how the span element that defines the slot is replaced with the b
element that fills the slot.

Customizing Default Presentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A common use of slot is to provide default presentation which you can
customize. In the slot example in the last section, the slot definition
was just an empty span element. However, you can provide default
presentation in a slot definition. For example, consider this revised
sidebar macro:

::

    <div metal:define-macro="sidebar">
      <div metal:define-slot="links">
      Links
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/support">Support</a></li>
        <li><a href="/contact">Contact Us</a></li>
      </ul>
      </div>
      <span metal:define-slot="additional_info"></span>
    </div>

Now the sidebar is fully customizable. You can fill the links slot to
redefine the sidebar links. However, if you choose not to fill the links
slot then you'll get the default links, which appear inside the slot
definition.

You can even take this technique further by defining slots inside of
slots. This allows you to override default presentation with a fine
degree of precision. Here's a sidebar macro that defines slots within
slots:

::

    <div metal:define-macro="sidebar">
      <div metal:define-slot="links">
      Links
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li><a href="/support">Support</a></li>
        <li><a href="/contact">Contact Us</a></li>
        <span metal:define-slot="additional_links"></span>
      </ul>
      </div>
      <span metal:define-slot="additional_info"></span>
    </div>

If you wish to customize the sidebar links you can either fill the
*links* slot to completely override the links, or you can fill the
*additional\_links* slot to insert some extra links after the default
links. You can nest slots as deeply as you wish.

Combining METAL and TAL
-----------------------

You can use both METAL and TAL statements on the same elements. For
example:

::

    <ul metal:define-macro="links"
        tal:repeat="link context/getLinks">
      <li>
        <a href="link_url"
           tal:attributes="href link/url"
           tal:content="link/name">link name</a>
      </li>
    </ul>

In this case, getLinks is a (imaginary) Script that assembles a list of
link objects, possibly using a Catalog query.

Since METAL statements are evaluated before TAL statements, there are no
conflicts. This example is also interesting since it customizes a macro
without using slots. The macro calls the getLinks Script to determine
the links. You can thus customize your site's links by redefining the
getLinks Script at different locations within your site.

It's not always easy to figure out the best way to customize look and
feel in different parts of your site. In general you should use slots to
override presentation elements, and you should use Scripts to provide
content dynamically. In the case of the links example, it's arguable
whether links are content or presentation. Scripts probably provide a
more flexible solution, especially if your site includes link content
objects.

Whole Page Macros
-----------------

Rather than using macros for chunks of presentation shared between
pages, you can use macros to define entire pages. Slots make this
possible. Here's an example macro that defines an entire page:

::

    <html metal:define-macro="page">
      <head>
        <title tal:content="context/title">The title</title>
      </head>

      <body>
        <h1 metal:define-slot="headline"
            tal:content="context/title">title</h1>

        <p metal:define-slot="body">
          This is the body.
        </p>

        <span metal:define-slot="footer">
          <p>Copyright 2008 Fluffy Enterprises</p>
        </span>

      </body>
    </html>

This macro defines a page with three slots: *headline*, *body*, and
*footer*. Notice how the *headline* slot includes a TAL statement to
dynamically determine the headline content.

You can then use this macro in templates for different types of content,
or different parts of your site. For example here's how a template for
news items might use this macro:

::

    <html metal:use-macro="container/master_page/macros/page">

      <h1 metal:fill-slot="headline">
        Press Release:
        <span tal:replace="context/getHeadline">Headline</span>
      </h1>

      <p metal:fill-slot="body"
         tal:content="context/getBody">
        News item body goes here
      </p>

    </html>

This template redefines the *headline* slot to include the words "Press
Release" and call the getHeadline method on the current object. It also
redefines the *body* slot to call the getBody method on the current
object.

The powerful thing about this approach is that you can now change the
*page* macro and the press release template will be automatically
updated. For example you could put the body of the page in a table and
add a sidebar on the left and the press release template would
automatically use these new presentation elements.

Based on the `Zope
Book <http://www.zope.org/Documentation/Books/ZopeBook/>`_, © `Zope
Corporation <http://www.zope.com/>`_
