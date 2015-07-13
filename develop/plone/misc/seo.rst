==================================
 Search engine optimization (seo)
==================================

.. admonition:: Description

	How to make Plone more search engine aware

.. contents:: :local:

Introduction
--------------

Plone is very search-engine friendly out of the box.

You can further fine-tune your search engine optimizations with PloneSEO add-on

* https://plone.org/products/plone-seo/

robots.txt
------------------

You probably want to exclude following from the search engine listing

* Your image bank

* All search listings

* Login form

* Send to form

* ... generally all forms

See

* http://opensourcehacker.com/2009/08/07/seo-tips-query-strings-multiple-languages-forms-and-other-content-management-system-issues/

Procedural robots.txt
------------------------

Below is an example how to generate ``robots.txt`` in ZMI Python script.
It prevents accidental indexing of the site from non HTTP 80 ports if you need
to leave Zope direct port open for the world for some reason.

Create new Script (Python) in your site root in ZMI::

	url = context.absolute_url()

	# This is our direct Zope port
	if ":9980" in url:
	    return "Disallow: *\n"


	robots="""
	# Normal robots.txt body is purely substring match only
	# We exclude lots of general purpose forms which are available in various mount points of the site
	# and internal image bank which is hidden in the navigation tree in any case
	User-agent: *
	Disallow: set_language
	Disallow: login_form
	Disallow: sendto_form
	Disallow: /images

	# Googlebot allows regex in its syntax
	# Block all URLs including query strings (? pattern) - contentish objects expose query string only for actions or status reports which
	# might confuse search results.
	# This will also block ?set_language
	User-Agent: Googlebot
	Disallow: /*?*
	Disallow: /*folder_factories$

	# Allow Adsense bot on entire site
	User-agent: Mediapartners-Google*
	Disallow:
	Allow: /*
	"""

	return robots

