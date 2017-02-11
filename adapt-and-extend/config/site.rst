Site Configuration
==================


.. include:: ../../_robot.rst

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Site setup screen
       Go to  ${PLONE_URL}/@@site-controlpanel
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/site-setup.png
       ...  css=#content

.. figure:: ../../_robot/site-setup.png
   :align: center
   :alt: Site setup configuration


These settings should be changed for every site.

Site title
    The name of your website
Site Logo
    Upload your site logo. For extensive customization, you will want to create a special theme that will include your logo, but for a quick change this is enough.
Expose Dublin Core metadata
    This option allows information per content item, like Description, Tags, Author and others, to be shown to and ranked by search engines. It can help improve your search ranking, provided you fill in those fields with correct information.
Expose sitemap.xml.gz
    Almost always a good idea on a public website. It will make life for search engines easier, meaning they can better index your content.
JavaScript for web statistics support
    To gather information for web analytics like Piwik (an open-source self-hosted option) or Google Analytics you can paste the required snippet of code here. Be aware that this can have legal implications (so-called "cookie laws") in some countries.
Display publication date
    Show the date a content item was published in the byline.
Icon visibility
    Controls whether to show different icons for different types of content. Can be useful for content editors, but distracting for anonymous visitors. You can set it to show only for logged-in users.
Toolbar position
    On modern wide-screen monitors, having the Toolbar to the side provides most usable space. But some people prefer it to be on the top of their screen.
Site based relative URL for toolbar Logo
    Customize the small logo on top of the toolbar, if you prefer. Note: this is not the same as the website logo.
robots.txt
    By convention, search engines look for a file called robots.txt to show them what they should index or not.
