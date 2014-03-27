Jumpstart Your Theme Development Using Paster
=============================================

The quickest and most efficient way to get started is not to create your
theme product folders and associated files from scratch, but to take
advantage of a product generator which will automatically create the
framework for a theme product based on your responses to a few
interactive questions.

Using Paster on Your Local Machine
----------------------------------

For users more comfortable using the command line, you are more likely
to use a tool called ZopeSkel and the paster templates it contains.
ZopeSkel is a collection of PasteScript templates which can be used to
quickly generate Zope and Plone projects like buildouts, archetypes
products and, most pertinently for us, Plone themes.

`Please refer to this manual page for up-to-date instructions how to
include Paster with ZopeSkel templates in your Plone
configuration <http://collective-docs.readthedocs.org/en/latest/tutorials/paste.html>`_.
Plone Unified Installer should ship with a working Paster command.

Create your Theme Product
~~~~~~~~~~~~~~~~~~~~~~~~~

If you have paster and ZopeSkel installed, navigate to the directory
where you'd like to create your product (we'd recommend [your
buildout]/[zinstance\|zeocluster/src]) and run from the command line:

::

    $ bin/paster create -t plone3_theme plonetheme.mytheme

or, if you have paster in your Plone installation:

::

    $ [path to your buildout]/python-[version]/paster create -t plone3_theme plonetheme.mytheme

This will initiate a series of questions by the paster script. The
defaults are largely appropriate for your first theme, so in many cases
you can simply hit return. Here is example output from the interactive
session.

::

    Selected and implied templates:  ZopeSkel#basic_namespace  A project with a namespace package  ZopeSkel#plone            A Plone project  ZopeSkel#plone3_theme     A Theme for Plone 3.0Variables:  egg:      plonetheme.mytheme  package:  plonethememytheme  project:  plonetheme.mythemeEnter namespace_package (Namespace package (like plonetheme)) ['plonetheme']:Enter package (The package contained namespace package (like example)) ['example']:mythemeEnter skinname (The skin selection to be added to 'portal_skins' (like 'My Theme')) ['']:My ThemeEnter skinbase (Name of the skin selection from which the new one will be copied) ['Plone Default']:Enter empty_styles (Override default public stylesheets with empty ones?) [True]: FalseEnter include_doc (Include in-line documentation in generated code?) [False]:TrueEnter zope2product (Are you creating a Zope 2 Product?) [True]:Enter version (Version) ['1.0']:Enter description (One-line description of the package) ['An installable theme for Plone 3.0']: Enter long_description (Multi-line description (in reST)) ['']:Enter author (Author name) ['Plone Collective']:Enter author_email (Author email) ['product-developers@lists.plone.org']:Enter keywords (Space-separated keywords/tags) ['web zope plone theme']:Enter url (URL of homepage) ['http://svn.plone.org/svn/collective/']:Enter license_name (License name) ['GPL']:Enter zip_safe (True/False: if the package can be distributed as a .zip file) [False]:

You cannot use 'delete' to correct a typo during the interactive
session. If you make a mistake, ctrl-c to stop the script and start
over.

Paster Options
--------------

Some of these questions warrant further explanation:

Enter namespace\_package
    It is good practice to use the 'plonetheme' namespace for your
    theme. You can use other namespaces, of course ('products' might be
    another), but unless you have a compelling reason to do otherwise,
    use 'plonetheme'.
Enter package
    The 'package' is simply the lowercase name of your theme product,
    sans spaces or underscores.
Enter skinname
    The 'skinname' is the human-readable name for your theme. Spaces and
    capitalization are appropriate.
Enter skinbase
    In nearly all cases, you'll want to leave this as 'Plone Default'.
Enter empty\_styles
    Answering 'True' will cause empty stylesheets to be added to your
    product which will override the default base.css, public.css, and
    portlets.css included in any Plone site using the 'Plone Default'
    skin. 'False' will not add empty stylesheets. For the purposes of
    this practical, we recommend entering 'False'.
Enter include\_doc
    Answering 'True' will cause inline documentation to be added to the
    files created by ZopeSkel. It is worth doing this at least once, as
    some of the documentation is quite useful.
Enter zope2product
    Answering 'True' means that the package will be useable as an egg,
    it will be listed in the ZMI, skin folders will be registered as
    layers with the Skins Tool ('portal\_skins'), and the Generic Setup
    profile for the product can be loaded via the Setup Tool
    ('portal\_setup'). We'll explore some of this further; for now,
    suffice to say that you'll always want to enter 'True' here when
    generating a Plone theme.
Enter zip\_safe
    Stick with the default here.

`Creating new eggs and packages quickly with
paster <http://plone.org/documentation/how-to/how-to-create-a-plone-3-theme-product-on-the-filesystem/use-paster>`_

    How to use the paster command to create new packages with proper
    setuptools- and egg-compliant filesystem layout quickly and easily.

