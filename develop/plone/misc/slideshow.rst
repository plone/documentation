=======================
Slidehows and carousels
=======================

.. admonition:: Description

        How to use annotation design pattern to store
        arbitrary values on Python objects (Plone site,
        HTTP request) for storage and caching purposes.


Introduction
============

Header slideshows

* `Products.Carousel <https://plone.org/products/carousel/>`_

AJAX'y image pop-ups

* https://plone.org/products/pipbox

Migrate Products.Slideshow to Products.Carousel
===============================================

Here is a sample migration code to transform your site
from one add-on to another.

We create a migration view which you can call by typing in view name
manually to web browser.

This code will

* Scan site for folders which have Slideshow add-on enabled. In this example we check against a predefined list (scanned earlier),
  but the code contains example how to detect slideshow folders

* Create Carousel for those folders

* Create corresponds Carousel Banners for all Slideshow Image content items

* Set some Carousel settings

* Make sure that we invalidate cache for content items going through migration

* Set a new default view for folders which were using slideshow

Also

* After inspecting the process was ok you can delete migrated images

carousel.py::

        """

            Migrate slideshow to carousel.

            Usage:

            http://yoursite/@@migrate_carousel - the process can be repeated with adjusted settings. It's non-destructive.

            http://yoursite/@@delete_migrated_slideshow_images

        """

        import logging
        from StringIO import StringIO
        from Products.Five.browser import BrowserView

        from zope.component import getUtility, getMultiAdapter
        from zope.app.component.hooks import setHooks, setSite, getSite

        from zope.interface import alsoProvides
        from Products.Five import BrowserView
        from Products.CMFCore.utils import getToolByName
        from Products.Carousel.interfaces import ICarouselFolder
        from Products.Carousel.utils import addPermissionsForRole
        from Products.Carousel.config import CAROUSEL_ID
        from Products.Carousel.interfaces import ICarousel, ICarouselSettings

        from Products.slideshowfolder.interfaces import ISlideShowSettings, ISlideShowView, IFolderSlideShowView, ISlideShowFolder, ISlideshowImage

        logger = logging.getLogger("Slideshow Migrator")

        FOLDER_PATHS_TO_MIGRATE="""
        ('', 'site', 'folder1')
        ('', 'site', 'folder2')
        ('', 'site', 'folder2', 'subfolder')
        """

        class MigrateSlideshowToCarousel(BrowserView):
            """
            Migrate collective.slideshow to Products.Carousel
            """


            def startCapture(self, newLogLevel = None):
                """ Start capturing log output to a string buffer.

                http://docs.python.org/release/2.6/library/logging.html

                @param newLogLevel: Optionally change the global logging level, e.g. logging.DEBUG
                """
                self.buffer = StringIO()

                print >> self.buffer, "Log output"

                rootLogger = logging.getLogger()

                if newLogLevel:
                    self.oldLogLevel = rootLogger.getEffectiveLevel()
                    rootLogger.setLevel(newLogLevel)
                else:
                    self.oldLogLevel = None

                self.logHandler = logging.StreamHandler(self.buffer)
                formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
                self.logHandler.setFormatter(formatter)
                rootLogger.addHandler(self.logHandler)

            def stopCapture(self):
                """ Stop capturing log output.

                @return: Collected log output as string
                """

                # Remove our handler
                rootLogger = logging.getLogger()

                # Restore logging level (if any)
                if self.oldLogLevel:
                    rootLogger.setLevel(self.oldLogLevel)

                rootLogger.removeHandler(self.logHandler)

                self.logHandler.flush()
                self.buffer.flush()

                return self.buffer.getvalue()


            def getImages(self, folder):
                """ Get all ATImages in a folder """
                for obj in folder.objectValues():
                    if obj.portal_type == "Image":
                        yield obj

            def getOrCreateCarousel(self, folder):
                """ Copied from Products.Carousel manager.py """


                if hasattr(folder.aq_base, CAROUSEL_ID):
                    logger.info("Using existing carousel in " + str(folder))
                    carousel = getattr(folder, CAROUSEL_ID)
                else:
                    logger.info("Creating carousel in " + str(folder))
                    pt = getToolByName(folder, 'portal_types')
                    newid = pt.constructContent('Folder', folder, 'carousel', title='Carousel Banners', excludeFromNav=True)
                    carousel = getattr(folder, newid)

                    # mark the new folder as a Carousel folder
                    alsoProvides(carousel, ICarouselFolder)

                    # make sure Carousel banners are addable within the new folder
                    addPermissionsForRole(carousel, 'Manager', ('Carousel: Add Carousel Banner',))

                    # make sure *only* Carousel banners are addable
                    carousel.setConstrainTypesMode(1)
                    carousel.setLocallyAllowedTypes(['Carousel Banner'])
                    carousel.setImmediatelyAddableTypes(['Carousel Banner'])

                return carousel

            def imageToCarouselBanner(self, image, carousel):
                """
                Convert ATImage to Carousel Banner content item.
                """

                logger.info("Migrating slideshow image:" + str(image.getId()))

                id = image.getId()

                if not id in carousel.objectIds():
                    carousel.invokeFactory("Carousel Banner", id, title=image.Title())
                else:
                    logger.info("Carousel image already existed " + str(image))

                banner = carousel[id]

                # Copy over image field from ATImage content type
                banner.setImage(image.getImage())


                # Set a hidden flag which allows us later to delete images
                image._migrated_to_carousel = True

                 from Products.CMFCore.WorkflowCore import WorkflowException

                workflowTool = getToolByName(banner, "portal_workflow")
                try:
                    workflowTool.doActionFor(banner, "publish")
                    logger.info("Published " + banner.getId())
                except WorkflowException:
                    # a workflow exception is risen if the state transition is not available
                    # (the sampleProperty content is in a workflow state which
                    # does not have a "submit" transition)
                    logger.info("Could not publish:" + str(banner.getId()) + " already published?")
                    pass

            def setupCarousel(self, carousel_folder):
                """
                Set-up custom carousel settings for all carousels.
                """

                logger.info("Setting carousel settings for:" + carousel_folder.absolute_url())

                settings = ICarouselSettings(carousel_folder)

                settings.width = 640
                settings.height = 450
                settings.pager_template = u'@@pager-none'
                settings.default_page_only = False
                settings.element_id = "karuselli"
                settings.transition_delay = 5.0
                settings.banner_elements = [ u"image" ]


            def migrateFolder(self, folder):
                """ Migrate one folder from Slideshow to Products.Carousel
                """
                logger.info("Migrating folder:" + str(folder))

                carousel = self.getOrCreateCarousel(folder)

                self.setupCarousel(carousel)

                images = self.getImages(folder)
                for image in images:
                    self.imageToCarouselBanner(image, carousel)

                # This will toggle cache refresh for the object
                # if Products.CacheSetup is used -> should invalidate template cache.
                # Not necessary if Products.CacheSetup is not installed.
                folder.setTitle(folder.Title())
                folder.reindexObject()

                # Toggle folder away from slideshow view
                # empty_view is our custom view which does not list folder contents
                folder.setLayout("empty_view")

                # Set a marker flag in the case we need to play around with these
                # folders programmatically in the future
                folder._migrated_to_carousel = True




            def migrate(self):
                """
                Run the migration process for one Plone site.
                """

                brains = self.context.portal_catalog(portal_type="Folder")

                # Use predefined report of slideshow folder on old site
                # Alternative: detect slideshow folders as shown below
                carousel_folders  = FOLDER_PATHS_TO_MIGRATE.split("\n")

                for b in brains:

                    obj = b.getObject()

                    path = str(obj.getPhysicalPath())

                    # Alternative: if you don't have fixed list check here if getattr(obj, "default_view", "") == "slideshow_view"
                    if path in carousel_folders:
                        self.migrateFolder(obj)


            def __call__(self):
                """ Process the form.

                Process the form, log the output and show the output to the user.
                """

                self.logs = None


                try:
                    self.startCapture(logging.DEBUG)

                    logger.info("Starting full site migration")

                    # Do the long running,
                    # lots of logging stuff
                    self.migrate()

                    logger.info("Successfully done")


                except Exception, e:
                    # Show friendly error message
                    logger.exception(e)

                # Put log output for the page template access
                self.logs = self.stopCapture()

                return self.logs

        class DeleteMigratedImages(BrowserView):
            """
            Delete all slideshow image files which have been migrated to carousel banners.

            By doing migration in two phases allows us to adjust the process in the case it goes wrong.
            """

            def __call__(self):
                """

                """

                self.buffer = StringIO()

                print >> self.buffer, "Log output"

                brains = self.context.portal_catalog(portal_type="Image")
                for b in brains:
                    obj = b.getObject()
                    if getattr(obj, "_migrated_to_carousel", False) == True:
                        print >> self.buffer, "Deleting migrated Image " + obj.getId()
                        id = obj.getId()
                        parent = obj.aq_parent
                        parent.manage_delObjects([id])

                print >> self.buffer, "All migrated images deleted"

                return self.buffer.getvalue()



ZCML bits::

  <browser:page
    for="*"
    name="migrate_carousel"
    permission="cmf.ManagePortal"
    class=".carousel.MigrateSlideshowToCarousel"
    />

  <browser:page
    for="*"
    name="delete_migrated_slideshow_images"
    permission="cmf.ManagePortal"
    class=".carousel.DeleteMigratedImages"
    />

Setting every carousel widths on the site
============================================

Another example to manipulate Products.Carousel.
This script will update all carousel settings
on the site to have new image width.

::

        class SetCarouselWidths(BrowserView):
            """
            Set width to all carousels on the site.
            """

            def __call__(self):
                """

                """

                self.buffer = StringIO()

                print >> self.buffer, "Log output"

                brains = self.context.portal_catalog(portal_type="Folder")
                for b in brains:
                    obj = b.getObject()
                    if "carousel" in obj.objectIds():
                        carousel = obj["carousel"]
                        # Carousel installed on this folder
                        settings = ICarouselSettings(carousel)
                        print >> self.buffer, "Setting width for " + carousel.absolute_url()
                        settings.width = 680

                print >> self.buffer, "All carousels updated"

                return self.buffer.getvalue()


ZCML

.. code-block:: xml

  <browser:page
    for="*"
    name="set_carousel_widths"
    permission="cmf.ManagePortal"
    class=".carousel.SetCarouselWidths"
    />

AJAX full-size image loading for album views
----------------------------------------------

Plone album views can be converted to pop-up image viewing with PipBox.

Put the following to portal_properties / pipbox_properties

Album view <a> click handler::

    {type:'overlay', subtype:'image', selector:'.photoAlbumEntry a', urlmatch:'/view$', urlreplace:'/image_large'}


.. note::

        portal_javascript must be in debug mode while testing different Products.PipBox handlers.

