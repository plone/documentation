===================
ATVocabularyManager
===================

.. contents :: :local:

.. admonition:: Description

        ATVocabularyManager is a product for letting site managers define
        vocabularies for fields through-the-web or by import from XML files.
        ArchGenXML can generate the necessary code to use this product.

ATVM manages dynamic vocabularies. It installs a tool, where a site Manager can add, change and delete vocabularies. These vocabularies can then be used anywhere on the site.

You can download ATVocabularyManager from the Plone.org products area: `/products/atvocabularymanager <http://plone.org/products/atvocabularymanager>`_

Using simple flat vocabularies
------------------------------
Adding ATVM-vocabs to your UML model is quite easy.

1. Add a selection or multiselection field to your type.

2. Add a tag ``vocabulary:name`` and give it a name, let's say ``countries``

3. Add a tag ``vocabulary:type`` with the value ``ATVocabularyManager``

We are now finished with the UML. Save it and let AGX do the work. What still is missing, is to install the countries vocabulary. Therefore:

* Add a function called ``setupVocabularies`` to the protected code section in ``setuphandlers.py`` in your product and register it as an import step in ``/profiles/default/import_steps.xml`` in a code section (make it dependent from you ``*QI-Dependencies`` step.

* Add the following code to your setuphandler.py (this sets up a vocabulary ``countries`` with the given values, and registers it with ATVocabularyManager)::

    from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
    from Products.CMFCore.utils import getToolByName
    from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
    
    def setupVocabularies(context):
        """let's install the countries vocab"""
    
        vocabs = {}
        vocabs['countries'] = (
            ('ice', u'Iceland'),
            ('nor', u'Norway'),
            ('fin', u'Finland'),
            ('tyr', u'Tyrol'),
            ('auf', u'Ausserfern'),
        )
        site = context.getSite()
        atvm = getToolByName(site, ATVOCABULARYTOOL)
        createSimpleVocabs(atvm, vocabs)

Using simple tree vocabularies
------------------------------
If you are interested in using and creating hierachical vocab:

* use additional tag ``vocabulary:vocabulary_type`` with value ``TreeVocabulary``,

* have a look at the doc-string of ``Products.ATVocabularyManager.utils.createHierarchicalVocabs``.

Using vocabularies based on the **IMS Vocabulary Definition Exchange** (VDEX) format.

`VDEX <http://www.imsglobal.org/vdex/index.html>`_ is a simple XML based format to define flat or hierachical multilingual vocabularies. ATVocabularyManager supports VDEX in most of its dialects.

To tell Archetypes to use them in your UML first take Steps 1 to 3 of the first section and skip the import part. Then add a tag ``vocabulary:vocabulary_type`` and give it the value ``VdexVocabulary``.

Now add a folder called ``data`` in your products folder. Inside the ``/data`` folder create a new file called ``countries.vdex`` ("example":countries.vdex). It will be imported automatically on install or reinstall, but only if a vocabulary named countries does not exist.
