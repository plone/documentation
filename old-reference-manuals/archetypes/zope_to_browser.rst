=========================
From Zope to the Browser
=========================

.. admonition:: Description

		How do content types get "published" (in the Zope sense, not
		the workflow sense) to the web browser?

There is a fairly complex mechanism that determines how a content object
ends up being displayed in the browser. The following is an adaptation
of an email to the plone-devel list which aims to untangle this
complexity. It pertains to Plone 2.1 only.
Assumptions:

 * You want the 'view' action to be the same as what happens when you go to the object directly for most content types...

 * ...but for some types, like File and Image, you want the "view" action to display a template, whereas if you go straight to the object, you get the file's contents

 * You want to be able to redefine the 'view' action in your custom content types or TTW in portal\_types explicitly. This will essentially override the current layout template selection. Probably this won't be done very often for things deriving from ATContentTypes, since here you can register new templates with the FTI and have those be used (via the "display" menu) in a more flexible (e.g. per-instance, user-selectable) way, but you still want the "view" action to give the same power to change the default view of an object as it always has.

 * When you use the "display" menu (implemented with IBrowserDefault) to set a default page in a folderish container, you want it to display that item always, unless there is an index\_html - index\_html always wins (note - the "display" menu is disabled when there is an index\_html in he folder, precisely because it will have no effect)

 * When you use the "display" menu to set a layout template for an object (folderish or not), you want that to be displayed on the "view" tab (action), as well as by default when the object is traversed to without a template/action specified...

 * ...except for ATFile and ATImage, which use a method index\_html() to cut in when you don't explicitly specify an item. However, these types will \*still\* want their "view" action to show the selected layout, but will want a no-template invocation to result in the file content

Some implementation detail notes:
There are two distinct cases:

CASE I: "New-style" content types using the paradigms of ATContentTypes
-- These implement ISelectableBrowserDefault, now found in the generic
CMFDynamicViewFTI product. They support the "display" menu with
per-instance selectable views, including the ability to select a
default-page for folders via the GUI. These use CMF 1.5 features
explicitly.

CASE II: "Old-style" content types, including CMF types and old AT types
-- These do not implement this interface. The "display" menu is not
used. The previous behavior of Plone still holds.
The "old-style" behavior is implemented using the Zope hook
\_\_browser\_default\_\_(), which exists to define what happens when you
traverse to an object without an explicit page template or method. This
is used to look up the default-page (e.g. index\_html) or discover what
page template to render. In Plone, \_\_browser\_default\_\_() calls
PloneTool.browserDefault() to give us a single place to keep track of
this logic. The rules are (slightly simplified):

1. A method, attribute or contained object 'index\_html' will always
win. Files and Images use this to dump content (via a method
index\_html()); creating a content object index\_html in a folder as a
default page is the now-less-encouraged way, but should still be the
method that trumps all others.

2. A property  'default\_page' set on a folderish object giving the id of
a contained object to be the default-page is checked next.

3. A property 'default\_page' in 'site\_properties' gives us a list of
ids to check and treat similarly to index\_html. If a folder contains
items with any of these magic ids, the first one found will be used as a
default-page.

4. If the object has a 'folderlisting' action, use this. This is a funny
fallback which is necessary for old-style folders to work (see below).

5. Look up the object's 'view' action and use this if none of the above
hold true.

In addition, we test for ITranslatable to allow the correct translation
of returned pages to be selected (LinguaPlone), and have some WebDAV
overrides.
Lastly, it has always been possible to put "/view" at the end of a URL
and get the view of the object, regardless of any index\_html() method.
This means that you can go to /path/to/file/view and get the view of the
file, even if /path/to/file would dump the content (since it has an
index\_html() method that does that).
This mechanism uses the method view(), defined in PortalContent in CMF
(and also in BaseFolder in Archetypes). view() returns 'self()', which
results in a call to \_\_call\_\_(). In CMF 1.4, this would look up the
'view' action and resolve this. Note that for \*folders\* in Plone 2.0,
the 'view' action is just 'string:${object\_url}/', which in turn
results in \_\_browser\_default\_\_() and the above rules. This means
that /path/to/folder/view will render a default-page such as a content
object index\_html. The fallback on the 'folderlisting' action in
PloneTool.browserDefault() mentioned above is there to ensure that when
there \*isn't\* an index\_html or other default-page, we get
'folder\_listing' (instead of an infinite loop), essentially making the
'folderlisting' action on Folders the canonical place to specify the view
template. If you think that sounds messy, you're right. (With CMF 1.5
types, things are little different - more on that later.)

Enter CMF 1.5. CMF 1.5 introduces "Method Aliases". It is important to
separate these from actions:

Actions -- These generate the content action tabs (the green ones). You
almost always have 'view' and 'edit'. Other standard actions are
'properties' and 'sharing'. Each action has a target, which is typically
something like 'string:${object\_url}/base\_edit' for the edit tab.
'base\_edit' here is a page template.

Method aliases -- These let you generalize actions. The alias 'edit' can
point to 'atct\_edit' for an ATContentTypes document, for example, and
point to 'document\_edit\_form' for a CMF document. Aliases can be
traversed to, so /path/to/object/edit will send you to 'atct\_edit' on
the object if the object is an ATContentTypes document, and to
'document\_edit\_form' if it is a CMF Document.
This level of indirection is actually quite useful. First of all, we get
a standard set of URLs, so /path/to/object/edit is always edit,
/path/to/object/view is always view. The actions (tabs) can point to
these, meaning that we can pretty much use the same set of actions for
all common types, with the variation happening in the aliases instead.
Secondly, a method alias with the name "(Default)" specifies what
happens when you browse to the object without any template or action
specified. That is, /path/to/object will look up the "(Default)" alias.
This may specify a page template, for example, or a method (such as a
file-dumping index\_html()) to call.
Crucially, if "(Default)" is not set or is an empty string, CMF falls
back on the old behavior of calling the \_\_browser\_default\_\_()
method. In PloneFolder.py, this is defined to call
PloneTool.browserDefault(), as mentioned above, which implements the
Plone-specific rules for the lookup. Hence, if we need the old
behavior, we can just unset "(Default)"! This is what happens with
old-style content types (that is, it is the default if you're not using
ATContentTypes' base classes or setting up the aliases yourself).
Now, CMFDynamicViewFTI, which is used by ATContentTypes, extends the
standard CMF FTI and a adds a few things:

1. A pair of interfaces, ISelectableBrowserDefault and IBrowserDefault
(the former extends the latter) describing various methods for getting
dynamic views, as found in Plone in the "display" menu.

2. A class BrowserDefaultMixin which gives you a sensible implementation
of these. This uses two properties, "default\_page" and "layout" to keep
track of which default-page and/or view template (aka layout) is
currently selected on an object.

3. Two new properties in the FTI in portal\_types - the default view,
and the list of available views.

4. A special \*target\* for a method alias called '(selected layout)',
which will return the
selected view template (layout).

5. Another special alias target called '(dynamic view)', which will
return a default-page, if set, or else the selected view template
(layout) - you can think of "(dynamic view)" as a superset of "(selected
layout)".

ATContentTypes uses BrowserDefaultMixin from CMFDynamicViewFTI, and sets
up the standard aliases for "(Default)" and "view" to point to "(dynamic
view)". The exceptions are File and Image, which have the "(Default)"
alias pointing to "index\_html", and the "view" alias pointing to
"(selected layout)". This way, /path/to/file results in the file content
(via the index\_html() method) and /path/to/file/view shows the selected
layout inside Plone. (Note that using "(dynamic view)" for the "view"
alias would \*not\* work, because the index\_html attribute would take
precedence over the layout when testing for a default-page.)
Additionally, the 'view' action (tab) for each of these types must be
'string:${object\_url}/view' to ensure it invokes the "view" alias, not
the "(Default)" alias.
For Folders, the use of "(dynamic view)" takes care of the default-page
and the selected view template. The 'folderlisting' fallback is no
longer needed - the 'view' action can still be "string:${object\_url}",
and the "(Default)" alias pointing to "(dynamic view)" takes care of the
rest.
In order for the "(dynamic view)" target to work as expected, it needs
to delegate to PloneTool so that Plone's rules for lookup order and
(especially) ITranslatable/LinguaPlone support are used. However,
delegating to PloneTool.browserDefault() is not an option, because this
does other checks which are not relevant (this essentially stems from
the fact that browserDefault() is implementing \*both\* the "(Default)"
and "view" cases above in a single method). Thus, the code for
determining which, if any, contained content object should be used as a
default-page has been factored out to its own method,
PloneTool.getDefaultPage(). Helpfully, this can also be used by
PloneTool.isDefaultPage(), radically simplifying that method.

Calling content objects
~~~~~~~~~~~~~~~~~~~~~~~~

The last issue is what happens with view() and \_\_call\_\_() in this
equation. The first thing to note is that view() method is masked by the
'view' method alias. Hence, /path/to/object/view will invoke the method
alias 'view' if it exists, not call view(), making that method a lot
less relevant.
However, we still want \_\_call\_\_() to have a well-defined behavior.
In CMF 1.4, \_\_call\_\_()used to look up the 'view' action, and this is
still the default fallback, but if the "(Default)" alias is set, this is
used instead. This may give somewhat unexpected behavior, however: From
the comments in the source code and the behavior in Zope, where
\_\_call\_\_() is the last fallback if neither
\_\_browser\_default\_\_() nor index\_html are found, and to ensure that
the "view() --> \_\_call\_\_()" mechanism always returns the object
itself, never dumped file content, it seems to be the intention that
\_\_call\_\_() should always return the object, never a default-page or
file content dumped via an index\_html() method. For \*Folders\* in
Plone 2.0, this was actually not the case: \_\_call\_\_() would look up
the 'view' action, which was "string:${object\_url}", which with the use
of \_\_browser\_default\_\_() resulted in a lookup of a default-page if
one was present. With the CMF 1.5 behavior, the use of the "(Default)"
alias in \_\_call\_\_() will mean that calling a File returns the dumped
file content. Calling a Folder will return the default-page (or the
Folder in its view if no default page is set) as in Plone 2.0.
The behavior in Plone 2.1 is that \_\_call\_\_(), as overridden in
BrowserDefaultMixin, should always return the object itself as it would
be rendered in Plone without any index\_html or default-page magic.
Hence, \_\_call\_\_() in CMFDynamicViewFTI looks up the "(selected
layout)" target and resolves this. This behavior is thus consistent
with the old behavior of Documents and Files, but whereas Folders with
a default-page in 2.0 used to return that default page from
\_\_call\_\_(), in 2.1, it returns the Folder itself rendered in its
selected layout. Again remember that this method will rarely if ever be
called, since /path/to/object is intercepted by CMF's pre-traversal hook
and ends up looking up the "(Default)" method alias (which \*does\*
honor default-page for Folders), and /path/to/object/view uses the
"view" method alias, as described above.
