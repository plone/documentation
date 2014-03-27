Anatomy of a Plone Theme Product
================================

The directory structure and an explanation of what all these files do.

 

Assuming that you've created your theme product successfully, you should
have a directory structure that looks roughly like this:

::

        plonetheme.mytheme   docs         HISTORY.txt         INSTALL.txt         LICENSE.GPL         LICENSE.txt    MANIFEST.in plonetheme       __init__.py         mytheme             __init__.py             browser                  __init__.py                 configure.zcml                  images                       README.txt                 interfaces.py               stylesheets                      main.css                    README.txt                 viewlet.pt                  viewlets.py            configure.zcml          profiles                 default                     cssregistry.xml                     import_steps.xml                    jsregistry.xml                      metadata.xml                    plonetheme.mytheme_various.txt                      skins.xml                   viewlets.xml           profiles.zcml           setuphandlers.py            skins                plonetheme_mytheme_custom_images                     CONTENT.txt                plonetheme_mytheme_custom_templates                      CONTENT.txt                plonetheme_mytheme_styles                   base.css.dtml                   base_properties.props                   CONTENT.txt                     portlets.css.dtml                   public.css.dtml            skins.zcml          tests.py            version.txt    plonetheme.mytheme-configure.zcml   plonetheme.mytheme.egg-info      dependency_links.txt        entry_points.txt        namespace_packages.txt      not-zip-safe        paster_plugins.txt      PKG-INFO        requires.txt        SOURCES.txt         top_level.txt  README.txt  setup.cfg   setup.py    zopeskel.txt

Things may seem a little complicated at this point, but not to worry.
Let's take closer look at the main files and directories according to
their respective functions.

Documentation
~~~~~~~~~~~~~

docs/
    The docs directory contains installation instructions (INSTALL.txt),
    license files, and the development log (HISTORY.txt).
README.txt
    The top-level text file contains the one-line description of the
    product you entered during the interactive session with ZopeSkel.
    Other README files exist throughout the product.

Python Package
~~~~~~~~~~~~~~

plonetheme/
    This is a namespace package, which serves to group other packages.
mytheme/
    This is the actual name of your theme, usually the name of the
    client or project you are working on.
tests.py
    Python tests for our package go here. Typically themes don't have
    much python code, and so don't have much in the way of testing.
version.txt
    The version of our product. This information is also contained in
    /profiles/default/metadata.xml.

Python Egg
~~~~~~~~~~

plonetheme.mytheme.egg-info/
    The egg metadata is stored here.
setup.cfg
    This configuration file contains information used to create egg-info
    files.
setup.py
    If we wanted setuptools to handle the installation of the package
    and dependencies we could install via "python setup.py install" (for
    now, we don't).

GenericSetup
~~~~~~~~~~~~

profiles.zcml
    Register appropriate GenericSetup profiles.
profiles/
    "Default" is the current configuration profile (only one profile is
    automatically created, but more could be added). Within our
    configuration profile we have XML files which tell GS how to
    configure CSS files (cssregistry.xml), Javascript files
    (jsregistry.xml), skin layers (skins.xml), and viewlets
    (viewlets.xml). Metadata.xml tracks the product version number and
    other metadata, import\_steps.xml \_\_\_\_\_ and the presence of
    plonetheme.mytheme-various.txt tells GS to look to setuphandlers.py
    for additional methods.

Zope 3
~~~~~~

plonetheme.mytheme-configure.zcml

This is the ZCML slug which must be placed in the etc/package-includes
if the theme is installed as a python package (ours won't be).

configure.zcml

skins.zcml

Register skin layers (images, styles, templates) as filesystem directory
views.

browser/

Stylesheets, Templates and More
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you've got your theme product in place, the next step is to modify
the pieces that Plone gives us, specifically templates, stylesheets, and
viewlets.

Templates/
    Plone templates, specifically the main\_template that controls the
    layout of a Plone site, can be grabbed from the
    parts/plone/CMFPlone/skins/plone\_templates directory. Most of the
    templates that were contained here in 2.5 have been moved to eggs
    and are controlled by viewlets. To modify a template from this
    directory, copy it to your theme product, into your theme's
    skins/templates folder and make your modifications there.
Stylesheets/
    Plone's default stylesheets can be found in your
    buildout/parts/plone/CMFPlone/skins/plone\_styles directory. It's
    usually advisable to create a stylesheet specific to your theme
    product, e.g. "mytheme.css" (where "mytheme" is the name of your
    theme product), and then take any relevant styles from CMFPlone's
    stylesheets and customize them in your own theme product, rather
    than overriding entire CMFPlone stylesheets. The one exception here
    may be IEFixes.css, which you likely want to keep intact as a single
    file, since it is called in explicitly from the main\_template.
Viewlets/
    It is a great oversimplification to state that most often you will
    be overriding viewlets from eggs commonly known as plone.app.layout,
    plone.app.portlets, and plone.app.content. Those viewlets, can be
    found in your buildout/eggs/ in packages named
    "plone.app.layout[xx]," "plone.app.portlets[xx]," and
    "plone.app.content[xx]," where [xx] is a version number. When
    modified, these viewlets and their related code belong in your theme
    product's browser/ directory. For more information on how to work
    with viewlets, `read this
    tutorial <http://plone.org/documentation/tutorial/customizing-main-template-viewlets>`_.

If modifying page templates, you won't need to restart Zope in order to
see your changes take effect. Changes to python, XML or ZCML, however,
will require a restart.

`Customization for
developers <http://plone.org/documentation/how-to/how-to-create-a-plone-3-theme-product-on-the-filesystem/plone.org/documentation/tutorial/customization-for-developers>`_
An overview of Plone 3 customization by Martin Aspeli.

