================================
Exceptions and common tracebacks
================================

.. admonition:: Description

        Common Python exception traceback patterns you may encounter when
        working with Plone and possible solutions for them.

        Please see :doc:`this tutorial </manage/troubleshooting/basic>` for extracting
        Python tracebacks from your Plone logs.

Add-on installer error: This object was originally created by a product that is no longer installed
---------------------------------------------------------------------------------------------------

**Traceback**::

    2009-10-18 13:11:20 ERROR Zope.SiteErrorLog 1255860680.760.514176531634 http://localhost:8080/twinapex/portal_quickinstaller/installProducts
    Traceback (innermost last):
      Module ZPublisher.Publish, line 125, in publish
      Module Zope2.App.startup, line 238, in commit
      Module transaction._manager, line 93, in commit
      Module transaction._transaction, line 325, in commit
      Module transaction._transaction, line 424, in _commitResources
      Module ZODB.Connection, line 541, in commit
      Module ZODB.Connection, line 586, in _commit
      Module ZODB.Connection, line 620, in _store_objects
      Module ZODB.serialize, line 407, in serialize
      Module OFS.Uninstalled, line 40, in __getstate__
    SystemError: This object was originally created by a product that
                is no longer installed.  It cannot be updated.
                (<Salt at broken>)

**Reason**: Data.fs contains objects for which the code is not present.
You have probably moved Data.fs or edited buildout.cfg.

**Solution**: Check that eggs and zcml contain all necessary products in buildout.cfg.

.. seealso::
    * http://article.gmane.org/gmane.comp.web.zope.plone.setup/3232

Add-on installer error: too many values to unpack
--------------------------------------------------

**Traceback**::

    Module ZPublisher.Publish, line 119, in publish
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 42, in call_object
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 589, in installProducts
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 475, in installProduct
     - __traceback_info__: ('gomobile.mobile',)
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 396, in snapshotPortal
    Module five.localsitemanager.registry, line 194, in registeredUtilities
    Module zope.component.registry, line 127, in registeredUtilities
    ValueError: too many values to unpack

**Condition**: When trying to install a plugin

**Reason**: You have run Data.fs with zope.component 3.5.1, but later downgraded / moved Data.fs.

**Solution**: Pin zope.component to 3.5.1.


Archetypes: TypeError: getattr(): attribute name must be string
------------------------------------------------------------------

**Traceback**::

    'user': <PropertiedUser 'admin'>}
    Module Products.PageTemplates.ZRPythonExpr, line 48, in __call__
     - __traceback_info__: otherwidget.Description(here, target_language=target_language)
    Module PythonExpr, line 1, in <expression>
    Module Products.Archetypes.generator.widget, line 100, in Description
    TypeError: getattr(): attribute name must be string

**Reason**: You might have used something else besides string or translation string
to define Archetypes widget name or description.

AttributeError in setRoles due to workflow state transition
-----------------------------------------------------------

**Traceback**::

    Traceback (innermost last):
    Module ZPublisher.Publish, line 115, in publish
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 41, in call_object
    Module Products.CMFPlone.FactoryTool, line 361, in __call__
    Module Products.CMFPlone.FactoryTool, line 147, in __getitem__
    Module Products.CMFPlone.PloneFolder, line 406, in invokeFactory
    Module Products.CMFCore.TypesTool, line 934, in constructContent
    Module Products.CMFCore.TypesTool, line 345, in constructInstance
    Module Products.CMFCore.TypesTool, line 357, in _finishConstruction
    Module Products.CMFCore.CMFCatalogAware, line 145, in notifyWorkflowCreated
    Module Products.CMFCore.WorkflowTool, line 355, in notifyCreated
    Module Products.DCWorkflow.DCWorkflow, line 392, in notifyCreated
    Module Products.DCWorkflow.DCWorkflow, line 476, in _changeStateOf
    Module Products.DCWorkflow.DCWorkflow, line 571, in _executeTransition
    Module Products.DCWorkflow.DCWorkflow, line 435, in updateRoleMappingsFor
    Module Products.DCWorkflow.utils, line 60, in modifyRolesForPermission
    Module AccessControl.Permission, line 93, in setRoles
    AttributeError: appname

**Possible reasons**:

#. You are using AnnotationStorage but you forgot to declare atapi.ATFieldProperty in your class body
#. You are inhering schema in Archetypes, but you do not inherit the class itself

AttributeError: 'FilesystemResourceDirectory' object has no attribute 'absolute_url'
------------------------------------------------------------------------------------

**Traceback**::

	2013-09-02 12:26:55 ERROR plone.transformchain Unexpected error whilst trying to apply transform chain
	Traceback (most recent call last):
	  File "/home/pab/.buildout/eggs/plone.transformchain-1.0.3-py2.7.egg/plone/transformchain/transformer.py", line 48, in __call__
	    newResult = handler.transformIterable(result, encoding)
	  File "/home/pab/.buildout/eggs/plone.app.theming-1.1.1-py2.7.egg/plone/app/theming/transform.py", line 179, in transformIterable
	    params = prepareThemeParameters(findContext(self.request), self.request, parameterExpressions, cache)
	  File "/home/pab/.buildout/eggs/plone.app.theming-1.1.1-py2.7.egg/plone/app/theming/utils.py", line 630, in prepareThemeParameters
	    params[name] = quote_param(expression(expressionContext))
	  File "/home/pab/.buildout/eggs/Zope2-2.13.20-py2.7.egg/Products/PageTemplates/ZRPythonExpr.py", line 48, in __call__
	    return eval(self._code, vars, {})
	  File "PythonExpr", line 1, in <expression>
	  File "/home/pab/.buildout/eggs/plone.memoize-1.1.1-py2.7.egg/plone/memoize/view.py", line 47, in memogetter
	    value = cache[key] = func(*args, **kwargs)
	  File "/home/pab/.buildout/eggs/plone.app.layout-2.3.5-py2.7.egg/plone/app/layout/globals/context.py", line 47, in current_base_url
	    self.context.absolute_url())))
	AttributeError: 'FilesystemResourceDirectory' object has no attribute 'absolute_url'

**Reason**: There is a not accessible filesystem resource declared in your diazo theme's html.

**Solution**: Check that all js and css files are available.

AttributeError: 'RelationList' object has no attribute 'source'
---------------------------------------------------------------

**Traceback**::

    2014-03-21 17:19:09 ERROR Zope.SiteErrorLog 1395433149.260.697467198696 http://localhost:8080/Plone/++add++MyType
    Traceback (innermost last):
      Module ZPublisher.Publish, line 138, in publish
      Module ZPublisher.mapply, line 77, in mapply
      Module ZPublisher.Publish, line 48, in call_object
      Module plone.z3cform.layout, line 66, in __call__
      Module plone.z3cform.layout, line 50, in update
      Module plone.dexterity.browser.add, line 112, in update
      Module plone.z3cform.fieldsets.extensible, line 59, in update
      Module plone.z3cform.patch, line 30, in GroupForm_update
      Module z3c.form.group, line 128, in update
      Module z3c.form.form, line 134, in updateWidgets
      Module z3c.form.field, line 277, in update
      Module z3c.formwidget.query.widget, line 108, in update
      Module z3c.formwidget.query.widget, line 95, in bound_source
      Module z3c.formwidget.query.widget, line 90, in source
    AttributeError: 'RelationList' object has no attribute 'source'

**Reason**: You're trying to use a relation field on your Dexterity-based content type but
`plone.app.relationfield`_ is not installed.

**Solution**: Follow the instructions on the Dexterity documentation as
`relation support is no longer included by default`_.

.. _`plone.app.relationfield`: https://pypi.python.org/pypi/plone.app.relationfield
.. _`relation support is no longer included by default`: https://pypi.python.org/pypi/plone.app.dexterity#relation-support-no-longer-included-by-default

AttributeError: 'module' object has no attribute 'HTTPSConnection'
--------------------------------------------------------------------

Python has not been compiled with HTTPS support.

Try installing your Python, for example, using minitage.

See :doc:`Python basics </develop/plone/getstarted/python>`.


AttributeError: 'str' object has no attribute 'other' (Mixed zope.viewpagetemplate and Five.viewpagetemplate)
--------------------------------------------------------------------------------------------------------------

**Traceback**::

    Module zope.tales.tales, line 696, in evaluate
     - URL: /home/moo/sits/src/plone.z3cform/plone/z3cform/crud/crud-master.pt
     - Line 17, Column 2
     - Expression: <PathExpr standard:u'form/render'>
     - Names:
        {'args': (),
         'context': <SitsPatient at /folder_sits/sitsngta/intranet/sitsdatabase/sitscountry_TE/sitshospital_TES/sitspatient.TETES2009062217>,
         'default': <object object at 0xb7d76538>,
         'loop': {},
         'nothing': None,
         'options': {},
         'repeat': {},
         'request': <HTTPRequest, URL=http://localhost:9000/folder_sits/sitsngta/intranet/sitsdatabase/sitscountry_TE/sitshospital_TES/sitspatient.TETES2009062217/@@ar>,
         'template': <zope.app.pagetemplate.viewpagetemplatefile.ViewPageTemplateFile object at 0xc6e552c>,
         'usage': <zope.pagetemplate.pagetemplate.TemplateUsage object at 0xf7fb78c>,
         'view': <Products.SitsPatient.browser.ar.ARCrudForm object at 0xf928ccc>,
         'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0xf7b4a0c>}
    Module Products.PTProfiler.ProfilerPatch, line 32, in __patched_call__
    Module zope.tales.expressions, line 217, in __call__
    Module zope.tales.expressions, line 211, in _eval
    Module z3c.form.form, line 143, in render
    Module Shared.DC.Scripts.Bindings, line 313, in __call__
    Module Shared.DC.Scripts.Bindings, line 348, in _bindAndExec
    Module Shared.DC.Scripts.Bindings, line 1, in ?
    Module Shared.DC.Scripts.Bindings, line 293, in _getTraverseSubpath
    AttributeError: 'str' object has no attribute 'other'

Five ViewPageTemplate class file is slightly different than Zope 3's normal ViewPageTemplate file.
In this case Five ViewPageTemplate was used, when Zope 3's normal ViewPageTemplate was expected.

Another reason is that acquisition chain is not properly set-up in your custom views.

Difference::

    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

vs.::

    from zope.pagetemplate.pagetemplatefile import PageTemplateFile

AttributeError: 'wrapper_descriptor' object has no attribute 'im_func'
------------------------------------------------------------------------

**Traceback**::

    File "/home/moo/code/gomobile/parts/zope2/lib/python/DocumentTemplate/DT_Util.py", line 19, in <module>
      from html_quote import html_quote, ustr # for import by other modules, dont remove!
    File "/home/moo/code/gomobile/parts/zope2/lib/python/DocumentTemplate/html_quote.py", line 4, in <module>
      from ustr import ustr
    File "/home/moo/code/gomobile/parts/zope2/lib/python/DocumentTemplate/ustr.py", line 18, in <module>
      nasty_exception_str = Exception.__str__.im_func
    AttributeError: 'wrapper_descriptor' object has no attribute 'im_func'

**Condition**: This exception happens when starting Plone

**Reason**: You are trying to use Python 2.6 with Plone 3

**Solution**: With Plone 3 you need to use Python 2.4.

AttributeError: REQUEST in getObject
------------------------------------

**Traceback**::

    import ZPublisher, Zope
    Traceback (most recent call last):
      File "<string>", line 1, in ?
      File "src/collective.mountpoint/collective/mountpoint/bin/update.py", line 31, in ?
        sys.exit(main(app))
      File "/srv/plone/saariselka/src/collective.mountpoint/collective/mountpoint/updateclient.py", line 243, in main
        exit_code = updater.updateAll()
      File "/srv/plone/saariselka/src/collective.mountpoint/collective/mountpoint/updateclient.py", line 151, in updateAll
        mountpoints = list(self.getMountPoints())
      File "/srv/plone/saariselka/src/collective.mountpoint/collective/mountpoint/updateclient.py", line 49, in getMountPoints
        return [ brain.getObject() for brain in brains ]
      File "/srv/plone/saariselka/parts/zope2/lib/python/Products/ZCatalog/CatalogBrains.py", line 86, in getObject
        target = parent.restrictedTraverse(path[-1])
      File "/srv/plone/saariselka/parts/zope2/lib/python/OFS/Traversable.py", line 301, in restrictedTraverse
        return self.unrestrictedTraverse(path, default, restricted=True)
      File "/srv/plone/saariselka/parts/zope2/lib/python/OFS/Traversable.py", line 259, in unrestrictedTraverse
        next = queryMultiAdapter((obj, self.REQUEST),
    AttributeError: REQUEST

**Reason**: You are using command line script. getObject() fails for a catalog
brain, because the actual object is gone. However, unrestrictedTraverse()
does not handle this case gracefully.

AttributeError: Schema
-----------------------

**Traceback**::

    Module zope.tales.tales, line 696, in evaluate
     - URL: file:/fast/xxxm2011/eggs/Products.Archetypes-1.7.10-py2.6.egg/Products/Archetypes/skins/archetypes/base_view.pt
     - Line 50, Column 4
     - Expression: <PythonExpr context.Schema().viewableFields(here)>
     - Names:
        {'container': <CourseInfo at /xxx/courses/professional-courses/business-management-courses/postgraduate-diploma-in-business-and-management-consultancy>,
         'context': <CourseInfo at /xxx/courses/professional-courses/business-management-courses/postgraduate-diploma-in-business-and-management-consultancy>,
         'default': <object object at 0x1002edb70>,
         'here': <CourseInfo at /xxx/courses/professional-courses/business-management-courses/postgraduate-diploma-in-business-and-management-consultancy>,
         'loop': {},
         'nothing': None,
         'options': {'args': ()},
         'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x10b70a208>,
         'request': <HTTPRequest, URL=http://localhost:8090/xxx/courses/professional-courses/business-management-courses/postgraduate-diploma-in-business-and-management-consultancy/base_view>,
         'root': <Application at >,
         'template': <FSPageTemplate at /xxx/courses/professional-courses/business-management-courses/postgraduate-diploma-in-business-and-management-consultancy/base_view>,
         'traverse_subpath': [],
         'user': <PropertiedUser 'admin'>}
    Module Products.PageTemplates.ZRPythonExpr, line 48, in __call__
     - __traceback_info__: context.Schema().viewableFields(here)
    Module PythonExpr, line 1, in <expression>
    Module AccessControl.ImplPython, line 675, in guarded_getattr

**Condition**: This error may comes when you try to view your custom content type

**Reason**: It is picking up Archetypes default view template for your Dexterity content type.

Try if you can access your view by a directly calling it to by its name. E.g.::

  http://yoursite.com/folder/content/@@view

If it's working then it is wrong data in *portal_types*.

Your content item might also be corrupted. It is trying to use dynamic view selector even if it's not supported. Try re-creating
the particular content item.

AttributeError: getPhysicalPath()
----------------------------------

**Traceback**::

	Module zope.tal.talinterpreter, line 408, in do_startTag
	Module zope.tal.talinterpreter, line 485, in attrAction_tal
	Module Products.PageTemplates.Expressions, line 230, in evaluateText
	Module zope.tales.tales, line 696, in evaluate
	 - URL: edit_header
	 - Line 25, Column 14
	 - Expression: <PythonExpr (view.getHeaderDefiner().absolute_url())>
	 - Names:
	    {'container': <Frontpage at /yourinstance/matkailijalle/yourinstance-1>,
	     'context': <Frontpage at /yourinstance/matkailijalle/yourinstance-1>,
	     'default': <object object at 0x7fabf9cec1f0>,
	     'here': <Frontpage at /yourinstance/matkailijalle/yourinstance-1>,
	     'loop': {},
	     'nothing': None,
	     'options': {'args': ()},
	     'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0xe617d88>,
	     'request': <HTTPRequest, URL=http://localhost:9444/yourinstance/matkailijalle/yourinstance-1/@@edit_header>,
	     'root': <Application at >,
	     'template': <ImplicitAcquirerWrapper object at 0xe6105d0>,
	     'traverse_subpath': [],
	     'user': <PropertiedUser 'admin'>,
	     'view': <Products.Five.metaclass.EditHeaderBehaviorView object at 0xe51ed10>,
	     'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0xe610c10>}
	Module zope.tales.pythonexpr, line 59, in __call__
	 - __traceback_info__: (view.getHeaderDefiner().absolute_url())
	Module <string>, line 0, in ?
	Module OFS.Traversable, line 64, in absolute_url
	Module OFS.Traversable, line 117, in getPhysicalPath
	AttributeError: getPhysicalPath

Another possible error is::

	AttributeError: absolute_url

This usually means that you should have used context.aq_inner when you have used context.
absolute_url() tries to get the path to the object, but object parent is set to view (context.aq_parent)
instead of real container object (context.aq_inner.aq_parent).

.. warning::

	When setting a member attribute in BrowserView, the acquisition parent of objects changes to BrowserView instance.
	All member attributes receive ImplicitAcquisitionWrapper automatically.

**Demonstration**

We try to set BrowserView member attribute defining_context to be some context object.::

	(Pdb) self.defining_context = context
	(Pdb) context.aq_parent
	<PloneSite at /plone>
	(Pdb) self.defining_context.aq_parent
	<Products.Five.metaclass.HeaderAnimationHelper object at 0xadb5750>
	(Pdb) self.defining_context.aq_inner.aq_parent
	<Products.Five.metaclass.HeaderAnimationHelper object at 0xadb5750>
	(Pdb) self.defining_context.aq_parent.aq_parent
	<ATDocument at /plone/doc>
	(Pdb) self.defining_context.aq_parent.aq_parent.aq_inner
	<ATDocument at /plone/doc>
	(Pdb) self.defining_context.aq_parent.aq_parent.aq_parent
	<PloneSite at /plone>

To get the real object (as it was before set was called) you can create a helper getter::

    def getDefiningContext(self):
        """
        Un-fuse automatically injected view from the acquisition chain

        @return: Real defining context object without bad acquistion
        """
        if self.defining_context is not None:
            return self.defining_context.aq_parent.aq_inner.aq_parent
        return None

AttributeError: type object 'IRAMCache' has no attribute '__iro__'
-------------------------------------------------------------------

**Traceback**::

    Module zope.component._api, line 130, in subscribers
    Module zope.component.registry, line 290, in subscribers
    Module zope.interface.adapter, line 535, in subscribers
    Module zope.app.component.site, line 375, in threadSiteSubscriber
    Module zope.app.component.hooks, line 61, in setSite
    Module Products.CMFCore.PortalObject, line 75, in getSiteManager
    Module ZODB.Connection, line 811, in setstate
    Module ZODB.Connection, line 870, in _setstate
    Module ZODB.serialize, line 605, in setGhostState
    Module zope.component.persistentregistry, line 42, in __setstate__
    Module zope.interface.adapter, line 80, in _createLookup
    Module zope.interface.adapter, line 389, in __init__
    Module zope.interface.adapter, line 426, in init_extendors
    Module zope.interface.adapter, line 430, in add_extendor
    AttributeError: type object 'IRAMCache' has no attribute '__iro__'

**Condition**: This error can happen when trying to open any page

**Reason**: You have probably imported a Data.fs using newer Plone/Zope version to old Plone, or
package pindowns are incorrect. If you are copying a site try re-checking that
source and target buildouts and package versions match.

AttributeError: set_stripped_tags
---------------------------------

**Traceback**::

    ...
    Module ZPublisher.Publish, line 60, in publish
    Module ZPublisher.mapply, line 77, in mapply
    Module ZPublisher.Publish, line 46, in call_object
    Module zope.formlib.form, line 795, in __call__
    Module five.formlib.formbase, line 50, in update
    Module zope.formlib.form, line 776, in update
    Module zope.formlib.form, line 620, in success
    Module plone.app.controlpanel.form, line 38, in handle_edit_action
    Module zope.formlib.form, line 543, in applyChanges
    Module zope.formlib.form, line 538, in applyData
    Module zope.schema._bootstrapfields, line 227, in set
    Module plone.app.controlpanel.filter, line 173, in set_
    AttributeError: set_stripped_tags

**Condition**: This error may happen on saving changed settings in the HTML-Filtering controlpanel.

possible cause:

* You have migrated your Plone site from 3.3.5 to Plone 4.x

* For some reason kupu library tool may not be removed in the upgrade step that removed kupu.

**Solution**: Go to the Management Interface and delete the kupu library tool manually.

AttributeError: set_stripped_combinations
-----------------------------------------

**Traceback**::

    ...
    Module ZPublisher.Publish, line 126, in publish
    Module ZPublisher.mapply, line 77, in mapply
    Module ZPublisher.Publish, line 46, in call_object
    Module zope.formlib.form, line 795, in __call__
    Module five.formlib.formbase, line 50, in update
    Module zope.formlib.form, line 776, in update
    Module zope.formlib.form, line 620, in success
    Module plone.app.controlpanel.form, line 38, in handle_edit_action
    Module zope.formlib.form, line 543, in applyChanges
    Module zope.formlib.form, line 538, in applyData
    Module zope.schema._bootstrapfields, line 227, in set
    Module plone.app.controlpanel.filter, line 254, in set
    AttributeError: set_stripped_combinations

**Condition**: This error may happen on saving changed settings in the HTML-Filtering controlpanel.

possible cause:

* You have migrated your Plone site from 3.3.5 to Plone 4.x

* For some reason kupu library tool may not be removed in the upgrade step that removed kupu.

**Solution**: Go to the Management Interface and delete the kupu library tool manually.

BadRequest: The id "xxx" is invalid - it is already in use.
------------------------------------------------------------------

**Traceback**::

        ...
        Module Products.CMFFormController.Script, line 145, in __call__
        Module Products.CMFCore.FSPythonScript, line 140, in __call__
        Module Shared.DC.Scripts.Bindings, line 313, in __call__
        Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
        Module Products.CMFCore.FSPythonScript, line 196, in _exec
        Module None, line 1, in content_edit
        <FSControllerPythonScript at /xxx/content_edit used for /xxx/sisalto/lomapalvelut/portal_factory/HolidayService/aktiviteetit>
        Line 1
        Module Products.CMFCore.FSPythonScript, line 140, in __call__
        Module Shared.DC.Scripts.Bindings, line 313, in __call__
        Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
        Module Products.CMFCore.FSPythonScript, line 196, in _exec
        Module None, line 9, in content_edit_impl
        <FSPythonScript at /xxx/content_edit_impl used for /xxx/sisalto/lomapalvelut/portal_factory/HolidayService/aktiviteetit>
        Line 9
        Module Products.CMFPlone.FactoryTool, line 264, in doCreate
        Module Products.ATContentTypes.lib.constraintypes, line 281, in invokeFactory
        Module Products.CMFCore.PortalFolder, line 315, in invokeFactory
        Module Products.CMFCore.TypesTool, line 716, in constructContent
        Module Products.CMFCore.TypesTool, line 276, in constructInstance
        Module Products.CMFCore.TypesTool, line 450, in _constructInstance
        Module xxx.app.content.holidayservice, line 7, in addHolidayService
        Module OFS.ObjectManager, line 315, in _setObject
        Module Products.CMFCore.PortalFolder, line 333, in _checkId
        Module OFS.ObjectManager, line 102, in checkValidId
        BadRequest: The id "holidayservice.2010-03-18.4474765045" is invalid - it is already in use.

.. TODO:: Not really sure why this happens.

Try portal_catalog rebuild as a fix.

ComponentLookupError: cmf.ManagePortal
--------------------------------------

**Traceback**::

	zope.configuration.config.ConfigurationExecutionError: <class 'zope.component.interfaces.ComponentLookupError'>: (<InterfaceClass zope.security.interfaces.IPermission>, u'cmf.ManagePortal')
	  in:
	  File "/fast/x/src/collective.portletcollection/collective/portletcollection/portlets/configure.zcml", line 11.2-20.8

**Condition**: This error may happen when starting Plone

This is a sign of changed loading order, starting from Plone 4.1.
You need to explicitly include *CMFCore/permissions.zcml* in your *configuration.zcml*.

Example::

	<include package="Products.CMFCore" file="permissions.zcml" />


Content status history won't render - traceback is content path reversed
------------------------------------------------------------------------

**Traceback**::

    Module zope.tales.tales, line 696, in evaluate
     - URL: file:/home/antti/workspace/plone/hotellilevitunturi/eggs/Plone-3.3.5-py2.4.egg/Products/CMFPlone/skins/plone_forms/content_status_history.cpt
     - Line 201, Column 14
     - Expression: <PythonExpr wtool.getTransitionsFor(target, here)>
     - Names:
        {'container': <PloneSite at /hotellilevitunturi>,
         'context': <MainFolder at /hotellilevitunturi/fi/ravintolamaailma>,
         'default': <object object at 0xb75d2540>,
         'here': <MainFolder at /hotellilevitunturi/fi/ravintolamaailma>,
         'loop': {},
         'nothing': None,
         'options': {'args': (),
                     'state': <Products.CMFFormController.ControllerState.ControllerState object at 0x1055614c>},
         'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x10556f6c>,
         'request': <HTTPRequest, URL=http://localhost:9888/hotellilevitunturi/fi/ravintolamaailma/content_status_history>,
         'root': <Application at >,
         'template': <FSControllerPageTemplate at /hotellilevitunturi/content_status_history used for /hotellilevitunturi/fi/ravintolamaailma>,
         'traverse_subpath': [],
         'user': <PropertiedUser 'admin'>}
    Module Products.PageTemplates.ZRPythonExpr, line 49, in __call__
     - __traceback_info__: wtool.getTransitionsFor(target, here)
    Module PythonExpr, line 1, in <expression>
    Module Products.CMFPlone.WorkflowTool, line 88, in getTransitionsFor
    Module Products.CMFPlone.WorkflowTool, line 37, in flattenTransitions
    Module Products.CMFPlone.WorkflowTool, line 69, in flattenTransitionsForPaths
    Module OFS.Traversable, line 301, in restrictedTraverse
    Module OFS.Traversable, line 284, in unrestrictedTraverse
     - __traceback_info__: ([u's', u'a', u'n', u'u', u'o', u'l', u'/', u'a', u'm', u'l', u'i', u'a', u'a', u'm', u'a', u'l', u'o', u't', u'n', u'i', u'v', u'a', u'r', u'/', u'i', u'f', u'/', u'i', u'r', u'u', u't', u'n', u'u', u't', u'i', u'v', u'e', u'l', u'i', u'l', u'l', u'e', u't', u'o', u'h'], u'/')
    KeyError: u'/'

.. TODO:: No solution

ContentProviderLookupError: plone.htmlhead
------------------------------------------

**Traceback**::

    Module zope.tales.tales, line 696, in evaluate
     - URL: file:/home/moo/isleofback/eggs/Plone-3.3.5-py2.4.egg/Products/CMFPlone/skins/plone_templates/main_template.pt
     - Line 39, Column 4
     - Expression: <StringExpr u'plone.htmlhead'>
     - Names:
        {'container': <PloneSite at /isleofback>,
         'context': <PloneSite at /isleofback>,
         'default': <object object at 0xb75f2528>,
         'here': <PloneSite at /isleofback>,
         'loop': {},
         'nothing': None,
         'options': {'args': (<isleofback.app.browser.company.CompanyCreationForm object at 0xea5e80c>,)},
         'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0xea62dcc>,
         'request': <HTTPRequest, URL=http://localhost:9666/isleofback/@@create_company>,
         'root': <Application at >,
         'template': <ImplicitAcquirerWrapper object at 0xea62bcc>,
         'traverse_subpath': [],
         'user': <PropertiedUser 'admin'>,
         'view': <UnauthorizedBinding: context>,
         'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0xea62d2c>}
    Module Products.Five.browser.providerexpression, line 25, in __call__
    ContentProviderLookupError: plone.htmlhead

This is not a bug in Zope. It is caused by trying to render a Plone page frame in an context
which has not acquisition chain properly set up. Plone ``main_template.pt``
tries to look up viewlet managers by
acquistion traversing to parent objects. ``plone.htmlhead`` is the first viewlet manager to
be looked up like this, and it will fail firstly.

Some possible causes:

* You are trying to embed main_template inside form/view which is already rendered in main_template frame.
  Please see how to :doc:`embed forms and wrap forms manually </develop/plone/forms/z3c.form>`.

* You might be using wrong ViewPageTemplate import (Five vs. zope.pagetemplate - explained elsewhere in this documentation)

* Make sure that you call __of__() method for views and other objects you construct by hand
  which expects themselves to be in the acquisition chain (normally discovered by traversing)

.. seealso::
    https://bugs.launchpad.net/zope2/+bug/176566

ERROR ZODB.Connection Couldn't load state for 0x00
--------------------------------------------------

**Traceback**::

	2010-07-14 05:02:33 ERROR ZODB.Connection Couldn't load state for 0x00
	Traceback (most recent call last):
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/Connection.py", line 811, in setstate
	    self._setstate(obj)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/Connection.py", line 870, in _setstate
	    self._reader.setGhostState(obj, p)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/serialize.py", line 604, in setGhostState
	    state = self.getState(pickle)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/serialize.py", line 597, in getState
	    return unpickler.load()
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/serialize.py", line 471, in _persistent_load
	    return self.load_oid(reference)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/serialize.py", line 537, in load_oid
	    return self._conn.get(oid)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/Connection.py", line 244, in get
	    p, serial = self._storage.load(oid, self._version)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/FileStorage/FileStorage.py", line 470, in load
	    pos = self._lookup_pos(oid)
	  File "/Users/moo/yourinstance/eggs/ZODB3-3.8.4-py2.4-macosx-10.6-i386.egg/ZODB/FileStorage/FileStorage.py", line 462, in _lookup_pos
	    raise POSKeyError(oid)
	POSKeyError: 0x01

**Condition**: This error can happen when you try to start Zope

**Reason**: Data.fs might have been damaged. You might be using blobs with Plone 3 and they don't work perfectly.
. . . or a bunch other issues which generally mean that your day is screwed.

.. seealso::
    http://plonechix.blogspot.com/2009/12/definitive-guide-to-poskeyerror.html

Error _restore_index() when starting instance / ZEO server
----------------------------------------------------------

**Traceback**::

    2011-05-09 09:42:20 INFO ZServer HTTP server started at Mon May  9 09:42:20 2011
            Hostname: 0.0.0.0
            Port: 10997
    2011-05-09 09:42:21 INFO Marshall libxml2-python not available. Unable to register libxml2 based marshallers, at least SimpleXMLMarshaller
    2011-05-09 09:42:22 INFO DocFinderTab Applied patch version 1.0.4.
    Traceback (most recent call last):
      File "/home/moo/code/python2/parts/opt/lib/python2.4/pdb.py", line 1066, in main
        pdb._runscript(mainpyfile)
      File "/home/moo/code/python2/parts/opt/lib/python2.4/pdb.py", line 991, in _runscript
        self.run(statement, globals=globals_, locals=locals_)
      File "/home/moo/code/python2/parts/opt/lib/python2.4/bdb.py", line 366, in run
        exec cmd in globals, locals
      File "<string>", line 1, in ?
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/run.py", line 56, in ?
        run()
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/run.py", line 21, in run
        starter.prepare()
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 102, in prepare
        self.startZope()
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 278, in startZope
        Zope2.startup()
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/__init__.py", line 47, in startup
        _startup()
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/App/startup.py", line 59, in startup
        DB = dbtab.getDatabase('/', is_root=1)
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/datatypes.py", line 280, in getDatabase
        db = factory.open(name, self.databases)
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/datatypes.py", line 178, in open
        DB = self.createDB(database_name, databases)
      File "/home/moo/xxx/parts/zope2/lib/python/Zope2/Startup/datatypes.py", line 175, in createDB
        return ZODBDatabase.open(self, databases)
      File "/home/moo/xxx/parts/zope2/lib/python/ZODB/config.py", line 97, in open
        storage = section.storage.open()
      File "/home/moo/xxx/parts/zope2/lib/python/ZODB/config.py", line 135, in open
        quota=self.config.quota)
      File "/home/moo/xxx/parts/zope2/lib/python/ZODB/FileStorage/FileStorage.py", line 154, in __init__
        r = self._restore_index()
      File "/home/moo/xxx/parts/zope2/lib/python/ZODB/FileStorage/FileStorage.py", line 365, in _restore_index
        index = info.get('index')

**Reason**: Data.fs.index is corrupted.

**Solution**: Remove Data.fs.index file. The index will be rebuilt on the launch.

Error: Incorrect padding
------------------------

**Traceback**::

	2012-02-06 16:52:25 ERROR Zope.SiteErrorLog 1328539945.430.234286547911 http://localhost:9888/index_html
	Traceback (innermost last):
	  Module ZPublisher.Publish, line 110, in publish
	  Module ZPublisher.BaseRequest, line 588, in traverse
	  Module Products.PluggableAuthService.PluggableAuthService, line 233, in validate
	  Module Products.PluggableAuthService.PluggableAuthService, line 559, in _extractUserIds
	  Module Products.PluggableAuthService.plugins.CookieAuthHelper, line 121, in extractCredentials
	  Module base64, line 321, in decodestring
	Error: Incorrect padding

**Condition**: This error can happen when you try to access any Plone site URL

**Reason**: It means that your browser most likely tries to serve bad
cookies / auth info to Zope.

**Solution**: Clear browser cache, cookies, etc.

Exception: Type name not specified in createObject
--------------------------------------------------

**Traceback**::

    Module ZPublisher.Publish, line 119, in publish
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 42, in call_object
    Module Products.CMFFormController.FSControllerPythonScript, line 104, in __call__
    Module Products.CMFFormController.Script, line 145, in __call__
    Module Products.CMFCore.FSPythonScript, line 140, in __call__
    Module Shared.DC.Scripts.Bindings, line 313, in __call__
    Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
    Module Products.CMFCore.FSPythonScript, line 196, in _exec
    Module None, line 11, in createObject
    <FSControllerPythonScript at /xxx/createObject used for /xxx/sisalto/lomapalvelut>
    Line 11
    Exception: Type name not specified

.. TODO:: Complete

ExpatError: portlets.xml: unbound prefix
----------------------------------------

**Traceback**::

    Traceback (innermost last):
      Module plone.postpublicationhook.hook, line 74, in publish
      Module ZPublisher.mapply, line 88, in mapply
      Module ZPublisher.Publish, line 42, in call_object
      Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 589, in installProducts
      Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 526, in installProduct
       - __traceback_info__: ('mfabrik.app',)
      Module Products.GenericSetup.tool, line 390, in runAllImportStepsFromProfile
       - __traceback_info__: profile-mfabrik.app:default
      Module Products.GenericSetup.tool, line 1179, in _runImportStepsFromContext
      Module Products.GenericSetup.tool, line 1090, in _doRunImportStep
       - __traceback_info__: portlets
      Module plone.app.portlets.exportimport.portlets, line 707, in importPortlets
      Module Products.GenericSetup.utils, line 543, in _importBody
    ExpatError: portlets.xml: unbound prefix: line 15, column 1

**Condition**: This error can happen while installing a new portlet portlets.xml

**Reason**: You have ``i18n:attributes="title; description"`` in your
portlets.xml.

**Solution**: Remove it or declare the i18n namespace in XML like this::

    <portlets xmlns:i18n="http://namespaces.zope.org/i18n">

Similar applies for actions.xml, etc.

IOError: [Errno url error] unknown url type: 'https'
----------------------------------------------------

**Traceback**::

    File "/home/moo/code/python/parts/opt/lib/python2.4/urllib.py", line 89, in urlretrieve
      return _urlopener.retrieve(url, filename, reporthook, data)
    File "/home/moo/code/python/parts/opt/lib/python2.4/urllib.py", line 222, in retrieve
      fp = self.open(url, data)
    File "/home/moo/code/python/parts/opt/lib/python2.4/urllib.py", line 187, in open
      return self.open_unknown(fullurl, data)
    File "/home/moo/code/python/parts/opt/lib/python2.4/urllib.py", line 199, in open_unknown
      raise IOError, ('url error', 'unknown url type', type)
    IOError: [Errno url error] unknown url type: 'https'

**Reason**: Python and Python socket modules have not been compiled with SSL support.

**Solution**: Make sure that you have SSL development libraries installed (Ubuntu/Debian example)

.. code-block:: console

        sudo apt-get install libssl-dev

Make sure that Python is built with SSL support

.. code-block:: console

        ./configure --with-package=_ssl

You can test Python after compilation::

        moo@murskaamo:~/code/python$ source python-2.4/bin/activate
        (python-2.4)moo@murskaamo:~/code/python$ python
        Python 2.4.6 (#1, Jul 16 2010, 10:31:46)
        [GCC 4.4.3] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import _ssl
        >>>

Also you might want try

.. code-block:: console

        easy_install pyopenssl

ImportError: Couldn't import ZPublisherEventsBackport
-----------------------------------------------------

The following traceback on instance start-up::

    File "/Users/moo/twinapex/parts/zope2/lib/python/zope/configuration/config.py", line 1383, in toargs
      args[str(name)] = field.fromUnicode(s)
    File "/Users/moo/twinapex/parts/zope2/lib/python/zope/configuration/fields.py", line 141, in fromUnicode
      raise schema.ValidationError(v)
    zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "/Users/moo/twinapex/parts/instance/etc/site.zcml", line 14.2-14.55
        ZopeXMLConfigurationError: File "/Users/moo/twinapex/parts/instance/etc/package-includes/009-gomobile.mobile-configure.zcml", line 1.0-1.59
        ZopeXMLConfigurationError: File "/Users/moo/twinapex/src/gomobile.mobile/gomobile/mobile/configure.zcml", line 15.4-15.51
        ZopeXMLConfigurationError: File "/Users/moo/twinapex/eggs/plone.postpublicationhook-1.1-py2.4.egg/plone/postpublicationhook/configure.zcml", line 5.4-8.10
        ConfigurationError: ('Invalid value for', 'package', "ImportError: Couldn't import ZPublisherEventsBackport, No module named ZPublisherEventsBackport")

**Reason**: plone.postpublicationhook 1.1 depends on new package, ZPublisherEventsBackport, for Plone 3.3.

**Solution**: You eed to include them both in your buildout.
You need to include both eggs::

    eggs =
            ZPublisherEventsBackport
            plone.postpublicationhook

ImportError: Inappropriate file type for dynamic loading
--------------------------------------------------------

**Traceback**::

    File "/Users/moo/twinapex/twinapex/parts/zope2/lib/python/ZConfig/datatypes.py", line 398, in get
      t = self.search(name)
    File "/Users/moo/twinapex/twinapex/parts/zope2/lib/python/ZConfig/datatypes.py", line 423, in search
      package = __import__(n, g, g, component)
    File "/Users/moo/twinapex/twinapex/parts/zope2/lib/python/Zope2/Startup/datatypes.py", line 20, in ?
      from ZODB.config import ZODBDatabase
    File "/Users/moo/twinapex/twinapex/eggs/ZODB3-3.8.2-py2.4-macosx-10.6-i386.egg/ZODB/__init__.py", line 20, in ?
      from persistent import TimeStamp
    File "/Users/moo/twinapex/twinapex/eggs/ZODB3-3.8.2-py2.4-macosx-10.6-i386.egg/persistent/__init__.py", line 19, in ?
      from cPersistence import Persistent, GHOST, UPTODATE, CHANGED, STICKY
    ImportError: Inappropriate file type for dynamic loading

**Condition**: When starting Zope

**Reason**: You probably have files lying over from wrong CPU architecture

* Hand copied eggs between servers

* Migrated OS to new version

* You have several Python interpreters installed and you try to run Zope using
  the wrong interpreter (the one which the code is not compiled for)

**Solution**: Delete /parts and /eggs buildout folders,
run bootstrap, run buildout.

ImportError: No module named PIL
--------------------------------

**Traceback**::

    ...
    Traceback (most recent call last):
      File "/home/moo/isleofback/bin/idelauncher.py", line 140, in ?
        execfile(ZOPE_RUN)
      File "/home/moo/isleofback/bin/../parts/zope2/lib/python/Zope2/Startup/run.py", line 56, in ?
        run()
      File "/home/moo/isleofback/bin/../parts/zope2/lib/python/Zope2/Startup/run.py", line 21, in run
        starter.prepare()
      File "/home/moo/isleofback/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 102, in prepare
        self.startZope()
      File "/home/moo/isleofback/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 278, in startZope
        Zope2.startup()
      File "/home/moo/isleofback/parts/zope2/lib/python/Zope2/__init__.py", line 47, in startup
        _startup()
      File "/home/moo/isleofback/parts/zope2/lib/python/Zope2/App/startup.py", line 45, in startup
        OFS.Application.import_products()
      File "/home/moo/isleofback/parts/zope2/lib/python/OFS/Application.py", line 686, in import_products
        import_product(product_dir, product_name, raise_exc=debug_mode)
      File "/home/moo/isleofback/parts/zope2/lib/python/OFS/Application.py", line 709, in import_product
        product=__import__(pname, global_dict, global_dict, silly)
      File "/home/moo/isleofback/eggs/Products.ATContentTypes-1.3.4-py2.4.egg/Products/ATContentTypes/__init__.py", line 64, in ?
        import Products.ATContentTypes.content
      File "/home/moo/isleofback/eggs/Products.ATContentTypes-1.3.4-py2.4.egg/Products/ATContentTypes/content/__init__.py", line 26, in ?
        import Products.ATContentTypes.content.link
      File "/home/moo/isleofback/eggs/Products.ATContentTypes-1.3.4-py2.4.egg/Products/ATContentTypes/content/link.py", line 39, in ?
        from Products.ATContentTypes.content.base import registerATCT
      File "/home/moo/isleofback/eggs/Products.ATContentTypes-1.3.4-py2.4.egg/Products/ATContentTypes/content/base.py", line 63, in ?
        from Products.CMFPlone.PloneFolder import ReplaceableWrapper
      File "/home/moo/isleofback/eggs/Plone-3.3.5-py2.4.egg/Products/CMFPlone/__init__.py", line 215, in ?
        from browser import ploneview
      File "/home/moo/isleofback/eggs/Plone-3.3.5-py2.4.egg/Products/CMFPlone/browser/ploneview.py", line 12, in ?
        from Products.CMFPlone import utils
      File "/home/moo/isleofback/eggs/Plone-3.3.5-py2.4.egg/Products/CMFPlone/utils.py", line 6, in ?
        from PIL import Image
    ImportError: No module named PIL

**Reason**: Python Imaging Library is not properly installed. The default PIL
package does not work nicely as egg.

**Solution**: Remove all existing PIL eggs from buildout/eggs folder.

Install PIL for your development Python environment::

        easy_install http://dist.repoze.org/PIL-1.1.6.tar.gz

ImportError: No module named html
---------------------------------

**Traceback**::

    from lxml.html import defs
    zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "/srv/plone/yourinstance/parts/client1/etc/site.zcml", line 14.2-14.55
    ZopeXMLConfigurationError: File "/srv/plone/yourinstance/parts/client1/etc/package-includes/012-yourinstance.mobi-configure.zcml", line 1.0-1.59
    ZopeXMLConfigurationError: File "/srv/plone/yourinstance/src/yourinstance.mobi/yourinstance/mobi/configure.zcml", line 13.2-13.43
    ZopeXMLConfigurationError: File "/srv/plone/yourinstance/src/gomobiletheme.basic/gomobiletheme/basic/configure.zcml", line 16.2-16.39
    ZopeXMLConfigurationError: File "/srv/plone/yourinstance/src/gomobile.mobile/gomobile/mobile/configure.zcml", line 19.4-19.34
    ZopeXMLConfigurationError: File "/srv/plone/yourinstance/src/gomobile.mobile/gomobile/mobile/browser/configure.zcml", line 24.4-29.10
    ImportError: No module named html

**Condition**: This error can happen when starting an instance

**Reason**: The system lxml version is too old

Let's see if we are getting too old system wide lxml installation::


        plone@mansikki:/srv/plone/yourinstance$ python2.4
        Python 2.4.5 (#2, Jan 21 2010, 20:05:55)
        [GCC 4.2.4 (Ubuntu 4.2.4-1ubuntu3)] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import lxml
        >>> lxml.__file__
        '/usr/lib/python2.4/site-packages/lxml/__init__.pyc'
        >>> dir(lxml)
        ['__builtins__', '__doc__', '__file__', '__name__', '__path__']
        >>> from lxml import html
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ImportError: cannot import name html


If we cannot fix the system lxml (your system software depends on it) the only workaround is to
create virtualenv. We cannot force Python 2.6, 2.5 or 2.4 not to use system libraries.

Example::

        root@mansikki:/srv/plone# virtualenv -p /usr/bin/python2.4 --no-site-packages py24

Include standalone lxml + libxml compilation in your ``buildout.cfg``::

        parts =
                ...
                lxml

        [lxml]
        recipe = z3c.recipe.staticlxml
        egg = lxml==2.2.6
        force = false

If there are exiting lxml builds in buildout be sure they are removed::

        rm -rf eggs/lxml*

Then as the non-root re-bootstrap the buildout using non-system wide Python::

        plone@mansikki:/srv/plone/yourinstance-2010/yourinstance$ source /srv/plone/py24/bin/activate
        (py24)plone@mansikki:/srv/plone/yourinstance-2010/yourinstance$ python bootstrap.py
        ...
        (py24)plone@mansikki:/srv/plone/yourinstance-2010/yourinstance$ bin/buildout
        ...

... and after this it should no longer pull the bad system lxml.


ImportError: No module named pkgutil
------------------------------------

**Traceback**::

    Traceback (most recent call last):
      File "/Users/moo/plonecommunity/bin/idelauncher.py", line 101, in <module>
        exec(data, globals())
      File "<string>", line 543, in <module>
      File "/Users/moo/plonecommunity/eggs/plone.app.z3cform-0.5.0-py2.6.egg/plone/__init__.py", line 5, in <module>
        from pkgutil import extend_path
    ImportError: No module named pkgutil

If you are using Eclipse, ``idelauncher.py`` has been updated for Plone 4.

Invalid or Duplicate property id
--------------------------------

**Traceback**::

    *   Dry run selected.
    * Starting the migration from version: 3.1.4
    * Attempting to upgrade from: 3.1.4
    * Upgrade aborted
    * Error type: zExceptions.BadRequest
    * Error value: Invalid or duplicate property id
    * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/MigrationTool.py",
    line 210, in upgrade newv, msgs = self._upgrade(newv)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/MigrationTool.py",
    line 321, in _upgrade res = function(self.aq_parent)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/migrations/v3_1/final_three1x.py",
    line 15, in three14_three15 loadMigrationProfile(portal,
    'profile-Products.CMFPlone.migrations:3.1.3-3.1.4')
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/migrations/migration_util.py",
    line 107, in loadMigrationProfile tool.runAllImportStepsFromProfile(profile,
    purge_old=False)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Products.GenericSetup-1.4.5-py2.4.egg/Products/GenericSetup/tool.py",
    line 390, in runAllImportStepsFromProfile
    ignore_dependencies=ignore_dependencies)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Products.GenericSetup-1.4.5-py2.4.egg/Products/GenericSetup/tool.py",
    line 1179, in _runImportStepsFromContext message =
    self._doRunImportStep(step, context)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Products.GenericSetup-1.4.5-py2.4.egg/Products/GenericSetup/tool.py",
    line 1090, in _doRunImportStep return handler(context)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/exportimport/propertiestool.py",
    line 37, in importPloneProperties importer.body = body
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Products.GenericSetup-1.4.5-py2.4.egg/Products/GenericSetup/utils.py",
    line 544, in _importBody self._importNode(dom.documentElement)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/exportimport/propertiestool.py",
    line 103, in _importNode self._initObjects(node)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/exportimport/propertiestool.py",
    line 154, in _initObjects importer.node = child
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Plone-3.3-py2.4.egg/Products/CMFPlone/exportimport/propertiestool.py",
    line 77, in _importNode self._initProperties(node)
        * File
    "/usr/local/Plone3.2.3/buildout-cache/eggs/Products.GenericSetup-1.4.5-py2.4.egg/Products/GenericSetup/utils.py",
    line 724, in _initProperties obj._setProperty(prop_id, val, prop_type)
        * File
    "/usr/local/Plone3.2.3/Zope-2.10.7-final-py2.4/lib/python/OFS/PropertyManager.py",
    line 186, in _setProperty raise BadRequest, 'Invalid or duplicate property
    id'
        * End of upgrade path, migration has finished
        * The upgrade path did NOT reach current version
        * Migration has failed
        * Dry run selected, transaction aborted

**Condition**: This exception can happen during Plone migration to the newer version

It is caused by a property (site setting) which already exists and migration tries to create it.
The usual reason is that one has edited site settings in new Plone version before running the migration.

Try remove violating property ids from the site_properties manually in Zope.

Potential candidates to be removed:

* enable_inline_editing

* lock_on_ttw_edit (boolean)

Potential candidates which need to be added manually:

* redirect_links (boolean)

.. seealso::
    http://www.mail-archive.com/setup@lists.plone.org/msg03988.html

InvalidInterface: Concrete attribute
------------------------------------

**Traceback**::

	/zope/interface/interface.py", line 495, in __init__
	    raise InvalidInterface("Concrete attribute, " + name)
	zope.configuration.xmlconfig.ZopeXMLConfigurationError: File "/Users/mikko/code/buildout.deco/parts/instance/etc/site.zcml", line 15.2-15.55
	    ZopeXMLConfigurationError: File "/Users/mikko/code/buildout.deco/parts/instance/etc/package-includes/002-plone.app.widgets-configure.zcml", line 1.0-1.61
	    ZopeXMLConfigurationError: File "/Users/mikko/code/buildout.deco/src/plone.app.widgets/plone/app/widgets/configure.zcml", line 56.2-62.6
	    InvalidInterface: Concrete attribute, multiChoiceCheckbox

**Condition**: Your ``zope.schema`` based schema breaks on Plone startup.

**Reason**: You have extra comma in your schema. Like this:

.. code-block:: python
    :emphasize-lines: 7

	class IChoiceExamples(model.Schema):

	    multiChoiceCheckbox = zope.schema.List(
	        title=u"Checkbox multiple choices",
	        description=u"Select multiple checkboxes using checkboxes and store values in zope.schema.List (maps to python List)." + DEFAULT_MUTABLE_WARNING,
	        required=False,
	        value_type=zope.schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes")),   # <---- This is the guilty comma

Iteration over non-sequence in _normalizeargs
---------------------------------------------

Case 1
~~~~~~

The following log trace will appear when you try to render
the site, but you can access the Management Interface normally::

    2009-09-23 20:47:18 WARNING OFS.Uninstalled Could not import class 'IPloneCommentsLayer' from module 'quintagroup.plonecomments.interfaces'
    2009-09-23 20:47:18 ERROR Zope.SiteErrorLog 1253728038.160.534632167217 http://localhost:9444/XXX
    Traceback (innermost last):
      Module plone.postpublicationhook.hook, line 65, in publish
      Module ZPublisher.BaseRequest, line 424, in traverse
      Module ZPublisher.BeforeTraverse, line 99, in __call__
      Module Products.CMFCore.PortalObject, line 94, in __before_publishing_traverse__
      Module zope.event, line 23, in notify
      Module zope.component.event, line 26, in dispatch
      Module zope.component._api, line 130, in subscribers
      Module zope.component.registry, line 290, in subscribers
      Module zope.interface.adapter, line 535, in subscribers
      Module zope.component.event, line 33, in objectEventNotify
      Module zope.component._api, line 130, in subscribers
      Module zope.component.registry, line 290, in subscribers
      Module zope.interface.adapter, line 535, in subscribers
      Module plone.browserlayer.layer, line 18, in mark_layer
      Module zope.interface.declarations, line 848, in directlyProvides
      Module zope.interface.declarations, line 1371, in _normalizeargs
      Module zope.interface.declarations, line 1370, in _normalizeargs
    TypeError: iteration over non-sequence
    2009-09-23 20:47:18 ERROR root Exception while rendering an error message
    Traceback (most recent call last):
      File "/home/moo/XXX/parts/zope2/lib/python/OFS/SimpleItem.py", line 227, in raise_standardErrorMessage
        v = s(**kwargs)
      File "/home/moo/workspace2/collective.skinny/collective/skinny/patch.py", line 8, in standard_error_message
        return self.restrictedTraverse('@@404.html')()
      File "/home/moo/workspace2/collective.skinny/collective/skinny/fourohfour.py", line 22, in __call__
        return skins.plone_templates.standard_error_message.__of__(
      File "/home/moo/XXX/eggs/Products.CMFCore-2.1.2-py2.4.egg/Products/CMFCore/FSPythonScript.py", line 140, in __call__
        return Script.__call__(self, *args, **kw)
      File "/home/moo/XXX/parts/zope2/lib/python/Shared/DC/Scripts/Bindings.py", line 313, in __call__
        return self._bindAndExec(args, kw, None)
      File "/home/moo/XXX/parts/zope2/lib/python/Shared/DC/Scripts/Bindings.py", line 350, in _bindAndExec
        return self._exec(bound_data, args, kw)
      File "/home/moo/XXX/eggs/Products.CMFCore-2.1.2-py2.4.egg/Products/CMFCore/FSPythonScript.py", line 196, in _exec
        result = f(*args, **kw)
      File "Script (Python)", line 27, in standard_error_message
    AttributeError: default_error_message

This usually means that you have copied Data.fs from another
system, but you do not have identical add-on product configuration
installed.

traceback to the console similar to the following if you have started Zope
process on foreground::

    2008-11-09 22:53:13 INFO Zope Ready to handle requests
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'ATSETemplateTool' from module 'Products.ATSchemaEditorNG.ATSETemplateTool'
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'SchemaEditorTool' from module 'Products.ATSchemaEditorNG.SchemaEditorTool'
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'SchemaManagerTool' from module 'Products.GenericPloneContent.SchemaManagerTool'
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'FormGenTool' from module 'Products.PloneFormGen.tools.formGenTool'
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'TemplatedDocument' from module 'collective.easytemplate.content.TemplatedDocument'
    2008-11-09 22:54:50 WARNING OFS.Uninstalled Could not import class 'FormFolder' from module 'Products.PloneFormGen.content.form'
    2008-11-09 22:54:52 WARNING OFS.Uninstalled Could not import class 'IDropdownSpecific' from module 'webcouturier.dropdownmenu.browser.interfaces'
    2008-11-09 22:54:52 ERROR Zope.SiteErrorLog http://localhost:8080/lsm
    Traceback (innermost last):
      Module ZPublisher.Publish, line 110, in publish
      Module ZPublisher.BaseRequest, line 424, in traverse
      Module ZPublisher.BeforeTraverse, line 99, in __call__
      Module Products.CMFCore.PortalObject, line 94, in __before_publishing_traverse__
      Module zope.event, line 23, in notify
      Module zope.component.event, line 26, in dispatch
      Module zope.component._api, line 130, in subscribers
      Module zope.component.registry, line 290, in subscribers
      Module zope.interface.adapter, line 535, in subscribers
      Module zope.component.event, line 33, in objectEventNotify
      Module zope.component._api, line 130, in subscribers
      Module zope.component.registry, line 290, in subscribers
      Module zope.interface.adapter, line 535, in subscribers
      Module plone.browserlayer.layer, line 18, in mark_layer
      Module zope.interface.declarations, line 848, in directlyProvides
      Module zope.interface.declarations, line 1371, in _normalizeargs
      Module zope.interface.declarations, line 1370, in _normalizeargs
    TypeError: iteration over non-sequence

notice the 'Could not import class' message.

**Reason**: You do not have identical product configuration on the new server.
Please install the missing products and site should work fine again.

Please note that you can get a 'TypeError: iteration over non-sequence'
exception in other contexts not related with missing products at all. Look
for the 'Could not import class' message in your traceback.

Case 2
~~~~~~

Example traceback::

        Traceback (most recent call last):
          File "/home/moo/twinapex/bin/idelauncher.py", line 158, in ?
            execfile(ZOPE_RUN)
          File "/home/moo/twinapex/bin/../parts/zope2/lib/python/Zope2/Startup/run.py", line 56, in ?
            run()
          File "/home/moo/twinapex/bin/../parts/zope2/lib/python/Zope2/Startup/run.py", line 21, in run
            starter.prepare()
          File "/home/moo/twinapex/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 102, in prepare
            self.startZope()
          File "/home/moo/twinapex/parts/zope2/lib/python/Zope2/Startup/__init__.py", line 278, in startZope
            Zope2.startup()
          File "/home/moo/twinapex/parts/zope2/lib/python/Zope2/__init__.py", line 47, in startup
            _startup()
          File "/home/moo/twinapex/parts/zope2/lib/python/Zope2/App/startup.py", line 45, in startup
            OFS.Application.import_products()
          File "/home/moo/twinapex/parts/zope2/lib/python/OFS/Application.py", line 686, in import_products
            import_product(product_dir, product_name, raise_exc=debug_mode)
          File "/home/moo/twinapex/parts/zope2/lib/python/OFS/Application.py", line 709, in import_product
            product=__import__(pname, global_dict, global_dict, silly)
          File "/home/moo/twinapex/eggs/Products.PloneHelpCenter-4.0a1-py2.4.egg/Products/PloneHelpCenter/__init__.py", line 9, in ?
            from Products.PloneHelpCenter import content
          File "/home/moo/twinapex/eggs/Products.PloneHelpCenter-4.0a1-py2.4.egg/Products/PloneHelpCenter/content/__init__.py", line 10, in ?
            import HowToFolder, HowTo
          File "/home/moo/twinapex/eggs/Products.PloneHelpCenter-4.0a1-py2.4.egg/Products/PloneHelpCenter/content/HowTo.py", line 40, in ?
            class HelpCenterHowTo(PHCContentMixin, ATCTOrderedFolder):
          File "/home/moo/twinapex/parts/zope2/lib/python/zope/interface/advice.py", line 132, in advise
            return callback(newClass)
          File "/home/moo/twinapex/parts/zope2/lib/python/zope/interface/declarations.py", line 485, in _implements_advice
            classImplements(cls, *interfaces)
          File "/home/moo/twinapex/parts/zope2/lib/python/zope/interface/declarations.py", line 462, in classImplements
            spec.declared += tuple(_normalizeargs(interfaces))
          File "/home/moo/twinapex/parts/zope2/lib/python/zope/interface/declarations.py", line 1372, in _normalizeargs
            _normalizeargs(v, output)
          File "/home/moo/twinapex/parts/zope2/lib/python/zope/interface/declarations.py", line 1371, in _normalizeargs
            for v in sequence:
        TypeError: iteration over non-sequence

Reason: You are trying to use Plone 4 (Zope 2.12) add-on on Plone 3 (Zope 2.10). Zope interface declarations have been changed.

**Solution 1**: Pick the older version for the add-on which is known to work with Plone 3. Make sure that you
delete all "too eggs" from ``eggs/`` and ``src/`` folders.

**Solution 2**: Upgrade your site to Plone.


NameError: name 'test' is not defined
-------------------------------------

**Condition**: This exception occurs when you try to customize TAL page template code using test() function.
test() function has been dropped in Zope 3 page templates. You should no longer
use test() function anywhere.

**Solution**: replace test() with common Python expression in your customized template.

For example the orignal::

    tal:attributes="class python:test(here.Format() in ('text/structured', 'text/x-rst', ), 'stx' + kss_class, 'plain', + kss_class)"

would need to be written as::

    tal:attributes="class python:here.Format() in ('text/structured', 'text/x-rst', ) and 'stx' + kss_class or 'plain' + kss_class"

NotFound error (Page not found) when accessing @@manage-portlets
----------------------------------------------------------------

If you get *Page not found* error when accessing @@manage-portlets the first thing
you need to do is to enable logging of NotFound exceptions in the Management Interface in error_log.

After that reload @@manage-portlets.

When you try to access @@manage-portlets an exception a NotFound exception is raised::

    2009-11-09 12:56:13 ERROR Zope.SiteErrorLog 1257764173.180.738005333766 http://localhost:8080/yourinstance/@@manage-portlets
    Traceback (innermost last):
      Module ZPublisher.Publish, line 119, in publish
        Module Products.PageTemplates.Expressions, line 223, in evaluateStructure
        ...
      Module zope.tales.tales, line 696, in evaluate
       - URL: file:/Users/moo/workspace/plonetheme.yourinstance/plonetheme/yourinstance/skins/plonetheme_yourinstance_custom_templates/main_template.pt
       - Line 92, Column 18
       - Expression: <StringExpr u'plone.leftcolumn'>
       - Names:
          {'container': <PloneSite at /yourinstance>,
           'context': <PloneSite at /yourinstance>,
           'default': <object object at 0x194520>,
           'here': <PloneSite at /yourinstance>,
           'loop': {},
           'nothing': None,
           'options': {'args': (<Products.Five.metaclass.SimpleViewClass from /Users/moo/yourinstance/eggs/plone.app.portlets-1.2-py2.4.egg/plone/app/portlets/browser/templates/manage-contextual.pt object at 0x67e43b0>,)},
           'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x73b59b8>,
           'request': <HTTPRequest, URL=http://localhost:8080/yourinstance/@@manage-portlets>,
           'root': <Application at >,
           'template': <ImplicitAcquirerWrapper object at 0x73b29f0>,
           'traverse_subpath': [],
           'user': <PropertiedUser 'admin'>,
           'view': <Products.Five.metaclass.SimpleViewClass from /Users/moo/yourinstance/eggs/plone.app.portlets-1.2-py2.4.egg/plone/app/portlets/browser/templates/manage-contextual.pt object at 0x67e43b0>,
           'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0x73b23d0>}
      Module Products.Five.browser.providerexpression, line 37, in __call__
      ...
      Module zope.tales.tales, line 696, in evaluate
       - URL: index
       - Line 18, Column 12
       - Expression: <PathExpr standard:'view/addable_portlets'>
       - Names:
          {'container': <PloneSite at /yourinstance>,
           'context': <PloneSite at /yourinstance>,
           'default': <object object at 0x194520>,
           'here': <PloneSite at /yourinstance>,
           'loop': {},
           'nothing': None,
           'options': {'args': ()},
           'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x7941be8>,
           'request': <HTTPRequest, URL=http://localhost:8080/yourinstance/@@manage-portlets>,
           'root': <Application at >,
           'template': <ImplicitAcquirerWrapper object at 0x78be050>,
           'traverse_subpath': [],
           'user': <PropertiedUser 'admin'>,
           'view': <plone.app.portlets.browser.editmanager.ContextualEditPortletManagerRenderer object at 0x789eb90>,
           'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0x790a870>}
      Module zope.tales.expressions, line 217, in __call__
      Module Products.PageTemplates.Expressions, line 163, in _eval
      Module Products.PageTemplates.Expressions, line 125, in render
      Module plone.app.portlets.browser.editmanager, line 154, in addable_portlets
      Module plone.app.portlets.browser.editmanager, line 149, in check_permission
      Module OFS.Traversable, line 301, in restrictedTraverse
      Module OFS.Traversable, line 284, in unrestrictedTraverse
       - __traceback_info__: ([], 'collective.easytemplate.TemplatedPortlet')
    NotFound: collective.easytemplate.TemplatedPortlet

This usually means that your site has an portlet assignment which code is not present anymore.

In this case you can see that portlet type "collective.easytemplate.TemplatedPortlet" is missing.

Ä Check that you include the corresponding product (collective.easytemplate) in eggs= section in buildout.cfg

* Reinstall removed egg which has the code for the portlet

* Check that you include the corresponding product (collective.easytemplate) in zcml= section in buildout.cfg

* Make sure that portlet name is the same in ZCML and GenericSetup XML

* Make sure you use <include package=".portlets" /> in your code

Manually removing the portlet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a traceback like this::

	URL: index
	Line 18, Column 12
	Expression: <PathExpr standard:'view/addable_portlets'>
	Names:
	{'container': <ATFolder at /webandmobile/support>,
	 'context': <ATFolder at /webandmobile/support>,
	 'default': <object object at 0x7f7e3af1a200>,
	 'here': <ATFolder at /webandmobile/support>,
	 'loop': {},
	 'nothing': None,
	 'options': {'args': ()},
	 'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x11dee1b8>,
	 'request': <HTTPRequest, URL=http://webandmobile.mfabrik.com/support/@@manage-portlets>,
	 'root': <Application at >,
	 'template': <ImplicitAcquirerWrapper object at 0x7f7e2a9199d0>,
	 'traverse_subpath': [],
	 'user': <PropertiedUser 'admin'>,
	 'view': <plone.app.portlets.browser.editmanager.ContextualEditPortletManagerRenderer object at 0xf0526d0>,
	 'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0x7f7e2a919810>}
	Module zope.tales.expressions, line 217, in __call__
	Module Products.PageTemplates.Expressions, line 163, in _eval
	Module Products.PageTemplates.Expressions, line 125, in render
	Module plone.app.portlets.browser.editmanager, line 154, in addable_portlets
	Module plone.app.portlets.browser.editmanager, line 149, in check_permission
	Module OFS.Traversable, line 301, in restrictedTraverse
	Module OFS.Traversable, line 284, in unrestrictedTraverse
	__traceback_info__: ([], 'gomobile.convergence.ContentMedia')
	NotFound: gomobile.convergence.ContentMedia

It usually means that there is a portlet in your content which product code has been removed.

Reinstall the add-on providing the portlet, remove the portlet and then uninstall the add-on again.

NotFound while accessing a BrowserView based view
-------------------------------------------------

**Traceback**::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 110, in publish
      Module ZPublisher.BaseRequest, line 506, in traverse
      Module ZPublisher.HTTPResponse, line 686, in debugError
    NotFound:   <h2>Site Error</h2>

**Condition**: You'll get a NotFound error when accessing view using view traverse notation,
event though the view exist.

Example URL::

        http://yoursite/@@myview

**Reason**: This is because there is an exception raised in your view's __init__()
method. Views are Zope multi-adapters. Exception in multi-adapter factory
method causes ComponentLookUpError. Zope 2 publisher translates
this to NotFound error.


**Solution**:
* Put :doc:`pdb break statement </develop/debugging/pdb>` to the beginning of the __init__() method of your view. Then step through view code to see where the exception is raised.
* If your view does not have __init__() method, then copy the source code __init__() method to your view class from the first parent class which has a view

POSKeyError
-----------

POSKeyError is when the database has been unable to convert a reference to an object into the object itself
It's a low level error usually caused by a corrupt or incomplete database.

* You did not copy blobs when you copied Data.fs

* Your data is corrupted

* Glitch in database (very unlikely)

.. seealso::
    http://rpatterson.net/blog/poskeyerror-during-commit

PicklingError: Can't pickle <class 'collective.singing.async.IQueue'>: import of module collective.singing.async
-----------------------------------------------------------------------------------------------------------------

Singing & Dancing add-on does not uninstall cleanly. Try this command-line script to get it fixed (not tested).
Some parts may work, some not, depending on how messed up your site is.

Note that you need to have S & D present in the buildout when running this and
then you can remove it afterwards::


        import transaction
        from collective.singing.interfaces import ISalt
        from collective.singing.async import IQueue

        # Your site here
        portal = app.mfabrik
        sm = portal.getSiteManager()

        util_obj = sm.getUtility(ISalt)
        sm.unregisterUtility(provided=ISalt)
        del util_obj

        sm.utilities.unsubscribe((), ISalt)
        del sm.utilities.__dict__['_provided'][ISalt]
        del sm.utilities._subscribers[0][ISalt]

        util = sm.queryUtility(IQueue, name='collective.dancing.jobs')
        sm.unregisterUtility(util, IQueue, name='collective.dancing.jobs')
        del util
        del sm.utilities._subscribers[0][IQueue]

        transaction.commit()

RuntimeError: maximum recursion depth exceeded (Archetypes field problem)
-------------------------------------------------------------------------

**Traceback**::

    - __traceback_info__: ('memberimage', <TTMemberImage at tt_member_image.2010-01-23.8138248069>, {'field': <Field memberimage(image:rw)>})
    Module Products.Archetypes.Storage, line 96, in get
    Module Products.Archetypes.utils, line 808, in shasattr
    Module Products.Archetypes.fieldproperty, line 101, in __get__
    Module Products.Archetypes.Field, line 997, in get
    Module Products.Archetypes.Field, line 709, in get
     - __traceback_info__: ('memberimage', <TTMemberImage at tt_member_image.2010-01-23.8138248069>, {'field': <Field memberimage(image:rw)>})
    RuntimeError: maximum recursion depth exceeded

**Condition**: The following code will generate this error when you try to access the object::

    atapi.ImageField(
         'memberimage',
         # storage=atapi.AnnotationStorage(), # paster version
         storage=atapi.AttributeStorage(), # results in "max recursion depth exceeded" error
         widget=atapi.ImageWidget(
             label=_(u"New Field"),
             description=_(u"Field description"),
         ),
         validators=('isNonEmptyFile'),
         original_size=(600,600),
         sizes={ 'mini' : (80,80),
                 'normal' : (200,200),
                 'big' : (300,300),
                 'maxi' : (500,500)},
     ),

**Reason**: Schema fields using AttributeStorage (usually images, files) **cannot** have ATFieldProperty in the class::

    class Sample(base.ATCTContent):

        # This does not work with AttributeStorage
        memberimage = atapi.ATFieldProperty('memberimage')

**Solution**: simply remove ATFieldProperty() declaration for the problematic field. You cannot
access the field value anymore by calling *object.memberimage* but you need to call *object.getMemberimage()* instead.

TraversalError with lots of tuples and lists (METAL problem)
------------------------------------------------------------

**Traceback**::

    File "/home/moo/yourinstance/parts/zope2/lib/python/zope/tales/expressions.py", line 217, in __call__
      return self._eval(econtext)
    File "/home/moo/yourinstance/parts/zope2/lib/python/Products/PageTemplates/Expressions.py", line 155, in _eval
      ob = self._subexprs[-1](econtext)
    File "/home/moo/yourinstance/parts/zope2/lib/python/zope/tales/expressions.py", line 124, in _eval
      ob = self._traverser(ob, element, econtext)
    File "/home/moo/yourinstance/parts/zope2/lib/python/Products/PageTemplates/Expressions.py", line 85, in boboAwareZopeTraverse
      request=request)
    File "/home/moo/yourinstance/parts/zope2/lib/python/zope/traversing/adapters.py", line 164, in traversePathElement
      return traversable.traverse(nm, further_path)
     - __traceback_info__: ({u'main': [('version', '1.6'), ('mode', 'html'), ('setPosition', (7, 0)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('beginScope', {u'define-macro': u'main'}), ('optTag', (u'metal:main-macro', None, 'metal', 0, [('startTag', (u'metal:main-macro', [(u'define-macro', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1)), ('setPosition', (8, 1)), ('defineSlot', (u'main', [('beginScope', {u'define-slot': u'main'}), ('optTag', (u'metal:main-slot', None, 'metal', 0, [('startTag', (u'metal:main-slot', [(u'define-slot', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1))])), ('endScope', ())])), ('setPosition', (9, 1)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('rawtextColumn', (u'\n', 0))])), ('endScope', ())]}, 'master')
    File "/home/moo/yourinstance/parts/zope2/lib/python/zope/traversing/adapters.py", line 52, in traverse
      raise TraversalError(subject, name)
     - __traceback_info__: ({u'main': [('version', '1.6'), ('mode', 'html'), ('setPosition', (7, 0)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('beginScope', {u'define-macro': u'main'}), ('optTag', (u'metal:main-macro', None, 'metal', 0, [('startTag', (u'metal:main-macro', [(u'define-macro', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1)), ('setPosition', (8, 1)), ('defineSlot', (u'main', [('beginScope', {u'define-slot': u'main'}), ('optTag', (u'metal:main-slot', None, 'metal', 0, [('startTag', (u'metal:main-slot', [(u'define-slot', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1))])), ('endScope', ())])), ('setPosition', (9, 1)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('rawtextColumn', (u'\n', 0))])), ('endScope', ())]}, 'master', [])
    TraversalError: ({u'main': [('version', '1.6'), ('mode', 'html'), ('setPosition', (7, 0)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('beginScope', {u'define-macro': u'main'}), ('optTag', (u'metal:main-macro', None, 'metal', 0, [('startTag', (u'metal:main-macro', [(u'define-macro', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1)), ('setPosition', (8, 1)), ('defineSlot', (u'main', [('beginScope', {u'define-slot': u'main'}), ('optTag', (u'metal:main-slot', None, 'metal', 0, [('startTag', (u'metal:main-slot', [(u'define-slot', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1))])), ('endScope', ())])), ('setPosition', (9, 1)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('rawtextColumn', (u'\n', 0))])), ('endScope', ())]}, 'master') (Also, the following error occurred while attempting to render the standard error message, please see the event log for full details: ({u'main': [('version', '1.6'), ('mode', 'html'), ('setPosition', (7, 0)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('beginScope', {u'define-macro': u'main'}), ('optTag', (u'metal:main-macro', None, 'metal', 0, [('startTag', (u'metal:main-macro', [(u'define-macro', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1)), ('setPosition', (8, 1)), ('defineSlot', (u'main', [('beginScope', {u'define-slot': u'main'}), ('optTag', (u'metal:main-slot', None, 'metal', 0, [('startTag', (u'metal:main-slot', [(u'define-slot', u'main', 'metal')]))], [('rawtextColumn', (u'\n\t', 1))])), ('endScope', ())])), ('setPosition', (9, 1)), ('setSourceFile', 'file:/home/moo/workspace2/collective.skinny/collective/skinny/skins/skinny_faux_layer/main_template.pt'), ('rawtextColumn', (u'\n', 0))])), ('endScope', ())]}, 'master'))

Some template tries to call macro inside another template and the macro is not defined in the target template.

TraversalError(subject, name) in expressions
--------------------------------------------

**Traceback**::

    File "/home/moo/sits/parts/zope2/lib/python/ZPublisher/Publish.py", line 119, in publish
      request, bind=1)
    File "/home/moo/sits/parts/zope2/lib/python/ZPublisher/mapply.py", line 88, in mapply
      if debug is not None: return debug(object,args,context)
    File "/home/moo/sits/parts/zope2/lib/python/ZPublisher/Publish.py", line 42, in call_object
      result=apply(object,args) # Type s<cr> to step into published object.
    File "/home/moo/sits/parts/zope2/lib/python/Products/Five/browser/metaconfigure.py", line 417, in __call__
      return self.index(self, *args, **kw)
    File "/home/moo/sits/parts/zope2/lib/python/Shared/DC/Scripts/Bindings.py", line 313, in __call__
      return self._bindAndExec(args, kw, None)
    File "/home/moo/sits/parts/zope2/lib/python/Shared/DC/Scripts/Bindings.py", line 350, in _bindAndExec
      return self._exec(bound_data, args, kw)
    File "/home/moo/sits/parts/zope2/lib/python/Products/PageTemplates/PageTemplateFile.py", line 129, in _exec
      return self.pt_render(extra_context=bound_names)
    File "/home/moo/sits/parts/zope2/lib/python/Products/PageTemplates/PageTemplate.py", line 98, in pt_render
      showtal=showtal)
    File "/home/moo/sits/parts/zope2/lib/python/zope/pagetemplate/pagetemplate.py", line 117, in pt_render
      strictinsert=0, sourceAnnotations=sourceAnnotations)()
    File "/home/moo/sits/parts/zope2/lib/python/zope/tal/talinterpreter.py", line 271, in __call__
      self.interpret(self.program)
    File "/home/moo/sits/parts/zope2/lib/python/zope/tal/talinterpreter.py", line 346, in interpret
      handlers[opcode](self, args)
    File "/home/moo/sits/parts/zope2/lib/python/zope/tal/talinterpreter.py", line 891, in do_useMacro
      self.interpret(macro)
      handlers[opcode](self, args)

    ...

    File "/home/moo/sits/parts/zope2/lib/python/zope/tal/talinterpreter.py", line 586, in do_setLocal_tal
      self.engine.setLocal(name, self.engine.evaluateValue(expr))
    File "/home/moo/sits/parts/zope2/lib/python/zope/tales/tales.py", line 696, in evaluate
      return expression(self)
    File "/home/moo/sits/parts/zope2/lib/python/zope/tales/expressions.py", line 218, in __call__
      return self._eval(econtext)
    File "/home/moo/sits/parts/zope2/lib/python/Products/PageTemplates/Expressions.py", line 153, in _eval
      ob = self._subexprs[-1](econtext)
    File "/home/moo/sits/parts/zope2/lib/python/zope/tales/expressions.py", line 124, in _eval
      ob = self._traverser(ob, element, econtext)
    File "/home/moo/sits/parts/zope2/lib/python/Products/PageTemplates/Expressions.py", line 103, in trustedBoboAwareZopeTraverse
      request=request)
    File "/home/moo/sits/parts/zope2/lib/python/zope/traversing/adapters.py", line 164, in traversePathElement
      return traversable.traverse(nm, further_path)
    File "/home/moo/sits/parts/zope2/lib/python/zope/traversing/adapters.py", line 52, in traverse
      raise TraversalError(subject, name)

**Reason**: From line ``Products/PageTemplates/Expressions.py`` you can see the error comes from TAL templates.
TAL templates are trying to execute path based expressions.

If you can view this error through error_log the error_log traceback will contain information
what expression causes the exception. However if this only happens with unit tests you can have something like::

    def __call__(self, econtext):
        if self._name == 'exists':
            return self._exists(econtext)
        print "Evaluating expression:" + self._s
        return self._eval(econtext)

manually injected to ``zope.tales.expression`` module.

TraversalError: @@standard_macros
---------------------------------

**Traceback**::

    - Warning: Macro expansion failed
    - Warning: zope.traversing.interfaces.TraversalError: (<plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>, '++view++standard_macros')
    Module zope.tal.talinterpreter, line 271, in __call__
    Module zope.tal.talinterpreter, line 346, in interpret
    Module zope.tal.talinterpreter, line 870, in do_useMacro
    Module zope.tales.tales, line 696, in evaluate
     - URL: form
     - Line 1, Column 0
     - Expression: <PathExpr standard:'context/@@standard_macros/page'>
     - Names:
        {'container': <plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>,
         'context': <plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>,
         'default': <object object at 0x100311200>,
         'here': <plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>,
         'loop': {},
         'nothing': None,
         'options': {'args': (<plone.app.headeranimation.browser.forms.AddHeaderAnimationForm object at 0x1102dc490>,)},
         'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0x110845758>,
         'request': None,
         'root': None,
         'template': <ImplicitAcquirerWrapper object at 0x11084ff10>,
         'traverse_subpath': [],
         'user': <PropertiedUser 'admin'>,
         'view': <UnauthorizedBinding: context>,
         'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0x110844310>}
    Module zope.tales.expressions, line 217, in __call__
    Module Products.PageTemplates.Expressions, line 155, in _eval
    Module zope.tales.expressions, line 124, in _eval
    Module Products.PageTemplates.Expressions, line 105, in trustedBoboAwareZopeTraverse
    Module zope.traversing.adapters, line 154, in traversePathElement
     - __traceback_info__: (<plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>, '@@standard_macros')
    Module zope.traversing.namespace, line 107, in namespaceLookup
    TraversalError: (<plone.app.headeranimation.browser.forms.HeaderCRUDForm object at 0x110289590>, '++view++standard_macros')

:doc:`Wrapping is missing from your form object </develop/plone/forms/z3c.form>`.

**Solution**:
::

    def update(self):
        super(HeaderCRUDForm, self).update()

        addform = self.addform_factory(self, self.request)
        editform = self.editform_factory(self, self.request)

        import zope.interface
        from plone.z3cform.interfaces import IWrappedForm

        zope.interface.alsoProvides(addform, IWrappedForm)
        addform.update()
        editform.update()
        self.subforms = [editform, addform]

TraversalError: No traversable adapter found
--------------------------------------------

**Traceback**::

    ...
    * Module ZPublisher.Publish, line 202, in publish_module_standard
    * Module ZPublisher.Publish, line 150, in publish
    * Module Zope2.App.startup, line 221, in zpublisher_exception_hook
    * Module ZPublisher.Publish, line 119, in publish
    * Module ZPublisher.mapply, line 88, in mapply
    * Module ZPublisher.Publish, line 42, in call_object
    * Module Shared.DC.Scripts.Bindings, line 313, in __call__
    * Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
    * Module Products.CMFCore.FSPageTemplate, line 216, in _exec
    * Module Products.CMFCore.FSPageTemplate, line 155, in pt_render
    * Module Products.PageTemplates.PageTemplate, line 98, in pt_render
    * Module zope.pagetemplate.pagetemplate, line 117, in pt_render
      Warning: Macro expansion failed
      Warning: zope.traversing.interfaces.TraversalError: ('No traversable adapter found',


This traceback is followed by long dump of template code internals.

Usual cause: Some add-on product fails to initialize.

**Solution**: Start Zope in foreground mode (bin/instance fg) to see which product fails.


TypeError: 'ExtensionClass.ExtensionClass' object is not iterable
-----------------------------------------------------------------

**Traceback**::

  Module ZPublisher.Publish, line 126, in publish
  Module ZPublisher.mapply, line 77, in mapply
  Module ZPublisher.Publish, line 46, in call_object
  Module Shared.DC.Scripts.Bindings, line 322, in __call__
  Module Products.PloneHotfix20110531, line 106, in _patched_bindAndExec
  Module Shared.DC.Scripts.Bindings, line 359, in _bindAndExec
  Module App.special_dtml, line 185, in _exec
  Module DocumentTemplate.DT_Let, line 77, in render
  Module DocumentTemplate.DT_In, line 647, in renderwob
  Module DocumentTemplate.DT_In, line 772, in sort_sequence
  Module ZODB.Connection, line 860, in setstate
  Module ZODB.Connection, line 914, in _setstate
  Module ZODB.serialize, line 612, in setGhostState
  Module ZODB.serialize, line 605, in getState
  Module zope.interface.declarations, line 756, in Provides
  Module zope.interface.declarations, line 659, in __init__
  Module zope.interface.declarations, line 45, in __init__
  Module zope.interface.declarations, line 1382, in _normalizeargs
  Module zope.interface.declarations, line 1381, in _normalizeargs
  TypeError: ("'ExtensionClass.ExtensionClass' object is not iterable", <function Provides at 0x9f04d84>, (<class 'Products.ATContentTypes.content.folder.ATFolder'>, <class 'Products.Carousel.interfaces.ICarouselFolder'>))

**Condition**: This error tends to happen after moving a Data.fs to a new instance that does not have the identical add-ons to the original instance.

In this example traceback the missing add-on is Products.Carousel which provides the marker interface Products.Carousel.interfaces.ICarousel

**Solution**: Install the missing add-on(s)

TypeError: 'NoneType' object is not callable during upgrade
-----------------------------------------------------------

**Traceback**::

    Traceback (innermost last):
      Module ZPublisherEventsBackport.patch, line 77, in publish
      Module ZPublisher.mapply, line 88, in mapply
      Module ZPublisher.Publish, line 42, in call_object
      Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 589, in installProducts
      Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 526, in installProduct
       - __traceback_info__: ('mfabrik.plonezohointegration',)
      Module Products.GenericSetup.tool, line 390, in runAllImportStepsFromProfile
       - __traceback_info__: profile-mfabrik.plonezohointegration:default
      Module Products.GenericSetup.tool, line 1179, in _runImportStepsFromContext
      Module Products.GenericSetup.tool, line 1090, in _doRunImportStep
       - __traceback_info__: toolset
      Module Products.GenericSetup.tool, line 128, in importToolset
    TypeError: 'NoneType' object is not callable

**Condition**: This error can happen during add-on install run / site upgrade

**Reason**: This means that your site database contains installed add-on utility objects
for which Python code is no longer present.

More pointers for resolving the tool can be found using pdb::

        (Pdb) tool_id
        'portal_newsletters'

This happens when you have used Singing and Dancing news letter product. This add-on
is problematic and does not uninstall cleanly.

* Reinstall Singing & Dancing

* Uninstall Singing & Dancing

* Hope your site works again

.. seealso::
    * :doc:`/manage/troubleshooting/manual-remove-utility`
    * http://opensourcehacker.com/2011/06/01/plone-4-upgrade-results-and-steps/
    * https://pypi.python.org/pypi/wildcard.fixpersistentutilities

TypeError: argument of type 'NoneType' is not iterable
------------------------------------------------------

**Traceback**::

	Module ZPublisher.Publish, line 115, in publish
	  Module ZPublisher.BaseRequest, line 437, in traverse
	  Module Products.CMFCore.DynamicType, line 147, in __before_publishing_traverse__
	  Module Products.CMFDynamicViewFTI.fti, line 215, in queryMethodID
	  Module Products.CMFDynamicViewFTI.fti, line 182, in defaultView
	  Module Products.CMFPlone.PloneTool, line 831, in browserDefault
	  Module plone.app.folder.base, line 65, in index_html
	  Module plone.folder.ordered, line 202, in __contains__
	TypeError: argument of type 'NoneType' is not iterable

**Reason** Plone 3 > Plone 4 migration has not been run. Run the migration
in *portal_migrations* under the Management Interface.

TypeError: len() of unsized object in smtplib
---------------------------------------------

**Traceback**::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 119, in publish
      Module ZPublisher.mapply, line 88, in mapply
      Module ZPublisher.Publish, line 42, in call_object
      Module Products.CMFFormController.FSControllerPageTemplate, line 90, in __call__
      Module Products.CMFFormController.BaseControllerPageTemplate, line 28, in _call
      Module Products.CMFFormController.ControllerBase, line 231, in getNext
      Module Products.CMFFormController.Actions.TraverseTo, line 38, in __call__
      Module ZPublisher.mapply, line 88, in mapply
      Module ZPublisher.Publish, line 42, in call_object
      Module Products.CMFFormController.FSControllerPythonScript, line 104, in __call__
      Module Products.CMFFormController.Script, line 145, in __call__
      Module Products.CMFCore.FSPythonScript, line 140, in __call__
      Module Shared.DC.Scripts.Bindings, line 313, in __call__
      Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
      Module Products.CMFCore.FSPythonScript, line 196, in _exec
      Module None, line 102, in order_email
       - <FSControllerPythonScript at /MySite/order_email>
       - Line 102
      Module Products.SecureMailHost.SecureMailHost, line 246, in secureSend
      Module Products.SecureMailHost.SecureMailHost, line 276, in _send
      Module Products.SecureMailHost.mail, line 126, in send
      Module smtplib, line 576, in login
      Module smtplib, line 536, in encode_cram_md5
      Module hmac, line 50, in __init__
    TypeError: len() of unsized object

**Reason**: Your SMTP password has been set empty. Please reset your SMTP password in *Mail* control panel.

.. seealso::
    http://plone.293351.n2.nabble.com/Plone-3-3-5-sending-emails-len-of-unsized-object-error-NO-ESMTP-PASSWORD-tp5415484p5415484.html

Unauthorized: The object is marked as private
---------------------------------------------

**Traceback**::

    File "/home/moo/twinapex/parts/zope2/lib/python/zope/tales/expressions.py", line 124, in _eval
      ob = self._traverser(ob, element, econtext)
    File "/home/moo/twinapex/parts/zope2/lib/python/Products/PageTemplates/Expressions.py", line 105, in trustedBoboAwareZopeTraverse
      request=request)
    File "/home/moo/twinapex/parts/zope2/lib/python/zope/traversing/adapters.py", line 164, in traversePathElement
      return traversable.traverse(nm, further_path)
    File "/home/moo/twinapex/parts/zope2/lib/python/zope/traversing/adapters.py", line 44, in traverse
      attr = getattr(subject, name, _marker)
    File "/home/moo/twinapex/parts/zope2/lib/python/Shared/DC/Scripts/Bindings.py", line 184, in __getattr__
      return guarded_getattr(self._wrapped, name, default)
    File "/home/moo/twinapex/parts/zope2/lib/python/AccessControl/ImplPython.py", line 563, in validate
      self._context)
    File "/home/moo/twinapex/parts/zope2/lib/python/AccessControl/ImplPython.py", line 443, in validate
      accessed, container, name, value, context)
    File "/home/moo/twinapex/parts/zope2/lib/python/AccessControl/ImplPython.py", line 808, in raiseVerbose
      raise Unauthorized(text)
    Unauthorized: The object is marked as private.  Access to 'showVideo' of (Products.Five.metaclass.SimpleViewClass from /home/moo/twinapex/src/mfabrik.app/mfabrik/app/browser/campaigntopview.pt object at 0x11003a0c) denied.

**Condition**:This error is raised when you try to access view functions or objects
for a view, which you call manually from the code.

**Reason**: View acquisition chain is not properly set up and the security manager cannot traverse acquisition
chain parents to properly determine permissions.

**Solution**: You need to use __of__() method to set-up the acquisition chain for the view::

    def getHeadingView(self):
        """
        Check if we have campaign view avaiable for this content and use it.
        """
        view = queryMultiAdapter((self.context, self.request), name="mfabrik_heading")
        view = view.__of__(self.context) # <---------- here
        return view


Unknown message (kss optimized for production mode) in JavaScript console
-------------------------------------------------------------------------

This is a KSS error message. KSS is an technology used in Plone 3
and started to be phased out in Plone 4.

**Possible causes**:

* Problems with KSS files (see portal_kss registry)

* Browser bugs (Google around for the fixes)

**Solution**:

* Go to portal_kss

* Remove are stale entries (missing files, marked on red)

Also:

* Put portal_kss for debug mode (in development environment)

ValueError: Non-zero version length. Versions aren't supported.
---------------------------------------------------------------

**Traceback**::

    File "/Users/moo/code/buildout-cache/eggs/zope.component-3.7.1-py2.6.egg/zope/component/registry.py", line 323, in subscribers
      return self.adapters.subscribers(objects, provided)
    File "/Users/moo/code/buildout-cache/eggs/ZODB3-3.9.5-py2.6-macosx-10.6-i386.egg/ZODB/Connection.py", line 838, in setstate
      self._setstate(obj)
    File "/Users/moo/code/buildout-cache/eggs/ZODB3-3.9.5-py2.6-macosx-10.6-i386.egg/ZODB/Connection.py", line 888, in _setstate
      p, serial = self._storage.load(obj._p_oid, '')
    File "/Users/moo/code/buildout-cache/eggs/ZODB3-3.9.5-py2.6-macosx-10.6-i386.egg/ZEO/ClientStorage.py", line 810, in load
      data, tid = self._server.loadEx(oid)
    File "/Users/moo/code/buildout-cache/eggs/ZODB3-3.9.5-py2.6-macosx-10.6-i386.egg/ZEO/ServerStub.py", line 176, in loadEx
      return self.rpc.call("loadEx", oid)
    File "/Users/moo/code/buildout-cache/eggs/ZODB3-3.9.5-py2.6-macosx-10.6-i386.egg/ZEO/zrpc/connection.py", line 703, in call
      raise inst # error raised by server
    ValueError: Non-zero version length. Versions aren't supported.

**Condition**: When trying to open any page

**Reason**: Most likely a corrupted Data.fs. Stop zeoserver. Recopy Data.fs. Recopy blobs.

.. seealso::
    * http://stackoverflow.com/questions/8387902/plone-upgrade-3-3-5-to-plone-4-1-2
    * https://mail.zope.org/pipermail/zodb-dev/2010-September/013620.html

Zope suddenly dies on OSX without a reason
-------------------------------------------

Symptoms: you do a HTTP request to a Plone site running OSX. Zope quits without a reason.

Reason: Infinite recursion is not properly handled by Python on OSX. This is because
OSX C stack size is smaller than Python default stack size. The underlying Python interpreter
dies before being able to raise stack size limit exception.

**Solution**

Edit ``python-2.4/lib/python2.4/site.py`` or corresponding Python interpreter ``site.py``
file (Python site installation customization file).

Put in to the first code line::

         sys.setrecursionlimit(800)

This will force smaller Python stack not exceeding native OSX C stack.
You might want to test other values and report back the findings.

.. seealso::
    http://blog.crowproductions.de/2008/12/14/a-buildout-to-tame-the-snake-pit/ (comments)

from zopeskel.basic_namespace import BasicNamespace
---------------------------------------------------------

When starting ZopeSkel::

  File "/home/moo/code/python2/parts/opt/lib/python2.6/pkgutil.py", line 238, in load_module
    mod = imp.load_module(fullname, self.file, self.filename, self.etc)
  File "/home/moo/code/plonecommunity/eggs/ZopeSkel-2.19-py2.6.egg/zopeskel/__init__.py", line 2, in <module>
    from zopeskel.basic_namespace import BasicNamespace

Or on paster with local commands::

  File "/fast/buildout-cache/eggs/templer.core-1.0b4-py2.6.egg/templer/core/basic_namespace.py", line 3, in <module>
    from templer.core.base import BaseTemplate
  File "/fast/buildout-cache/eggs/templer.core-1.0b4-py2.6.egg/templer/core/base.py", line 8, in <module>
    from paste.script import command
  ImportError: cannot import name command

System-wide templer / paster / zopeskel installation is affecting your buildout installation.

Remove system-wide installation::

    rm -rf /home/moo/code/python2/python-2.6/lib/python2.6/site-packages/ZopeSkel-2.19-py2.6.egg/

Re-run buildout.

Enjoy.

getUtility() fails: ComponentLookupError
----------------------------------------

**Traceback**::

    -> filter = getUtility(IConvergenceMediaFilter)
    (Pdb) n
    ComponentLookupError: <zope.component.interfaces.ComponentLookupError instance at 0x1038166c>

**Solution**: Make sure that your class object implements in the utility interface in the question::

    class ConvergedMediaFilter(object):
        zope.interface.implements(IConvergenceMediaFilter)


get_language: 'NoneType' object has no attribute 'getLocaleID'
---------------------------------------------------------------

**Traceback**::

    Module ZPublisher.Publish, line 202, in publish_module_standard
    Module ZPublisherEventsBackport.patch, line 115, in publish
    Module plone.app.linkintegrity.monkey, line 21, in zpublisher_exception_hook_wrapper
    Module Zope2.App.startup, line 221, in zpublisher_exception_hook
    Module ZPublisherEventsBackport.patch, line 77, in publish
    Module ZPublisher.mapply, line 88, in mapply
    Module ZPublisher.Publish, line 42, in call_object
    Module Products.Five.browser.metaconfigure, line 417, in __call__
    Module Shared.DC.Scripts.Bindings, line 313, in __call__
    Module Shared.DC.Scripts.Bindings, line 350, in _bindAndExec
    Module Products.PageTemplates.PageTemplateFile, line 129, in _exec
    Module Products.CacheSetup.patch_cmf, line 126, in PT_pt_render
    Warning: Macro expansion failed
    Warning: exceptions.TypeError: ('Could not adapt', <HTTPRequest, URL=http://mansikki.redinnovation.com:9666/isleofback/sisalto/etusivu/isleofbackfrontpage_view>, <InterfaceClass zope.i18n.interfaces.IUserPreferredLanguages>)
    Module zope.tal.talinterpreter, line 271, in __call__
    Module zope.tal.talinterpreter, line 346, in interpret
    Module zope.tal.talinterpreter, line 891, in do_useMacro
    Module zope.tal.talinterpreter, line 346, in interpret
    Module zope.tal.talinterpreter, line 536, in do_optTag_tal
    Module zope.tal.talinterpreter, line 521, in do_optTag
    Module zope.tal.talinterpreter, line 516, in no_tag
    Module zope.tal.talinterpreter, line 346, in interpret
    Module zope.tal.talinterpreter, line 534, in do_optTag_tal
    Module zope.tal.talinterpreter, line 516, in no_tag
    Module zope.tal.talinterpreter, line 346, in interpret
    Module zope.tal.talinterpreter, line 745, in do_insertStructure_tal
    Module Products.PageTemplates.Expressions, line 223, in evaluateStructure
    Module zope.tales.tales, line 696, in evaluate
    URL: file:/srv/plone/saariselka.fi/src/plonetheme.isleofback/plonetheme/isleofback/skins/plonetheme_isleofback_custom_templates/main_template.pt
    Line 58, Column 4
    Expression: <StringExpr u'plone.htmlhead.links'>
    Names:

    {'container': <IsleofbackFrontpage at /isleofback/sisalto/etusivu>,
     'context': <IsleofbackFrontpage at /isleofback/sisalto/etusivu>,
     'default': <object object at 0x7fd445785220>,
     'here': <IsleofbackFrontpage at /isleofback/sisalto/etusivu>,
     'loop': {},
     'nothing': None,
     'options': {'args': (<Products.Five.metaclass.SimpleViewClass from /srv/plone/saariselka.fi/src/isleofback.app/isleofback/app/browser/isleofbacknewfrontpageview.pt object at 0xbaa9910>,)},
     'repeat': <Products.PageTemplates.Expressions.SafeMapping object at 0xcd1b3f8>,
     'request': <HTTPRequest, URL=http://mansikki.redinnovation.com:9666/isleofback/sisalto/etusivu/isleofbackfrontpage_view>,
     'root': <Application at >,
     'template': <ImplicitAcquirerWrapper object at 0xcd208d0>,
     'traverse_subpath': [],
     'user': <SpecialUser 'Anonymous User'>,
     'view': <Products.Five.metaclass.SimpleViewClass from /srv/plone/saariselka.fi/src/isleofback.app/isleofback/app/browser/isleofbacknewfrontpageview.pt object at 0xbaa9910>,
     'views': <zope.app.pagetemplate.viewpagetemplatefile.ViewMapper object at 0xcd20d90>}

    Module Products.Five.browser.providerexpression, line 37, in __call__
    Module plone.app.viewletmanager.manager, line 83, in render
    Module plone.memoize.volatile, line 265, in replacement
    Module plone.app.layout.links.viewlets, line 28, in render_cachekey
    Module plone.app.layout.links.viewlets, line 19, in get_language

    AttributeError: <exceptions.AttributeError instance at 0xcd1bb48> (Also, the following error occurred while attempting to render the standard error message, please see the event log for full details: 'NoneType' object has no attribute 'getLocaleID')

Some sort of Products.CacheSetup related problem on Plone 3.3.x, hiding the real error.
Zope component architecture loading has failed (you are missing critical bits). This is
just the first entry where it tries to use an unloaded code.

Start your instance on the foreground and you should see the actual error.

importToolset: TypeError: 'NoneType' object is not callable
------------------------------------------------------------

**Traceback**::

    Module ZPublisher.Publish, line 47, in call_object
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 575, in installProducts
    Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 512, in installProduct
     - __traceback_info__: ('plone.app.registry',)
    Module Products.GenericSetup.tool, line 323, in runAllImportStepsFromProfile
     - __traceback_info__: profile-plone.app.registry:default
    Module Products.GenericSetup.tool, line 1080, in _runImportStepsFromContext
    Module Products.GenericSetup.tool, line 994, in _doRunImportStep
     - __traceback_info__: toolset
    Module Products.GenericSetup.tool, line 123, in importToolset

**Condition**: This happens when you try to install an add-on
product through Add-ons configuration panel.

**Reason**: You have leftovers from some old add-on installation (persistent tool)
and Python egg code is no longer present for this tool.

You should see a warning in logs giving you a hint when running add-on installer::

    2011-05-29 16:40:25 INFO GenericSetup.toolset Class Products.Notifica.NotificaTool.NotificaTool not found for tool notifica_tool

**Solution**: see information below (Removing portal tools part)

* :doc:`/manage/troubleshooting/manual-remove-utility`

Example: start site debug shell::

    bin/instance debug

Then run the script for your site id and problem tool id::

        bad_tool = 'notifica_tool'
        site = app.yoursiteid

        setup_tool = site.portal_setup
        toolset = setup_tool.getToolsetRegistry()
        if bad_tool in toolset._required.keys():
            del toolset._required[bad_tool]
            setup_tool._toolset_registry = toolset
        else:
            print "Tool not found:" + bad_tool

        import transaction ; transaction.commit()
        app._p_jar.sync()

In debug shell you can also check what all leftoverts toolset contains::

        >>> toolset._required.keys()
        ['portal_historyidhandler', 'portal_actions', 'portal_skins', 'portal_form_controller',
        'portal_workflow', 'portal_catalog', 'portal_languages', 'kupu_library_tool', 'portal_diff',
        'portal_repository', 'reference_catalog', 'portal_groupdata', 'portal_search_and_replace',
        'portal_atct', 'mimetypes_registry', 'portal_purgepolicy', 'formgen_tool', 'uid_catalog',
        'error_log', 'portal_modifier', 'portal_discussion', 'portal_actionicons', 'portal_calendar', 'portal_metadata', 'portal_url',
        'portal_archivist', 'portal_tinymce', 'portal_factory', 'content_type_registry', 'portal_groups', 'portal_controlpanel',
        'portal_uidannotation', 'portal_transforms', 'portal_memberdata', 'portal_javascripts', 'portal_registration', 'portal_css',
        'portal_facets_catalog', 'portal_password_reset', 'plone_utils', 'caching_policy_manager',
        'portal_historiesstorage', 'portal_undo', 'portal_placeful_workflow', 'translation_service',
        'archetype_tool', 'portal_view_customizations', 'portal_syndication', 'portal_quickinstaller', 'portal_uidhandler',
        'portal_referencefactories', 'portal_interface', 'portal_facetednavigation', 'portal_membership',
        'MailHost', 'portal_properties', 'portal_migration', 'portal_types', 'portal_uidgenerator']


.. seealso::
    http://plone.293351.n2.nabble.com/importToolset-NoneType-object-is-not-callable-upon-product-install-td5553065.html

z3c.form based form updateWidgets() raises ComponentLookupError
---------------------------------------------------------------

Case: missing plone.app.z3cform migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Traceback**::

    Traceback (innermost last):
      Module ZPublisher.Publish, line 126, in publish
      Module ZPublisher.mapply, line 77, in mapply
      Module ZPublisher.Publish, line 46, in call_object
      Module z3c.form.form, line 215, in __call__
      Module z3c.form.form, line 208, in update
      Module plone.z3cform.patch, line 21, in BaseForm_update
      Module z3c.form.form, line 149, in update
      Module z3c.form.form, line 129, in updateWidgets
      Module zope.component._api, line 109, in getMultiAdapter
    ComponentLookupError: ((<Products.Five.metaclass.EditForm object at 0x117a97dd0>, <HTTPRequest, URL=http://localhost:8080/folder_xxx/xxxngta/@@dgftreeselect-test>, <PloneSite at /folder_xxx/xxxngta>), <InterfaceClass z3c.form.interfaces.IWidgets>, u'')

**Reason**: You are running Plone 4 with ``plone.app.directives`` form which does not
open. The reason is that you most likely have old ``plone.app.z3cform``
installation which is not upgraded properly. In particular,
the following layer is missing

.. code-block:: xml

	<layer name="plone.app.z3cform" interface="plone.app.z3cform.interfaces.IPloneFormLayer" />

This enables ``z3c.form`` widgets on a Plone site.

**Solution**: *portal_setup* > *Import*. Choose profile *Plone z3cform support*.
and import. The layer gets properly inserted to your site database.


ImportError: cannot import name datetime
----------------------------------------

**Traceback**::

        (zinstance) [vagrant@dev Plone-5.0.7]$ ./zinstance/bin/plonectl start
    instance: Traceback (most recent call last):
      File "/home/vagrant/src/Plone-5.0.7/zinstance/bin/instance", line 259, in <module>
        import plone.recipe.zope2instance.ctl
      File "/home/vagrant/src/Plone-5.0.7/buildout-cache/eggs/plone.recipe.zope2instance-4.2.22-py2.7.egg/plone/__init__.py", line 2, in <module>
        __import__('pkg_resources').declare_namespace(__name__)
      File "/home/vagrant/src/Plone-5.0.7/zinstance/lib/python2.7/site-packages/pkg_resources/__init__.py", line 35, in <module>
        import plistlib
      File "/usr/lib64/python2.7/plistlib.py", line 62, in <module>
        import datetime
      File "/home/vagrant/src/Plone-5.0.7/buildout-cache/eggs/DateTime-4.0.1-py2.7.egg/datetime/__init__.py", line 14, in <module>
        from .DateTime import DateTime
      File "/home/vagrant/src/Plone-5.0.7/buildout-cache/eggs/DateTime-4.0.1-py2.7.egg/datetime/DateTime.py", line 24, in <module>
        from datetime import datetime
      File "/home/vagrant/src/Plone-5.0.7/buildout-cache/eggs/DateTime-4.0.1-py2.7.egg/datetime/datetime.py", line 24, in <module>
        from datetime import datetime
    ImportError: cannot import name datetime

**Reason**: You are running Plone in a virtual machine (docker, vagrant) on a case sensitive (or rather case unaware) file system (Mac OSX).
The system is getting confused between ``DateTime`` and ``datetime`` because it gets the wrong information from the host system.

**Solution**: Make sure you are not using shared folders that get written to by both systems.
Or at least do not put packages there.

.. seealso::
    https://community.plone.org/t/plone-5-0-7-unifiedinstaller-importerror-issue/3986
