From Scratch or Based on Plone Default?
=======================================

It is perfectly possible to build your own Plone theme completely from
scratch, but you probably won't want to do this.

Based on Plone Default?
-----------------------

In particular, the bells and whistles of the Plone editing interface are
wrapped up as part of the out-of-the box Plone Default, and you'll
probably want to keep these.

The good news is that you can **base** your own theme on Plone Default
and interweave your bits of templates, styles, scripts and components
with what's already there. There are three ways of doing this:

-  with the Skin building block you **customize**\ the Plone Default
   bits (there's a neat way of doing this which ensures you leave the
   Plone Default theme completely intact)
-  with the Components building block you **build your own**, but you
   can **reuse** bits of the Plone Default components in the process
-  with the Configuration you simply **add new**\ directives

There's more good news - the elements of a Plone theme are broken up
into very small parts. Each one can be dealt with independently of the
others, so you can home in on just the bits you want to change.The price
of all this flexibility is that it is sometimes difficult to track down
exactly which bit you want, and things can start to seem complicated.
This manual should help with that.

You can change a great deal of the look and feel just by overwriting
existing CSS styles, or by rewriting some of the existing style sheets.
However, if you want to start moving page elements around or rewriting
some of the XHTML, then you'll need to delve into the templates,
components, and configuration in more detail.

In the end, you're likely to come up with a theme based on Plone Default
(that is, based structurally, not necessarily visually). This will
probably contain

-  your own style sheet; or rewrites of some of the Plone CSS
-  some rearrangement of page elements
-  a few rewrites of some page elements
-  a few 'new' page elements

 


