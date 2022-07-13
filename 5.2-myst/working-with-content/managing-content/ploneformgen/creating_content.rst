=========================
Creating Content From PFG
=========================

.. topic :: Description

    This how-to covers simple creation of portal content from PloneFormGen. We'll create web pages from sample form submissions.

 A question that's come up frequently on Gitter and the Plone forum is "How do I create an event, news item, page, or some other content item from PloneFormGen? It's common that there's some security need or extra content needed that prevents just using Plone's "add item."

This is actually very easy if you know a little Python and are willing to learn something about the content items you want to create.

Please note that I'm not going to show you how to create new content types here. Just how to use PFG to create content objects from existing types. If you want to create new content types, learn to use Dexterity.

Your first step should be to determine the attributes you want to set in the new content item and how they'll map from your form fields.

In this case, we're going to use the sample contact form created when you first create a form folder to create a page (Document).

Our mapping of form fields to content attributes will look like this:

============================= ==========================
Form Field                    Document Attribute
============================= ==========================
Your E-Mail Address (replyto) Description
Subject (topic)               Title
Comments (comments)           Body text
============================= ==========================

Note that for each form field, we've determined its ID in the form. We'll use those to look up the field in the form submission.

Next, we need to learn the methods that are used to set our attributes on a Document object. How do you learn these? It's always nice to read the source, but when I'm working fast, I usually just use DocFinderTab and look for "set*" methods matching the attributes.

Now, determine where you want to put the new content. That's your target folder. It's convenient to locate that folder in a parent folder of the form object, as you may then use the magic of acquisition to find it without learning how to traverse the object database.

Now, in the form folder, we add a "Custom Script Adapter" - which is just a very convenient form of Python script. Then, just customize the script to look something like the following:

.. code-block:: python

    # Find our target folder from the context. The ID of
    # our target folder is "submissions"
    target = context.submissions

    # The request object has a dictionary attribute named
    # form that contains the submitted form content, keyed
    # by field name
    form = request.form

    # We need to engineer a unique ID for the object we're
    # going to create. If your form submit contained a field
    # that was guaranteed unique, you could use that instead.
    from DateTime import DateTime
    uid = str(DateTime().millis())

    # We use the "invokeFactory" method of the target folder
    # to create a content object of type "Document" with our
    # unique ID for an id and the form submission's topic
    # field for a title.
    target.invokeFactory("Document", id=uid, title=form['topic'])

    # Find our new object in the target folder
    obj = target[uid]

    # Set its format, content and description
    obj.setFormat('text/plain')
    obj.setText(form['comments'])
    obj.setDescription(form['replyto'])

    # Force it to be reindexed with the new content
    obj.reindexObject()

That's it. This will really work.

Security
========

At the moment, the person that submits your form will need to be logged in as a user that has the right to add pages to the target folder, then change their attributes. You may need to allow other users (even anonymous ones) to submit the form. That's where the Proxy role setting of the custom script adapter comes in. You may change this setting to Manager, and the script will run as if the user has the manager role - even if they're anonymous.

I hope it's obvious that you want to be very, very careful writing a script that will run with the Manager role. Review it, and review it again to make sure it will do only what you want. Never trust unchecked form input to determine target or content ids.

If I'm doing this trick with a form that will be exposed to the public, I often will use a Python script rather than the custom script adapter, as it allows me to determine the proxy role for the script more precisely than choosing between None and Manager. I may even create a new role with minimal privileges, and those only in the target folder.
Credit!


.. note::

    A big thank's to Mikko Ohtamaa for contributing the Custom Script Adapter to PloneFormGen.
