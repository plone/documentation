===============================
Content Quality helper tools
===============================

.. admonition:: Description

   A selection of add-ons that can help create and maintain appealing, searchable, and high-quality content.



Apart from the :doc:`inbuilt tools <index>`, there are several add-ons available.

Note that these are all separate add-ons you will have to :doc:`install</manage/installing/installing_addons>`, and we strongly suggest testing them out first on a separate test-instance of your site, to see if they fit your purpose and do not interfere with other parts of your site.
Also, some of these tools rely on web-services, which may or may not be allowed or advisable in high-security scenarios.


Avoiding content errors
-----------------------

- `collective.jekyll <https://pypi.python.org/pypi/collective.jekyll>`_ is a package that will help you identify common pitfalls, like too long or short titles or descriptions, or a URL starting with "copy_of". You can even set it up so it alerts editors when they don't stick to the preferred image format, or if a page has not enough links to other pages.
- `eea.progressbar <https://pypi.python.org/pypi/eea.progressbar>`_ can provide a visual clue as to where a document is in the workflow progress, making it easier for editors and reviewers to track what to do next to publish a document.

Check your links
----------------

- `collective.linkcheck <https://pypi.python.org/pypi/collective.linkcheck>`_ provides link validity checking and reporting.
- although you may also want to keep this out of Plone itself, and run an external linkchecker regularly. `This Linkchecker <http://wummel.github.io/linkchecker/>`_ is open source, available for multiple platforms and can be scripted.

Better images
--------------

- `Products.ImageEditor <https://pypi.python.org/pypi/Products.ImageEditor>`_ allows you to rotate, flip, blur, compress, change contrast & brightness, sharpen, add drop shadows, crop, resize an image, and apply sepia.
- `collective.aviary <https://pypi.python.org/pypi/collective.aviary>`_ integrates the external "Aviary" image editor into Plone.
- `plone.app.imagecropping <https://pypi.python.org/pypi/plone.app.imagecropping>`_ surprisingly enough, crops images.


Tags, relations and more
-------------------------

- `eea.tags <https://pypi.python.org/pypi/eea.tags>`_ provides a Facebook-like autocomplete widget for tagging content.
- `eea.alchemy <https://pypi.python.org/pypi/eea.alchemy>`_ allows you to bulk auto-discover geographical coverage, temporal coverage, keywords and more.
- `collective.taghelper <https://pypi.python.org/pypi/collective.taghelper>`_ can connect to a range of webservices to assist tagging
- `collective.simserver <https://github.com/collective/collective.simserver.core>`_ can help with creating 'related items' links
- `collective.taxonomy <https://github.com/collective/collective.taxonomy>`_ can set up hierarchical taxonomies in multiple languages
- `collective.classifiers <https://github.com/collective/collective.classifiers>`_ provides a 'middle ground' between a complex taxonomy and simple tagging, allowing for two new fields to classify content
- `collective.facets <https://github.com/collective/collective.facets>`_ is an alternative approach allowing editors to add 'facets' to content.


Analytics and SEO
------------------

- `collective.googleanalytics <https://pypi.python.org/pypi/collective.googleanalytics>`_ enables easy tracking of the standard Google statistics as well as external links, e-mail address clicks and file downloads. It also defines Analytics reports that are used to query Google and display the results using Google Visualizations.
- `quintagroup.seoptimizer <https://pypi.python.org/pypi/quintagroup.seoptimizer/>`_ allows setting various meta tags and other information search engines like and need.
- if you have migrated from another system, and need to set up aliases to content that still lives in search engines, `Products.RedirectionTool <https://pypi.python.org/pypi/Products.RedirectionTool>`_ gives you an interface to Plone's built-in redirection and aliasing.




And after all that work, you can use `quintagroup.analytics <https://pypi.python.org/pypi/quintagroup.analytics>`_ to see your webmaster stats increase. Now lean back with your favorite hot beverage, you've earned it!
