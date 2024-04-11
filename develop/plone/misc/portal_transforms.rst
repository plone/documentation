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

    logger = logging.getLogger("MY.PACKAGE.setuphandlers")

    def isNotThisProfile(context, marker_file):
        return context.readDataFile(marker_file) is None

    def setup_portal_transforms(context):
        if isNotThisProfile(context, "MY.PACKAGE-PROFILENAME.txt"): return

        logger.info("Updating portal_transform safe_html settings")

        registry = getUtility(IRegistry, context=portal)
        settings = registry.forInterface(IFilterSchema, prefix="plone")

        settings.nasty_tags = ["meta"]
        settings.valid_tags = [
            "code", "meter", "tbody", "style", "img", "title", "tt", "tr",
            "param", "li", "source", "tfoot", "th", "td", "dl", "blockquote",
            "big", "dd", "kbd", "dt", "p", "small", "output", "div", "em",
            "datalist", "hgroup", "video", "rt", "canvas", "rp", "sub", "bdo",
            "sup", "progress", "body", "acronym", "base", "br", "address",
            "article", "strong", "ol", "script", "caption", "dialog", "col",
            "h1", "h2, "h3", "h4", "h5", "h6", "header", "table", "span",
            "area", "mark", "dfn", "var", "cite", "thead", "head", "hr",
            "link", "ruby", "b", "colgroup", "keygen", "ul", "del", "iframe",
            "embed", "pre", "figure", "ins", "aside", "html", "nav", "details",
            "samp", "map", "object", "a", "footer", "i", "q", "command",
            "time", "audio", "section", "abbr"]

Alternatively, you could use the plone.api to achieve the same result:::

    from plone import api

    custom_nasty_tags = [u"meta]
    custom_valid_tags = [u"code", u"meter", u"tbody", ...]
    api.portal.set_registry_record("plone.nasty_tags", custom_nasty_tags)
    api.portal.set_registry_record("plone.valid_tags", custom_valid_tags)


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
