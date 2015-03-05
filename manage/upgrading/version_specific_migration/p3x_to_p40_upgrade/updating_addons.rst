====================================
Updating add-on products for Plone 4
====================================

.. admonition:: Description

   This is a list of the most common updates that need to be applied by product authors to ensure that their products work on Plone 4.

.. contents:: :local:

Detecting Plone 4
=================

When Plone 3 and Plone 4 code branches differ you need to discriminate between Plone versions.
You can do this using BBB imports.

Here is an example how to detect Plone 4 during imports.
Then you can use PLONE_VERSION variable for making different code paths.::

    try:
        # Plone 4 and higher
        import plone.app.upgrade
        PLONE_VERSION = 4
    except ImportError:
        PLONE_VERSION = 3

No more global definitions in templates
=======================================

Lots of definitions that were available in templates in Plone 3.x are no longer there.
You need to add the ones you really need yourself.

It is good practice in most cases to let the templates in your product use the main_template.pt of Plone.
Until Plone 3.x this used to make a lot of variable definitions available directly in your template, as the main template pulled in definitions from the global_defines.pt template.
This was handy, but the downside was that for every template lots of these variables were calculated but never used.
The Plone developers decided that this was too expensive (when thinking in terms of processor time) and removed the global defines.
This makes Plone faster, but it does ask for some changes in your product.

How do you know if your product needs changes?
The theoretical approach would be to open all your templates in an editor and check if every variable that is used in a TALES expression (like tal:content or tal:define) has been defined earlier in that same template.
Note that some variables are still globally available, the most important being context, view and template.
A more practical approach is simply to try out your product in Plone 4, visit all pages that belong to your product and see if any errors occur.
An error would look like this::

    NameError: name 'templateId' is not defined


How do you know what definition you should add to your template?
The canonical place to look this up is the @@plone view from Plone 3 (not Plone 4).
This is the file `Products/CMFPlone/browser/ploneview.py <http://dev.plone.org/plone/browser/CMFPlone/branches/3.0/browser/ploneview.py>`_, specifically the method _initializeData.

The most common variables that are now missing, including their definitions, are these::

    <div
        tal:define="template_id template/getId;
                normalizeString nocall:context/@@plone/normalizeString;
                toLocalizedTime nocall:context/@@plone/toLocalizedTime;
                portal_properties context/portal_properties;
                site_properties context/portal_properties/site_properties;
                here_url context/@@plone_context_state/object_url;
                portal context/@@plone_portal_state/portal;
                isAnon context/@@plone_portal_state/anonymous;
                member context/@@plone_portal_state/member;
                actions python:context.portal_actions.listFilteredActionsFor(context);
                mtool context/portal_membership;
                wtool context/portal_workflow;
                wf_state context/@@plone_context_state/workflow_state;
                default_language context/@@plone_portal_state/default_language;
                is_editable context/@@plone_context_state/is_editable;
                isContextDefaultPage context/@@plone_context_state/is_default_page;
                object_title context/@@plone_context_state/object_title;
                putils context/plone_utils;
                ztu modules/ZTUtils;
                acl_users context/acl_users;
                ifacetool context/portal_interface;
                syntool context/portal_syndication;">
    </div>

These changes are compatible with Plone 3.

Watch out for 'exists'!
-----------------------

A very sneaky thing can go wrong when you use the 'exists' keyword.  Say you have a condition like this in your template::

    tal:condition="python:exists('portal/beautiful.css')"

This condition is False when portal does not have the mentioned css file, but it also fails when portal is not defined!
And you logically get no error message about this, but you just miss a piece of html or some css or javascript is not loaded because this condition is False.
So you should go through your templates, search for the 'exists' keyword and check that everything that should be defined is actually defined.

The action icons tool (portal_actionicons) has been deprecated
==============================================================

Products providing icons for CMF actions should now register them using the 'icon_expr' setting on the action itself, rather than using the separate action icons tool.

In Plone 3, products could register icons associated with CMF actions using the action icons tool (portal_actionicons in the ZMI, actionicons.xml in GenericSetup profiles).
In Plone 4 the action icons tool has been deprecated. Instead, actions in the actions tool and control panel tool can now have an associated icon expression which gives the URL of the icon.

For example, Kupu now registers the icon for its control panel using the following controlpanel.xml file in its GenericSetup profile::

    <?xml version="1.0"?>
    <object name="portal_controlpanel" meta_type="Plone Control Panel Tool">
      <configlet title="Visual editor" action_id="kupu" appId="Kupu"
          category="Plone" condition_expr=""
          icon_expr="string:$portal_url/kupuimages/kupu_icon.gif"
          url_expr="string:${portal_url}/kupu_library_tool/kupu_config"
          visible="True">
        <permission>Manage portal</permission>
      </configlet>
    </object>

The 'icon_expr' setting gives the URL for the icon associated with this configlet.

The 'icon_expr' setting may also be used with normal actions in the actions tool / actions.xml.

Registering icons with the action icons tool will still work in Plone 4, but it is deprecated and will no longer work in the next major release of Plone.
You may remove actionicons.xml to avoid a deprecation warning, or leave it in place to maintain compatibility with Plone 3, depending on your needs.

No more Zope 2 interfaces
=========================

Versions of Zope 2 prior to Zope 2.12.0 supported two types of interfaces (the old Zope 2 implementation and the new Zope 3 implementation from zope.interface).
Now only the latter remains.

In Plone 2.5 and Plone 3, Zope contained two different ways of declaring that a class implements a particular interface.

**Zope 2 style**::

    from Interface import Interface

    class MyInterface(Interface):
        pass

    class MyClass(object):
        __implements__ = (MyInterface,)

**Zope 3 style**::

    from zope.interface import Interface

    class MyInterface(Interface):
        pass

    class MyClass(object):
        implements(MyInterface)

In Zope 2.12, only Zope 3 style interfaces are supported.

Code trying to define Zope 2 interfaces will raise the following exception::

    ImportError: No module named Interface

Zope 2 style interfaces removed from ATContentTypes
---------------------------------------------------

In Plone 3, the Zope 2 style interfaces were defined in interfaces.py and the Zope 3 ones in the interface folder.

In Plone 4, the Zope 2 style interfaces have been removed and the Zope 3 ones moved to the interfaces submodule, to follow naming conventions.
However, a link to these Zope 3 interfaces has been left in interface.py, so the following example code will work in both Plone 3 and 4::

    from Products.ATContentTypes.interface import IATFolder

Trying to use implements() with Zope 2 style interfaces will fail.

Miscellaneous import changes
============================

A number of imports have been moved to new locations.
In addition, a number of previously deprecated methods have been removed.

Moved
-----
P = Abbreviation for "Products".


+---------------------------------------------------+-----------------------------------------------------------------------+
| Old location	                                    | New location                                                          |
+===================================================+=======================================================================+
| P.ATContentTypes.content.folder.ATFolder          | plone.app.folder.folder.ATFolder                                      |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.ATContentTypes.content.folder.ATFolderSchema    | plone.app.folder.folder.ATFolderSchema                                |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.navtree.\	                    | P.CMFPlone.browser.navtree.SitemapNavtreeStrategy.item_icon           |
| SitemapNavtreeStrategy.icon                       |                                                                       |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.plone                          | P.CMFPlone.browser.ploneview                                          |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.ploneview.cache_decorator      | plone.memoize.instance.memoize                                        |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.ploneview.Plone.isRightToLeft  | @@plone_portal_state/is_rtl                                           |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.ploneview.\                    | @@plone_context_state/keyed_actions                                   |
| Plone.keyFilteredActions                          |                                                                       |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.browser.portlets                       | plone.app.portlets.portlets                                           |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.interfaces.OrderedContainer.\          | OFS.interfaces.IOrderedContainer                                      |
| IOrderedContainer                                 |                                                                       |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.utils.BrowserView                      | P.Five.BrowserView                                                    |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.utils.getGlobalTranslationService      | P.PageTemplates.GlobalTranslationService.getGlobalTranslationService  |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.utils.scale_image                      | P.CMFPlone.utils.utranslate                                           |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.PageTemplates.GlobalTranslationService.\        | P.PlonePAS.utils.scale_image                                          |
| getGlobalTranslationService                       |                                                                       |
+---------------------------------------------------+-----------------------------------------------------------------------+
| zope.i18n.translate                               | zope.i18n                                                             |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.CMFPlone.utils.ulocalized_time                  | P.CMFPlone.i18nl10n.ulocalized_time                                   |
+---------------------------------------------------+-----------------------------------------------------------------------+
| zope.app.cache.interfaces.ram.IRAMCache           | zope.ramcache.interfaces.ram.IRAMCache                                |
+---------------------------------------------------+-----------------------------------------------------------------------+
| P.ATReferenceBrowserWidget.\                      | archetypes.referencebrowserwidget.ReferenceBrowserWidget              |
| ATReferenceBrowserWidget.ReferenceBrowserWidget   |                                                                       |
+---------------------------------------------------+-----------------------------------------------------------------------+
	
Removed
-------

Products.CMFPlone.CatalogTool.registerIndexableAttribute – see the plone.indexer package instead.

Products.CMFPlone.PloneTool.setDefaultSkin

Products.CMFPlone.PloneTool.setCurrentSkin

Products.CMFPlone.PortalContent

Products.CMFPlone.browser.ploneview.IndexIterator, Products.CMFPlone.utils.IndexIterator

the Favorite content type

use_folder_tabs from site_properties

The 'actions' method of @@plone_context_state now takes a single parameter
which is the action category that should be retrieved. This should be used
instead of the 'keyed_actions' method which has been removed.

Items removed from the plone_deprecated skin layer:

* colophon.pt
* correctPREformatting.js
* cropText.py
* deprecated.css.dtml
* document_actions.pt
* document_byline.pt
* enabling_cookies.pt
* enabling_cookies.pt.metadata
* extract_date_components.py
* folder_contents_filter.js
* folder_contents_hideAddItems.js
* folder_localrole_add.py
* folder_localrole_delete.py
* folder_localrole_form.pt
* folder_localrole_form.pt.metadata
* footer.pt
* getActionIconList.py
* getActionIconList.py.metadata
* getAddableTypesInMenu.py
* getCurrentUrl.py
* getEventString.py
* getNextMonth.py
* getOrderedUserActions.py
* getPersonalFolderFor.py
* getPreviousMonth.py
* getReplyReplies.py
* getViewTemplateId.py
* getWorkflowHistory.py
* getYearAndMonthToDisplay.py
* getZopeInfo.py
* getZopeInfo.py.metadata
* global_contentmenu.pt
* global_contentviews.pt
* global_logo.pt
* global_pathbar.pt
* global_personalbar.pt
* global_searchbox.pt
* global_sections.pt
* global_siteactions.pt
* global_skinswitcher.pt
* hide_columns.py
* isDefaultPageInFolder.py
* isRightToLeft.py
* keyFilteredActions.py
* login.js
* navigationCurrent.py
* navigationLocalRelated.py
* old_folder_contents.pt
* old_folder_factories.pt
* old_folder_factories.pt.metadata
* plone_minwidth.js.dtml
* plone_minwidth.js.dtml.metadata
* plonifyActions.py
* portlet_calendar.pt
* portlet_events.pt
* portlet_languages.pt
* portlet_login.pt
* portlet_navigation.pt
* portlet_news.pt
* portlet_recent.pt
* portlet_related.pt
* portlet_review.pt
* prepare_slots.py
* presentation.css.dtml
* presentation.css.dtml.metadata
* rejectAnonymous.py
* review_history.pt
* review_history.pt.metadata
* showEditableBorder.py
* viewThreadsAtBottom.pt

AdvancedQuery has been removed from Plone core
==============================================

AdvancedQuery is no longer included with Plone 4, but you may declare it as a dependency for add-on products.

Plone 4 no longer includes AdvancedQuery. In Plone 3, it was used only by wicked, and the Plone 4 version of wicked no longer requires AdvancedQuery. AdvancedQuery was seen by the Plone 4.0 Framework Team as a risky dependency because it is maintained in a private repository rather than in the Plone core or Collective repositories.

If your add-on product or custom code depends on AdvancedQuery, you will need to explicitly require it now. You can do this by including dependency in your add-on product's setup.py::

     install_requires=[
         'setuptools',
         'Products.AdvancedQuery',

`AdvancedQuery can be found here. <https://pypi.python.org/pypi/Products.AdvancedQuery/3.0.1>`_

Validators
==========

Validators no longer function with old style zope 2 interfaces but need new zope 3 style interfaces.

Error you may get when starting your zope instance::

    Products.validation.exceptions.FalseValidatorError:
    <Products.PloneSoftwareCenter.validators.ProjectIdValidator instance at 0xa92082c>

This means that the specified validator is using old interfaces and is not working anymore. You need to remove this line::

    __implements__= (IValidator,)

(IValidator might be called ivalidator in all lowercase, at least in this specific example) and replace it with this::

        implements(IValidator)



If you now use this code on Plone 3, this will fail::

    TypeError: Error when calling the metaclass bases
        iteration over non-sequence


Manual calls to translate
=========================

When you directly call the 'translate' method in your code, there are some changes.

If you have any of these imports, you cannot use them anymore::

    Products.CMFPlone.utils.utranslate
    Products.PageTemplates.GlobalTranslationService.getGlobalTranslationService

Instead you need to use zope.i18n.translate directly. See this example changeset from Poi.

The tricky thing here is that the order of the arguments has changed so you probably need some more changes. The old call signature was this::

    utranslate(domain, msgid, mapping=None, context=None,
        target_language=None, default=None)

And the new is this::

    translate(msgid, domain=None, mapping=None, context=None,
        target_language=None, default=None)

So:
* msgid is now the first instead of the second call
* domain is now optional

And one more tricky thing (and this changeset does that not completely correctly): when you specify the context you first had to pass a content object (usually the page, image, folder etc you are looking at) but now you need to pass in the request instead.

Use plone.app.blob-based BLOB storage
=====================================

Plone 4 ships with a new type of storage specially designed for large binary objects, as images or other files. Here you can learn how to use this feature for new content types and how to and prepare your already existing content types to use the new BLOB storage.

Using plone.app.blob for new content types
------------------------------------------

Just use plone.app.field.BlobField or plone.app.field.ImageField instead of atapi.FileField or atapi.ImageField (respectively) in your schema::

    from Products.Archetypes import atapi
    from plone.app.blob.field import BlobField, ImageField

    schema = atapi.Schema((
        BlobField('afile',
                  widget=atapi.FileWidget(label='A file',
                                          description='Some file'),
                  required=True,
                  ),
        ImageField('animage',
                  widget=atapi.ImageWidget(label='An image',
                                          description='Some image'),
                  ),
        ))

Check the `Archetypes Fields Reference <http://plone.org/documentation/manual/developer-manual/archetypes/fields/fields-reference/>`_ for details.

Preparing already existing content types
----------------------------------------

In order to prepare your own content types to use blobs and provide migration facilities to your users once plone.app.blob is available, you need to perform the following steps. Check `example.blobattype <http://dev.plone.org/collective/browser/example.blobattype/trunk>`_ for example code.

Use a schema extender to replace the FileField(s) of your content type with BlobField(s). For detailed information on how to do so please look into the `archetypes.schemaextender <https://pypi.python.org/pypi/archetypes.schemaextender/>`_ documentation. In essence this breaks down to:

* Creating an extension field::

    class ExtensionBlobField(ExtensionField, BlobField):
        """ derivative of blobfield for extending schemas """

* Extending your content type to use the blob fields. So for instance if your content type ExampleATType has a field named file you will need to register a schema extender like the following::

    class ExampleATTypeExtender(object):
        adapts(IExampleATType)
        implements(ISchemaExtender)

        fields = [
            ExtensionBlobField('file',
                widget=atapi.FileWidget(
                    label=_(u"File"),
                    description=_(u"Some file"),
                ),
                required=True,
                validators=('isNonEmptyFile'),
            ),
        ]

        def __init__(self, context):
            self.context = context

        def getFields(self):
            return self.fields

  If you want to be able to still use your content type without plone.app.blob in sites that have not yet installed support for blobs, you will find it convenient to register the adapter conditionally like so::

    <adapter
        zcml:condition="installed plone.app.blob"
        factory=".extender.ExampleATTypeExtender" />

  This way, if plone.app.blob is not installed your original FileField(s) will be used.

* Provide a migration function for your content. The easiest way to do so is to use the helper method from plone.app.blob. Given a portal type name it will automatically find all blob-aware fields as defined by the schema extender above and perform migrations for those. It is as simple as::

    from plone.app.blob.migrations import migrate
    def migrateExampleATTypes(context):
        return migrate(context, 'ExampleATType')

You can now call *migrateExampleATTypes* from a view or a script to migrate existing content items of the specified type. If you need more control, you can write your own migrator. Please refer to `example.blobattype <http://dev.plone.org/collective/browser/example.blobattype/trunk>`_ for more details on how to do this.

Add views for content types
===========================

In Plone 4, every Factory Type Information object in portal_types will have an additional, optional property which can be set to a TALES expression to provide the URL of a view that will be shown when the user chooses to add an object of this particular type from the "Add" menu in Plone.

This property has the title Add view URL (expression) and the internal id add_view_expr.

For example, if you have a custom add form called @@add-my-content, you could set this expression to string:${folder_url}/@@add-my-content. (Note that the view in this case needs to be registered for the folder type, not for the type being created.)

If this property is not set, Plone will fall back on the createObject script as before, which in turn will create the object or invoke the portal_factory tool. This is likely to be the correct behaviour for most Archetypes-based content objects.

In Plone 3, it was possible to have an add view be invoked by registering a view for the IAdding view (aka the + view) that had the same name as the factory property specified in the Factory Type Information. For example, a type with a factory of my.type could be accompanied by a view with the name 'my.type' registered for the IAdding interface. This would be found and preferred over the createObject script, and was sometimes used with non-Archetypes content.

In Plone 4, this association needs to be made explicit. (This is mainly for performance reasons.) To use such an add view, you need to set the add_view_expr property to invoke it, e.g. string:${folder_url}/+/my.type.

Finally, note that the IAdding (+) view is falling out of favour. It will continue to work indefinitely, but most people these days prefer to register a simple view (e.g. @@add-my-content) for the folder type (e.g. the IFolderish interface from Products.CMFCore.interfaces) which constructs and adds the content in reaction to a valid form submission. This is because the "view-on-a-view" concept used by IAdding can be confusing and requires special handling in certain places (e.g. some vocabulary factories) to deal with the fact that view.context is another view, not a content object. The add form base classes in zope.formlib still use the IAdding view, but z3c.form comes with an add form base class that acts as a simple view.

'MailHost.secureSend' is now deprecated; use 'send' instead
===========================================================

The SecureMailHost product is no longer a part of Plone in 4.0. As a result, the 'secureSend' method which was generally used to send mail is now deprecated. The default 'send' method of MailHost should be used instead.

In Plone 2.1 - 3.x the standard method for sending mail looked like this::

    mh = getToolByName(context, 'MailHost')
    mh.secureSend(message, mto, mfrom, subject=None,
              mcc=None, mbcc=None, subtype=None,
              charset=None, **kwargs)

Where the message parameter is either text with no headers or an email.Message.Message object, the mto, mfrom, mcc and mbcc parameters are lists of email addresses, subject is content of the email subject header, subtype is used to provide the message mime sub-type, charset is used for message and header encoding, and the kwargs are used to provide additional headers.

In Plone 4.x, this method is deprecated and the standard send method of the MailHost should be used instead. The following is an example of using send::

    mh = getToolByName(context, 'MailHost')
    mh.send(messageText, mto=None, mfrom=None,
        subject=None, encode=None,
        immediate=False, charset='utf8', msg_type=None)

Here, messageText is the message with or without headers or an *email.Message.Message* object, *mto* and *mfrom* are strings containing the to and from addresses, *subject* is the content of the email subject header, *encode* is used to specify the message payload encoding (and should almost never be used), *immediate* is used to override the default *MailHost* queuing behavior, and *charset* is used for message and header character encoding (in Plone you should generally pass 'utf8' as the value for charset unless you have a specific reason not to). If you need to set custom headers they will need to be set in the *messageText* itself.

Message Type
------------

Instead of passing the MIME subtype as the subtype parameter to set the message content type, you pass the full MIME type as msg_type. So instead of subtype='plain' you would use msg_type='text/plain'.

Custom Headers
--------------

The *secureSend* method had provided the ability to set some specific headers, and to set custom headers as well. Unfortunately, send does not allow doing this directly; fortunately it is pretty simple to construct a message with custom headers to pass to send. Below is an example that assumes you have the MailHost object and have already defined message_body, mto, mfrom and subject::

    from email import message_from_string
    from email.Header import Header
    my_message = message_from_string(message_body.encode('utf-8'))
    my_message.set_charset('utf-8')
    my_message['CC']= Header('someone@example.com')
    my_message['BCC']= Header('secret@example.com')
    my_message['X-Custom'] = Header(u'Some Custom Parameter', 'utf-8')
    mailhost.send(my_message, mto, mfrom, subject)

Delayed Sending
---------------

By default send waits to send messages until the end of the request transaction.  This ensures that if a conflict error occurs and the transaction is retried, multiple emails will not be sent (which is what happens with secureSend and earlier versions of send). Unfortunately, this means that unless you explicitly request immediate=True when using send, you will not be able to catch any errors which might happen during sending, as they won't occur until the end of the transaction.

If you want to handle email errors to prevent them from aborting an otherwise successful transaction, you need to set immediate=True and enclose the send call in a try/except block. Alternatively, you can go the the MailHost configuration screen in the ZMI and enable SMTP Queuing. This will ensure the mail sending happens completely outside of the transaction, providing more reliability and increased performance while still avoiding transaction retry issues. Using the new MailHost queueing feature is highly recommended for production sites.

Writing Tests
-------------

Plone includes some helpers for writing tests that need to use email in the Products.CMFPlone.tests.utils and Products.CMFPlone.tests.test_mails modules. These include a MockMailHost and a MockMailHostTestCase that replaces the MailHost in the test Plone site with a MockMailHost object. For products that make use of Plone's MockMailHost in their own tests, there are a few more changes that need to be made.

The messages property of the mail host no longer includes the an email.Message object, but instead contains a string representation of message. This means that in order to test the message object you can either work directly with the message string, or convert it into a email message object using the message_from_string function used in the last example.

Summary
-------

In most cases, all you need to do to use send instead of secureSend is convert your mto and mfrom parameters from lists to comma separated strings, and add any CC, BCC, or other headers directly to the messageText instead of passing them as parameters. If you are using secureSend to add custom headers or make other adjustments to the message, the changes are a little more involved, but still straightforward. Additionally, if you are using Plone's MockMailHost in your tests you will need to update your tests to work with the message string rather than an email.Message object.

Portlets Generic Setup syntax changes
=====================================

The syntax for limiting portlets to a certain type of manager has changed.

The original format for limiting a portlet to a certain type of manager was::

    <portlet addview="portlets.BBB"
         title="Foo"
         description="Foo"
         for="plone.app.portlets.interfaces.IColumn" />

but this form was deprecated in Plone 3.1 to allow multiple values in the for field. In Plone 4 the required form is::

    <portlet title="Foo"
            addview="portlets.New"
            description="Foo">
        <for interface="plone.app.portlets.interfaces.IColumn" />
        <for interface="plone.app.portlets.interfaces.IDashboard" />
    </portlet>

Updating Plone 3 themes for Plone 4
===================================

Plone 3 themes may require a few modifications in order to work in Plone 4, depending on how much template customization was done.

Plone 4's Built-in Themes
-------------------------

Plone 3 shipped with two skins, Plone Default and NuPlone.

Plone 4 includes three skins:

* Sunburst Theme
  A new, modern skin, packaged in the plonetheme.sunburst egg.  Sunburst is the default skin for newly created sites.
* Plone Classic Theme
  The old default skin that was called Plone Default in Plone 3. It is now packaged in the plonetheme.classic egg.
* Plone Default (or "Unstyled")
  The "Plone Default" skin is now just a barebones interface with no CSS styling, intended for use with post-processing theming engines such as xdv or deliverance.

Plone 4 no longer ships with NuPlone, but it is still available as an add-on.

Upgrading a Plone 3 site with an existing theme
-----------------------------------------------

If you upgrade a site from an older version of Plone to Plone 4, the automatic upgrade will try to do something reasonable with the theme.

If you have installed and selected a custom theme, almost no changes will be made. The exception is that the 'plone_styles' skin layer will be replaced by the 'classic_styles' layer, since the name of this layer used by the Plone Classic Theme has been renamed. You may need to take additional steps to update the theme to work properly in Plone 4, as described below.

If your skin was set to "Plone Default" with the default set of skin layers, your skin will be set to "Plone Classic Theme," which should look the same.

If your skin was set to "Plone Default" but you have customized it by changing the skin layers used (or installing add-ons which add additional skin layers), then these skin selections will be copied to a new skin called "Old Plone 3 Custom Theme," which will be made active. The viewlet configuration will also be preserved.

Updating a theme to work in Plone 4
-----------------------------------

There are several updates you may need to make to a custom theme to make sure that it continues to work in Plone 4.

Updates to main_template.pt
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your theme has a custom version of main_template.pt, it will need to be updated. The best way to do this is probably to compare the custom main_template to the one that shipped with Plone 3, and then start over with a fresh copy of main_template from Plone 4 and re-apply the same modifications that had been made. In particular, watch for the following changes in main_template:
* The defines on the html tag have been modified.
* Some new defines have been added to the body tag.
* main_template now includes the standard viewlet managers used within the main content area, and defines a new slot called "content-core" where the actual content body goes.

Updates to template variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Templates that have been overridden must be reviewed to make sure new changes to the original templates are included. Also, check to make sure they are not using `global template variables that are no longer available <http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/updating-add-on-products-for-plone-4.0/no-more-global-definitions-in-templates>`_.

Update the "based-on" declarations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your theme is installed via a GenericSetup profile, then you probably have a profiles/default/skins.xml file which declares a "skin-path" consisting of various layers. The skin path declaration may say based-on="Plone Default". If so, update it to say based-on="Plone Classic Theme" so that it will continue to use the same set of layers as a basis that it did in Plone 3. If the "plone_styles" layer is referenced by name, change it to "classic_styles".

Similarly, you may have a profiles/default/viewlets.xml file which customizes the viewlets used in your theme. If any of the "order" or "hidden" manager directives in this file say based-on="Plone Default", update them to say based-on="Plone Classic Theme" instead.

Update the theme-specific interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Your theme may define a Zope 3 interface called IThemeSpecific in browser/interfaces.py. If so, update it so that it extends the theme interface from the Plone Classic Theme::

    from plonetheme.classic.browser.interfaces import IThemeSpecific as IClassicTheme
    class IThemeSpecific(IClassicTheme):
        """theme-specific layer"""

This will ensure that your theme continues to have available the viewlets that are registered for the Plone Classic Theme only, as there are several which are slightly customized compared to the default viewlets of Plone 4 used by the Sunburst theme.

Include a dependency in your (testing) profile's metadata.xml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may to include the plonetheme.classic default profile as a dependency in your products default / testing profile to get your end-to-end tests passing.  Add the following to metadata.xml::

    <dependency>profile-plonetheme.classic:default</dependency>

New users and groups functionality
==================================

Some pages have been renamed and moved, registration made flexible, and nested groups enabled by default.

join_form moved and renamed
---------------------------

In Plone 3, the login form was living in the portal_skins/plone_login skin layer of the Plone (Products.CMFPlone) package. This form has been moved to a Zope 3 view named @@register in the plone.app.users package.

This means that you'll have to adapt any customizations made to the join_form template to use the new @@register view.

Added @@new-user form
---------------------

This is the form that site administrators, or any other user with the Manage users permission, can use to add new users, bypassing the Enable self-registration and Let users select their own passwords settings, that only affect the public @@register form.

User registration fields made flexible
--------------------------------------

The new join and user-addding forms let you to select the groups to which the user will be assigned once created. You can customize which fields do you want to be shown in this form from the Site Setup → Users and Groups → Member registration dialog. You can also modify the list programatically and add new fields as described in `collective.examples.userdata <https://pypi.python.org/pypi/collective.examples.userdata>`_.

Nested groups enabled by default
--------------------------------

When viewing a group's membership page, you can add groups as well as users as members. This way, members of the nested group inherit all roles and permissions assigned to the parent group. For example, the "Biology Department" and "Chemistry Department" groups as well as the college's Dean may belong to the "Science" group. If "Science" is given view rights over the college's intranet folder, the Dean, and anyone belonging to the Biology or Chemisty groups would gain view access to that folder.

If you want to disable this behavior, deactivate the recursive_groups plugin at plone_site_root/acl_users/plugins/Groups Plugins.

Make sure your templates are valid XML
======================================

It's always been "best practice" to make sure your templates validate, even though it's not required. With Plone 4, there are even more benefits to doing so.

It's long been considered "best practice" to make sure that all of the templates in your custom products validate as valid XML.  But, since web browsers are so forgiving of sloppy markup, it has also been the case that there have been few strong incentives to make sure your XML is perfectly valid.  Until now.

By using `Chameleon <http://chameleon.repoze.org/>`_, a drop-in replacement for Zope's ZPT template rendering engine, a Plone 4 site can immediate experience 25-50% improvements in performance.  However, Chameleon absolutely requires that all page templates be valid XML.

Plone 4 does not include Chameleon, although it can be added as an add-on product.  Current plans call for Plone 5 to use Chameleon by default, and it may start shipping (disabled) with a future release in the Plone 4.x series (as of this writing, possibly Plone 4.2). **Bottom line: as you're updating your add-on products for Plone 4, now is the perfect time to double-check your templates to make sure they're well-formed XML.**

The simplest way to validate your templates is probably to use `xmllint <http://www.xmlsoft.org/xmllint.html>`_.  You can also use the `W3C validator <http://validator.w3.org/>`_, either online or `on your Mac OS X system <http://habilis.net/validator-sac/>`_.

document_byline and some other macros are now viewlets
======================================================

Some content relatd TAL macros have been removed and replaced with viewlets.

This change concerns theme and add-on product authors who have custom content templates.

If your template had a byline macro, which shows the author name, before like::

    <div metal:use-macro="context/document_byline/macros/byline"></div>

it does not work anymore (you will receive AttributeError: document_byline).

Byline is now rendered by a viewlet plone.belowcontenttitle.documentbyline (from package plone.app.layout.viewlets) which is defined in a viewlet manager IBelowContentTitle. You need to change this to your content templates.::

    <div tal:replace="structure provider:plone.belowcontenttitle" />

The same goes for document actions. Old::

    <div metal:use-macro="context/document_actions/macros/document_actions"></div>

New::

    <div tal:replace="structure provider:plone.documentactions" />

For templates and macros checklist, please see `this <http://manage.plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/deprecated-templates-checklist>`_.

No longer bin/instance test - use zc.recipe.testrunner
======================================================

Zope 2 start-up script no longer supports running tests. You need to use zc.recipe.testrunner for this purpose.

Add to your builout.cfg:

    parts =
        ...
        test

    [test]
    recipe = zc.recipe.testrunner
    defaults = ['--auto-color', '--auto-progress']
    eggs = ${instance:eggs}

Rerun buildout.Then you can run tests::

    bin/test -s your.packagename

See `z3c.recipe.testrunner <https://pypi.python.org/pypi/zc.recipe.testrunner#detailed-documentation>`_ page for more information.

Changes in PloneTestCase setup
------------------------------

If you previously set up a `PloneTestCase as explained in the developer manual <http://plone.org/documentation/manual/developer-manual/testing/writing-a-plonetestcase-unit-integration-test>`_

you might need to change the initialization of Zope2 products::

    from Products.Five import zcml
    from Testing import ZopeTestCase as ztc
    from Products.PloneTestCase import PloneTestCase as ptc
    from Products.PloneTestCase.layer import onsetup

    @onsetup
    def setup_product():

        import my.types
        zcml.load_config('configure.zcml', my.types)

        # We need to tell the testing framework that these products
        # should be available. This can't happen until after we have loaded
        # the ZCML.
        ztc.installProduct('TextIndexNG3')
        ztc.installPackage('my.types')


    setup_product()
    ptc.setupPloneSite(products=['my.types'])

ztc.installProduct('TextIndexNG3') needs to be moved out of the deferred method setup_product so it's initialized properly::

    @onsetup
    def setup_product():

        import my.types
        zcml.load_config('configure.zcml', my.types)

        # We need to tell the testing framework that these products
        # should be available. This can't happen until after we have loaded
        # the ZCML.
        ztc.installPackage('my.types')

    #initialize products outside of the deferred (@onsetup) method, otherwise it's too late
    ztc.installProduct('TextIndexNG3')

    setup_product()
    ptc.setupPloneSite(products=['my.types'])

see `the blogpost describing this issue in more details <http://webmeisterei.com/news/unit-test-setup-for-plone-4>`_


Vocabulary Directive now replaced by Utilities
==============================================

Vocabulary factories should be registered using utilities

Previously a named vocabulary would be registered in this manner:

**Zope 2 style**::

    <vocabulary
         name="collective.exampleapp.Subscribers"
         factory=".vocabularies.Subscribers" />

**Code that attempts to use the Zope 2 style vocabulary directive will throw a configuration error**::

    ConfigurationError: ('Unknown directive', u'http://namespaces.zope.org/zope', u'vocabulary')

The new way to register a vocabulary is like this:

**Zope 3 style**::

    <utility
         name="collective.exampleapp.Subscribers"
         component=".vocabularies.Subscribers"
         provides="zope.app.schema.vocabulary.IVocabularyFactory"
          />

See more information about :doc:`utilities </develop/addons/components/utilities>` and :doc:`vocabularies </develop/plone/forms/vocabularies>`.

Or register your vocabularies using a grok utility. Read more about :doc:`how vocabularies are handled the grok way </external/plone.app.dexterity/docs/advanced/vocabularies>` in the dexterity developer manual.

Folder implementation changes
=============================

Large Folder and Folder content types have been unified in Plone 4. This may impact your add-on product code.

Plone 4 unifies two different folder implementations (Folder and Large Folder) to one implementation. There are internal changes to ATFolder base classes (Archetypes folder implementation). This change simplifies code, API and makes folders scale better.

plone.app.folder is the new package providing the folder code. plone.app.folder provides a migration view which is run during Plone 4 upgrade for all ATFolder based content.

`For more information see this discussion. <http://plone.293351.n2.nabble.com/Custom-content-and-migrating-to-plone-app-folder-P4-tp5545767p5633850.html>`_

`Performance impact explained. <http://plone.org/products/plone/features/new-faster-folder-implementation>`_

Empty/Control_Panel/Products using Plone 4
==========================================

In Plone 4 Zope Management Interface's Products section has been turned off.

In ZMI, /Control_Panel/Products shows no products, and says "There are currently no items in Product Management"

It was turned off in Plone 4.


