==============================================
Changing Portal Transforms Settings via Python
==============================================

Introduction
------------

If you have to change some portal_transforms settings you can't use a Generic
Setup config file for this.
But you can change it with python and a Generic Setup import step.

.. warning::

   Security: The configuration shown below allows users to use nasty HTML tags which can be a security issue if not used carefully.

Let's say we have a Plone package called MY.PACKAGE.

Writing an Generic Setup Import Step Method
-------------------------------------------

This setup method is defined in MY.PACKAGE/setuphandlers.py.
It configures the safe_html portal_transform a bit less paranoid about nasty tags and valid_tags,
so that content managers are allowed to insert iframe, object, embed, param,
script, style, tags and more into the TinyMCE editor::

    import logging
    from plone import api
    from Products.PortalTransforms.Transform import make_config_persistent

    logger = logging.getLogger('MY.PACKAGE.setuphandlers')

    def isNotThisProfile(context, marker_file):
        return context.readDataFile(marker_file) is None

    def setup_portal_transforms(context):
        if isNotThisProfile(context, 'MY.PACKAGE-PROFILENAME.txt'): return

        logger.info('Updating portal_transform safe_html settings')

        tid = 'safe_html'

        pt = api.portal.get_tool(name='portal_transforms')
        if not tid in pt.objectIds(): return

        trans = pt[tid]

        tconfig = trans._config
        tconfig['class_blacklist'] = []
        tconfig['nasty_tags'] = {'meta': '1'}
        tconfig['remove_javascript'] = 0
        tconfig['stripped_attributes'] = ['lang', 'valign', 'halign', 'border',
                                         'frame', 'rules', 'cellspacing',
                                         'cellpadding', 'bgcolor']
        tconfig['stripped_combinations'] = {}
        tconfig['style_whitelist'] = ['text-align', 'list-style-type', 'float',
                                      'width', 'height', 'padding-left',
                                      'padding-right'] # allow specific styles for
                                                       # TinyMCE editing
        tconfig['valid_tags'] = {
            'code': '1', 'meter': '1', 'tbody': '1', 'style': '1', 'img': '0',
            'title': '1', 'tt': '1', 'tr': '1', 'param': '1', 'li': '1',
            'source': '1', 'tfoot': '1', 'th': '1', 'td': '1', 'dl': '1',
            'blockquote': '1', 'big': '1', 'dd': '1', 'kbd': '1', 'dt': '1',
            'p': '1', 'small': '1', 'output': '1', 'div': '1', 'em': '1',
            'datalist': '1', 'hgroup': '1', 'video': '1', 'rt': '1', 'canvas': '1',
            'rp': '1', 'sub': '1', 'bdo': '1', 'sup': '1', 'progress': '1',
            'body': '1', 'acronym': '1', 'base': '0', 'br': '0', 'address': '1',
            'article': '1', 'strong': '1', 'ol': '1', 'script': '1', 'caption': '1',
            'dialog': '1', 'col': '1', 'h2': '1', 'h3': '1', 'h1': '1', 'h6': '1',
            'h4': '1', 'h5': '1', 'header': '1', 'table': '1', 'span': '1',
            'area': '0', 'mark': '1', 'dfn': '1', 'var': '1', 'cite': '1',
            'thead': '1', 'head': '1', 'hr': '0', 'link': '1', 'ruby': '1',
            'b': '1', 'colgroup': '1', 'keygen': '1', 'ul': '1', 'del': '1',
            'iframe': '1', 'embed': '1', 'pre': '1', 'figure': '1', 'ins': '1',
            'aside': '1', 'html': '1', 'nav': '1', 'details': '1', 'u': '1',
            'samp': '1', 'map': '1', 'object': '1', 'a': '1', 'footer': '1',
            'i': '1', 'q': '1', 'command': '1', 'time': '1', 'audio': '1',
            'section': '1', 'abbr': '1'}
        make_config_persistent(tconfig)
        trans._p_changed = True
        trans.reload()


Registering the Import Step Method with Generic Setup
-----------------------------------------------------

Add an import step in MY.PACKAGE/MYPROFILESDIR/PROFILENAME/import_steps.xml like
so:::

    <?xml version="1.0"?>
    <import-steps>
      <import-step
        id="MY.PACKAGE-portal_transforms"
        handler="MY.PACKAGE.setuphandlers.setup_portal_transforms"
        title="MY.PACKAGE portal_transforms setup"
        version="1.0">
        <dependency step="plone-final"/>
      </import-step>
    </import-steps>

Create the File ``MY.PACKAGE/MYPROFILESDIR/PROFILENAME/MY.PACKAGE-PROFILENAME.txt``, so that this
import step is not run for any profile but just for this one.


Calling the Import Step Method in Management Interface, portal_setup
--------------------------------------------------------------------

Go to your site's portal_setup in Management Interface, select your registered profile and import
the import step "MY.PACKAGE portal_transforms setup".
