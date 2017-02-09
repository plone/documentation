=======================
Discussion and comments
=======================

.. admonition:: Description

        How to control commenting and discussion in Plone programmatically



Introduction
--------------

``plone.app.discussion`` provides basic in-site discussion support.

Disqus is a popular external <iframe> embed service used for commenting.

More info

* http://packages.python.org/plone.app.discussion/

* https://pypi.python.org/pypi/plone.app.discussion

Content type support
-------------------------

Enable discussion in :doc:`portal_types </develop/plone/content/types>` for each content typ
It's the *Allow Discussion* checkbox.

Discussion shows up as ``plone.comments`` viewlet in ``plone.app.layout.viewlets.interfaces.IBelowContent``
viewlet manager.

Getting total comment count
------------------------------------

Example::

    def getDiscussionCount(self):
        try:
            # plone.app.discussion.conversation object
            # fetched via IConversation adapter
            conversation = IConversation(self.targetContent)
        except:
            return 0

        return conversation.total_comments
