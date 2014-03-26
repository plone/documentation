Presentation Mode
=======================

Plone comes with the ability to create very simple slideshow
presentations.

Presentation Mode is a special feature of the Page content type. You can
enable Presentation Mode by editing the page, then going to the
**Settings** tab. Notice the Presentation Mode checkbox available there.
Once checked, a link will appear in the view of the page for a user to
view the page in Presentation Mode.

How to Create Slides
--------------------

All the content for a presentation lives on a single page. You do not
need to create a page for each slide. A slide is created when you use
the Heading (h1) class on the page - they effectively indicate to Plone
where you want your slides to be.

You can have as many slides as you want in your presentation. Just add
more Heading (h1) tags to your page and the content between that h1 tag
and the next h1 tag becomes the content of your slide.

How to Format a Slide
---------------------

It is very important to note that the **Normal Paragraph style will not
render any content in the slide**. Slides are meant to display summary
information, not chunks of paragraph text. As such, you must class all
content in each slide with a style other than Normal Paragraph. Examples
of those styles include:

-  Heading (h1)
-  Subheading (h3)
-  Definition list
-  Bulleted list
-  Numbered list
-  Literal
-  Pull-quote
-  Call out
-  Highlight

