Style Guide
===========

Python, like any programming language, can be written in a number of styles. We're the first to admit that Zope and Plone are not the finest examples of stylistic integrity, but that doesn't stop us from trying!

If you are not familiar with `PEP 8 <http://www.python.org/dev/peps/pep-0008>`_ - the python style guide, please take a moment to read and get up to date. We don't require it but we as a community really, really appreciate it. 

Naming Conventions
------------------
Above all else, be consistent with any code your are modifying! Historically the code is all camel case, but many new libraries are in the PEP8 convention. The mailing list is exploding with debate over what is better so we'll leave the excersize of deciding what to do with the user.

File Conventions
----------------
In Zope 2, file names used to be MixedCase. In Python, and thus in Plone going forward, we prefer all-lowercase filenames. This has the advantage that you can instantly see if you refer to a module / file or a class::

  from zope.pagetemplate.pagetemplate import PageTemplate

compare that to::

  from Products.PageTemplates.PageTemplate import PageTemplatePageTemplate

Filenames should be short and descriptive. Think about how an import would read::

  from Products.CMFPlone.utils import safe_hasattr

compare that to::

  from Products.CMFPlone.PloneUtilities import safe_hasattr

The former is obviously much easier to read, less redundant and generally more aesthetically pleasing.

**Note** This example is just about as terrible as they come. We need a better one.

Concrete Rules
--------------
 * Do not use tabs in Python code! Use spaces as indenting, 4 spaces for each level. We don't "require" `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_, but most people use it and it's good for you.
 * Indent properly, even in HTML. 
 * Never use a bare except. Anything like 'except: pass' will likely be reverted instantly
 * Avoid tal:on-error, since this swallows exceptions
 * Don't use hasattr() - this swallows exceptions, use getattr(foo, 'bar', None) instead. The problem with swallowed exceptions is not just poor error reporting. This can also mask ConflictErrors, which indicate that something has gone wrong at the ZODB level!
 * Never, ever put any HTML in Python code and return it as a string
 * Do not acquire anything unless absolutely necessary, especially tools. For example, instead of using 'context.plone_utils', use::
  
    from Products.CMFCore.utils import getToolByName
    plone_utils = getToolByName(context, 'plone_utils')

 * Do not put too much logic in ZPT (use Views instead!)
 * Remember to add i18n tags in ZPTs and Python code
