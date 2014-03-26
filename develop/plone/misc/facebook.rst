===================================
Facebook integration
===================================

.. admonition:: Description

        How to integrate Facebook to Plone site

.. contents:: :local:

Introduction
--------------

See the add-on

* http://plone.org/products/facebook-like-button

for non-programming integration.

Like button
------------

Here is an example which creates a Like button pointing to the current page.

Page template code:

.. code-block:: html

       <iframe tal:attributes="src string:${view/getFBURL}" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:227px; height:50px;" allowTransparency="true"></iframe>

View code

.. code-block:: python

    import urllib

    ...

    class YourView(BrowserView):

        ...

            def getQuotedURL(self):
                url = self.context.absolute_url()
                url = urllib.quote(url)
                return url

            def getFBURL(self):
                base = "http://www.facebook.com/plugins/like.php?href=%(url)s&layout=standardt&show_faces=false&width=227&action=like&colorscheme=light&height=50"
                url = base % {"url" : self.getQuotedURL() }
                return url

.. note ::

        If you are using Like button you should also add OpenGraph metadata to your pages
        as described below.

More info

* http://developers.facebook.com/docs/reference/plugins/like/

OpenGraph metadata
--------------------

OpenGraph is Facebook page metadata protocol. You'll insert extra
<meta> tags on the page which will give additional information about the page
to be displayed with Facebook links.

* http://developers.facebook.com/docs/opengraph/

Below is an example of filling in Facebook metadata

* Using content description in Facebook

* Having main image

* Having location

* Having contact info

.. note ::

        You need to include your Facebook app or your Facebook user id as the admin for the site
        in the metadata.
        Otherwise Facebook will report an error for the page.

You can see Facebook id your yourself and your friends here

* http://apps.facebook.com/whatismyid

Simple example. Add this to your :doc:`main_template.pt </templates_css_and_javascripts/template_basics>`.
Supports Plone default content types and news item image

.. code-block:: html

        <html xmlns="http://www.w3.org/1999/xhtml"
              xml:lang="en"
              lang="en"
              tal:define="lang language"
              tal:attributes="lang lang;
                              xml:lang lang">


          <head>

            ...

            <!-- Facebook integration -->

            <meta property="og:description" tal:attributes="content context/Description|nothing"/>

            <tal:has-image omit-tag="" condition="context/image|nothing">
                <tal:comment replace="nothing"><!-- News item image support --></tal:comment>
                <meta property="og:image" tal:attributes="content string:${context/absolute_url}/image"/>
            </tal:has-image>

            <meta property="fb:admins" content="123123" />

            <meta property="og:type" content="website"/>

          </head>


Complex example for custom content type

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          lang="en"
          metal:use-macro="here/main_template/macros/master"
          i18n:domain="saariselka.app"
          >


           <tal:comment replace="nothing">
           <!--

                    We will insert this HTML to <head> section,
                    "head_slot", defined by Plone's main_template.pt

           -->
          </tal:comment>

          <tal:facebook-opengraph metal:fill-slot="head_slot" >

              <meta property="og:description" tal:attributes="content context/Description|nothing"/>
             <meta property="og:type" content="hotel"/>

              <tal:comment replace="nothing">
                   <!--

                            Fill in geo info if available.
                   -->
              </tal:comment>
              <tal:has-location omit-tag="" tal:define="lat view/data/Latitude|nothing; long view/data/Longitude|nothing;" tal:condition="lat">
                    <meta property="og:latitude" tal:attributes="content lat"/>
                    <meta property="og:longitude" tal:attributes="content long"/>
              </tal:has-location>

              <tal:comment replace="nothing">
                   <!--

                            Fill in contact info.
                   -->
              </tal:comment>
              <meta property="og:email" content="xxx@yoursite.com"/>
              <meta property="og:phone_number" content="+ 358 123 1234"/>

              <tal:comment replace="nothing">
                   <!--

                            URL to 70 px wide image used by Facebook as the news item splash image.

                            Note: Facebook resized the image automatically.

                   -->
              </tal:comment>
              <tal:has-image omit-tag="" condition="view/main_image">
                    <meta property="og:image" tal:attributes="content view/main_image"/>
              </tal:has-image>

              <tal:comment replace="nothing">
                   <!-- Facebook admins is a compulsory field. Put here the side admin Facebook id(s), comma separated

                        http://apps.facebook.com/whatismyid
                   -->
              </tal:comment>
              <meta property="fb:admins" content="123123" />

          </tal:facebook-opengraph>
