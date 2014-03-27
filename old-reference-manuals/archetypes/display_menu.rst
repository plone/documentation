===================
The 'display' menu
===================

.. admonition:: Description

		The 'display' menu is the drop-down that lets content authors select
		which view template to use, or which object to set as a default-page
		in a folder. 

The ``display`` menu is found in ``global\_contentmenu.pt`` and supports
three different functions:
- Set the display template (aka “layout”) of the current content object,
provided that object supports this.
- Set the default-page of a folder, provided the folder supports this
- If viewing a folder with a default-page, allow selecting the standard
view template/layout for that folder, thus unsetting the default-page.
There are two interfaces in ``CMFDynamicViewFTI.interfaces`` that are used
to support this functionality:
IBrowserDefault – Provides information about the layout current
selection of a given content object, including any selected deafult-page
ISelectableBrowserDefault – Extends IBrowserDeafult with methods to
manipulate the current selection
The canonical implementation of both these interfaces is in
``CMFDynamicViewFTI.browserdefault.BrowserDefaultMixin``. This in turn
gets the vocabulary of available view methods from the FTI (and hence
this can be edited through-the-web in ``portal\_types``), and stores the
current selection in two properties on each content object: ``layout``,
for the currently selected view template, and ``default\_page`` if any
default page is selected. If both are set, the default-page will take
precedence.
``BrowserDefaultMixin`` actually provides a ``\_\_call\_\_`` method which
means that will render the object with its default layout template.
However, ``PloneTool.browserDefault()`` will actually query the interface
directly to find out which template to display - please see the next
page for the gory details.
