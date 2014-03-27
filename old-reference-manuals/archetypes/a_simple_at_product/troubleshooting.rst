===================
Troubleshooting 
===================

.. admonition:: Description

		When creating new content types, many factors can silently fail due
		to human errors in the complex content type setup chain and security
		limitations. The effect is that you don't see your content type in
		Add drop down menu. Here are some tips for debugging. 

1. Is your product broken due to Python import time errors? Check the
\*Zope Management Interface (ZMI from now on) → Control Panel →
Products\*. Turn on Zope debugging mode to trace import errors. To see
error messages directly in the console with buildout, use \*bin/instance
fg\*.

2. Have you rerun the quick installer (GenericSetup) after
creating/modifying the content type? If not, (re)install the product
from the \*Plone Control Panel → Add-on Products\* or from the \*ZMI →
portal\_quickinstaller\*.

3. Do you have a correct Add permission for the product? Check the call
of the \`\`ContentInit()\`\` method inside the \*\_\_init\_\_.py\* file.
See `The startup module
<http://plone.org/documentation/manual/archetypes-developer-manual/a-semi-realistic-example/the-startup-module>`_.

4. Does it show up in the portal factory? Check \*ZMI →
portal\_factory\* and \*factorytool.xml\*.

5. Is it correctly registered as a portal type and implictly addable?
Check \*ZMI → portal\_types\*. Check
\*default/profiles/type/yourtype.xml\*.

6. Does it have a correct product name defined? Check \*ZMI →
portal\_types\*.

7. Does it have a proper factory method? Check \*ZMI → types\_tool\*.
Check Zope logs for \`\`\_queryFactory\`\` and import errors.

8. Does it register itself with Archetypes? Check \*ZMI →
archetypes\_tool\*. Make sure that you have \`\`ContentInit\`\` properly
run in your \*\_\_init\_\_.py\*. Make sure that all modules having
Archetypes content types defined and \`\`registerType()\`\` calls are
imported in \*\_\_init\_\_py\*.