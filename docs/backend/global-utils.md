---
html_meta:
  "description": "Global functions defined in CMFPlone and plone.app.layout."
  "property=og:description": "Global functions defined in CMFPlone and plone.app.layout."
  "property=og:title": "Global utils and helpers"
  "keywords": "global variables,portal_state,context_state,plone_view,portal_url,helper methods"
---


# Global utils and helpers

The following are global functions defined in `CMFPlone` and `plone.app.layout`.

- `portal_state`
- `context_state`
- `plone_view`


(backend-global-utils-plone-view-label)=

## `plone_view`

```python
def getCurrentUrl():
    """ Returns the actual url plus the query string. """

def uniqueItemIndex(pos=0):
    """Return an index iterator."""

def toLocalizedTime(time, long_format=None, time_only=None):
    """ The time parameter must be either a string that is suitable for
        initializing a DateTime or a DateTime object. Returns a localized
        string.
    """

def toLocalizedSize(size):
    """ Convert an integer to a localized size string
    3322 -> 3KB in english, 3Ko in french
    """

def normalizeString(text):
    """Normalizes a title to an id.
    """

def isDefaultPageInFolder():
    """ Returns a boolean indicating whether the current context is the
        default page of its parent folder.
    """

def isStructuralFolder():
    """Checks if a given object is a "structural folder".

    That is, a folderish item which does not explicitly implement
    INonStructuralFolder to declare that it doesn't wish to be treated
    as a folder by the navtree, the tab generation etc.
    """

def navigationRootPath():
    """Get the current navigation root path
    """

def navigationRootUrl():
    """Get the url to the current navigation root
    """

def getParentObject():
    """Returns the parent of the current object, equivalent to
        aq_inner(aq_parent(context)), or context.aq_inner.getParentNode()
    """

def getCurrentFolder():
    """If the context is the default page of a folder or is not itself a
        folder, the parent is returned, otherwise the object itself is
        returned.  This is useful for providing a context for methods
        which wish to act on what is considered the current folder in the
        ui.
    """

def getCurrentFolderUrl():
    """Returns the URL of the current folder as determined by
        self.getCurrentFolder(), used heavily in actions.
    """

def getCurrentObjectUrl():
    """Returns the URL of the current object unless that object is a
        folder default page, in which case it returns the parent.
    """

def isFolderOrFolderDefaultPage():
    """Returns true only if the current object is either a folder (as
        determined by isStructuralFolder) or the default page in context.
    """

def isPortalOrPortalDefaultPage():
    """Returns true only if the current object is either the portal object
        or the default page of the portal.
    """

def getViewTemplateId():
    """Returns the template Id corresponding to the default view method of
        the context object.
    """

def showToolbar():
    """Returns true if the editable border should be shown
    """

def cropText(text, length, ellipsis):
    """ Crop text on a word boundary """

def site_encoding():
    """ returns site encoding """

def patterns_settings():
    """ returns mockup pattern settings """
```

(backend-global-utils-portal-state-label)=

## `portal_state`

```python
def portal():
    """The portal object"""

def portal_title():
    """The title of the portal object"""

def portal_url():
    """The URL of the portal object"""

def navigation_root():
    """The navigation root object"""

def navigation_root_title():
    """The title of the navigation root object"""

def navigation_root_path():
    """path of the navigation root"""

def navigation_root_url():
    """The URL of the navigation root"""

def default_language():
    """The default language in the portal"""

def language():
    """The current language"""

def locale():
    """Get the current locale"""

def is_rtl():
    """Whether or not the portal is being viewed in an RTL language"""

def member():
    """The current authenticated member"""

def anonymous():
    """Whether or not the current member is Anonymous"""

def friendly_types():
    """Get a list of portal types considered "end user" types"""
```

(backend-global-utils-context-state-label)=

## `context_state`

```python
def current_page_url():
    """The URL to the current page, including template and query string."""

def current_base_url():
    """The current "actual" URL from the request, excluding the query
    string.
    """

def canonical_object():
    """The current "canonical" object.

    That is, the current object unless this object is the default page
    in its folder, in which case the folder is returned.
    """

def canonical_object_url():
    """The URL to the current "canonical" object.

    That is, the current object unless this object is the default page
    in its folder, in which case the folder is returned.
    """

def view_url():
    """URL to use for viewing

    Files and Images get downloaded when they are directly
    called, instead of with /view appended.  We want to avoid that.
    """

def view_template_id():
    """The id of the view template of the context"""

def is_view_template():
    """Return True if the currentl URL (in the request) refers to the
    standard "view" of the context (i.e. the "view" tab).
    """

def object_url():
    """The URL of the current object"""

def object_title():
    """The prettified title of the current object"""

def workflow_state():
    """The workflow state of the current object"""

def parent():
    """The direct parent of the current object"""

def folder():
    """The current canonical folder"""

def is_folderish():
    """True if this is a folderish object, structural or not"""

def is_structural_folder():
    """True if this is a structural folder"""

def is_default_page():
    """True if this is the default page of its folder"""

def is_portal_root():
    """True if this is the portal or the default page in the portal"""

def is_editable():
    """Whether or not the current object is editable"""

def is_locked():
    """Whether or not the current object is locked"""

def is_toolbar_visible():
    """Wether toolbar is visible or not in the actual context"""

def actions(category):
    """The filtered actions in the context. You can restrict the actions
    to just one category.
    """

def portlet_assignable():
    """Whether or not the context is capable of having locally assigned
    portlets.
    """
```