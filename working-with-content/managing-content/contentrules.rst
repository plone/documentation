===================
Using Content Rules
===================

This tutorial discusses what content rules are and how to configure and use them.

Overview
========

A general overview as to what makes up a content rule, some sample use cases, and who can set up and use content rules.

**What is a content rule?**

A content rule will automatically perform an action when certain events (known as "triggers") take place. For example, you can set up a content rule to send an email (the action) whenever certain (or any) content is added to a specific folder (the trigger).

**Other use cases for content rules**

- Move content from one folder to another when that content item is published
- Send email when a content item is deleted
- Delete content after a certain date

**Who can set up and use content rules?**

Site Manager permissions are required to in order to set up and apply content rules. In the ZMI "Content rules: Manage rules" is the permission related to being able to access the content rules configuration pages.

**What are the triggers and actions that come with Plone 3.0?**

The following general triggers are available by default:

- Object added to this container
- Object modified
- Object removed from this container
- Workflow state changed

The following actions are available by default:

- Make an entry in the event log
- Notify user with an information, warning, or error message
- Copy object to folder
- Move object to folder
- Delete object
- Transition workflow state of object
- Send email


Creating and Defining Content Rules
===================================

How to define content rules using the triggers and actions included in Plone

Creating a Rule
===============

Content rules are created globally through the Plone Control Pane ("site setup" link) and then selected from the Rules tab for the desired folder (or at the Plone site root if you want the rule applied site-wide).

In this example, you're going to create a content rule that will send an email any time a Page type is modified.

    - Click on "Content Rules" from the Site Setup page
    - The first option, "Enable Globally", allows you to enable and disable ALL content rules easily. Make sure this is enabled (which is the default) before continuing.
    - In the second section of the main page for Content Rules is where any existing content rules will be listed:

.. image:: /_static/example_rules_list.png
   :align: center
   :alt:


If there are a large number of content rules, it can be useful to filter them based on the triggers in the dropdown menu

- If no content rules exist, the only option is an "Add content rule" button. Click that.
- An "Add Rule" form comes up. Enter a descriptive title -- for this example, use: "Send Email when any Page is Modified". Enter a description if desired.
- For the "Triggering event" select "Object modified". Leave "Enabled" checked, and "Stop executing rules" unchecked.

.. image:: /_static/addingnewrule.png
   :align: center
   :alt:


- Click the "Save" button. At this point, you have essentially created a "container" for the content rule:

.. image:: /_static/rulejustadded.png
   :align: center



Next you'll further define the trigger and actions for this rule.


Defining a Content Rule
========================



- After creating a content rule, you need to actually define the specific conditions of the trigger and actions that will occur based on those conditions.
- Click on the title of your content rule, in this case "Send Email when any Page is Modified".
- Two new sections will show up for setting the conditions and actions:

.. image:: /_static/conditionlistempty.png
   :align: center


**For the condition:**

        - By default, "Content type" is selected and since you want a trigger only for Pages, just click on the "Add" button.
        - From the "Add Content Type Condition" page, select "Page" and click on "Save":

.. image:: /_static/addcontenttypecondition.png
   :align: center


**For the action:**

        - Select "Send email" from the drop down menu and click on the "Add" button.
        - From the "Add Mail Action" page, fill out the form:
        - For the "Subject" enter: "Automated Notification: Page Modified"
        - "Email source" is the From: address and is optional
        - "Email recipients" is the To: address; enter a valid email address
        - For the "Message" enter what you want for the body of the email:

.. image:: /_static/addmailaction.png
   :align: center


- Click the "Save" button



Congratulations, you have created a working content rule! Your content rule should look like:

.. image:: /_static/ruleslistcomplete.png
   :align: center


In the next section, you'll learn how easy it is to apply this content rule to any part (or all) of your Plone site.


Assigning a Content Rule
========================

Now that you've set up a content rule, how does it actually get used?

At this point, you have successfully created a content rule. However, this content rule isn't actually in use until it has been assigned and enabled on one or more folders.

- Navigate to the folder where you want the content rule to be in effect. This can be any folder on the Plone site or it can be for the entire Plone site ("Home").
- Click on the "Rules" tab. From there you will see a drop down menu of possible content rules:

.. image:: /_static/availablecontentrulesforcontext.png
   :align: center


- Select the desired content rule ("Send Email..." in this example) and click on the "Add" button. The "Rules" tab now shows that your rule has been assigned to the current folder:

.. image:: /_static/rulesforthiscontext.png
   :align: center


- By default, the rule has now been applied to the current folder only as indicated by the symbol in the "Enabled here" column indicates.


Notice there are several buttons near the bottom. Tick the check box for the rule you want ("Send Email...") and then click on either "Apply to subfolders"  button. Now this content rule will also apply to any subfolder that exist now or are created in the future.
If you wish to have this rule apply to all the subfolders but not to the current folder, then tick the check box next to the rule and click on the "Disable" button.

.. note ::

    Note: that the "Enabled here" column is empty for this rule now. You will need to explicitly use the "Enable" button to re-active this rule for the current folder; just using the "Apply to current folder only" button will NOT re-enable the content rule.

    Basically, the "Apply to subfolders" and "Apply to current folder only" can be thought of as toggles.
    You can test this rule now by creating a new Page or modifying an existing Page. Once you click on "Save" for that Page, an email will be sent.


Managing Multiple Rules
=======================

Now that you've created, defined, and assigned one content rule, it's time to explore how multiple rules work together.

In this section you'll need to create one or more additional rules before proceeding. Try one of these for size:

    Send an email when a News Item is deleted.
    Move News Items to a Folder when that News Item is published
    Send an email whenever a News Item is modified.




More on Triggers. Actions, and Assigning Rules
==============================================

In-depth information covering each of the triggers and actions available and notes on applying content rules.

Triggers
--------

    - Object added to container
    -    Object modified (note: this gets triggered on creation for a Page -- because it's renamed?)
    -    Object removed
    -    Workflow state changed


Conditions
----------

    -    Content type
    -    File extension
    -    Workflow state: restricts rules to objects in particular workflow states
    -    Workflow transition: restricst rules to execute only after a certain transition
    -   User's group
    -    User's role


Actions
-------

    -    Logger
    -    Notify user
    -    Copy to folder
    -    Move to folder
    -    Delete object
    -    Transition workflow state
    -    Mail action


Assigning rules
---------------

    -    Rules tab on the folder
    -        rule name is in the drop down
    -        select rule, click on add
    -    enable / disable
    -    apply to subfolders / apply to current folder only
    -    unassign


Things to note when "navigating" with assigned content rules
--------------------------------------------------------------

The "Edit Content Rule" page uses a 'related items' like display ("Assignments") for listing all the locations where the rule is assigned. From there, you can go directly to that folder's Rules tab by clicking on the Title of that folder. Note that there is no indication in the Assignments section if the Rule is applied to subfolders or not.

.. image:: /_static/rule_assignment_list.png
   :align: center


If you're on a folder that has the rule assigned to it directly (e.g. it's NOT a subfolder of a folder that has the rule assigned), you can get directly to the "Edit Content Rule" page from the Rules tab by clicking on the Title of that rule (which is always a link).

Alternately, if you're on a folder that has the rule assigned from a folder higher up in the hierarchy, clicking on the rule Title link will take you to the folder's Rules tab where the rule has been explicitly assigned.

If from the Rules tab, a rule is listed at active, then the assignment of that rule is being managed from a parent folder.
