The Custom Style Sheet and Base Properties
==========================================

You can do a great deal by simply overriding Plone's existing styles.
There's a stylesheet available for just this purpose.

You'll find an empty stylesheet called ploneCustom.css in

-  [your products directory]/CMFPlone/skins/plone\_styles or
-  Site Setup > Zope Management Interface > portal\_skins >
   plone\_styles

This stylesheet is always loaded last on a page, and can be used,
therefore, to override any other styles. There's an excellent and
comprehensive tutorial on this here:

-  `http://plone.org/documentation/tutorial/working-with-css <http://plone.org/documentation/manual/tutorial/working-with-css>`_

 

DTML
----

You'll see that ploneCustom.css has a .dtml extension, and the CSS
inside is wrapped in

::

    /* <dtml-with base_properties> */
     .......
    /* </dtml-with> */

DTML is another Zope templating language, which in this case is deployed
so that particular variables can be picked up from a properties sheet
(base\_properties.props) - for example:

::

    #portal-column-one {
        vertical-align: top;
        width: <dtml-var columnOneWidth missing="16em">;
        border-collapse: collapse;
        padding: 0;
    }

We wouldn't recommend using this technique as it is likely to be phased
out, but it is as well to know that it is there. You can sometimes get
caught out if you're customizing ploneCustom.css and accidentally delete
the top or bottom "dtml-with" statement, or forget to add the .dtml
extension.
