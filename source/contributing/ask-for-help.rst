===============
Asking For Help
===============

.. admonition:: Abstract

   Best practices on how to ask for help.

.. contents::
   :local:
   :depth: 2
   :backlinks: none

Guidelines And Examples
=======================

If you need help with an error or problem: before asking the question, please take a few minutes to read the guidelines below.

It is important to know how to state questions, because once you learn it, you will get better answers back more quickly.


Support And Discussion Forums
-----------------------------

By stating a **well-phrased question** you increase the likelihood of fast and helpful responses to your question.

Here are some general key rules users need to follow in creating a new topic.

- Always start with searching before you ask a question.
  Most of your questions were probably already answered by someone else in the past.

- Save your and our time by searching the web first.

How to search:

- Pick meaningful keywords from the log entry.
- Sometimes searching for the entire error message works!

Where to search:

- Google - Before asking for help, make a Google search with related keywords.


- `Plone Community Forums <https://community.plone.org/>`_ - help and discussion forums

- `StackOverflow <https://stackoverflow.com/questions/tagged/plone?sort=faq>`_ - some FAQs are maintained here

- `Troubleshooting <https://docs.plone.org/manage/troubleshooting/index.html>`_ tips and common error messages - for enabling debug mode and common tracebacks

- `GitHub issue tracker <https://github.com/plone/Products.CMFPlone/issues>`_ - for known related issues

- `Documentation issue tracker <https://github.com/plone/documentation/issues>`_ - for documentation related issues

If at any point you see any kind of error message (including error codes) – put them in your question.

Please do not write anything like “I see some error message”.
Be specific.

See `Basic troubleshooting <https://docs.plone.org/manage/troubleshooting/basic.html>`_ in case of an error

Follow netiquette while visiting and writing on forum or mailing list (give respect = get respect). This includes:

- Be patient – sometimes the problem cannot be solved within minutes or hours.

- You might need to bump the topic few times until an experienced person comes to the site and sees it.

- If you do not see any response after a day or two it probably means we do not know the answer to your question,
  or perhaps your question needs to include more detail.

- Do not use bad words.
  Respect others and what they are doing.

- Do not completely edit/erase your posts after you posted them on the forum (except for small corrections - they are allowed).

  Remember that once you sent them, they belong to the community and shall be used by anyone who needs it.

How To Write A Good Topic
-------------------------

Keep in mind, that if you ask a question and all you hear is silence, it might be a good indicator that something is wrong with your topic.

Read the hints below and try to match your topic with specified pattern.

Subject Lines
`````````````

Most people will read a message only if it appears to be intelligent.

Your subject line is your sales pitch, you should make your subject line specific and clear to understand.

.. admonition:: Example

   **A poor subject line:**

   GET METHOD!! URGENT HELP!!!!

   **A better subject line:**

   FooError in Passing GET variables to FormController

The big picture - An opening sentence should state the general problem that you wish to solve.

A Snapshot Of Your Environment
``````````````````````````````

- For Plone and for other relevant products: provide version numbers. e.g.,
  "I'm running Plone 6.0 under Python 3.x"

Steps To Reproduce The Issue
````````````````````````````

Give information about your ideas of how this error appeared:

- What caused it or anything that could lead to reproducing the error on another computer
- Your buildout.cfg, versions.cfg, version numbers of installed add-ons, detailed command lines, the complete error message stack.
- Mention your expected result.

Online Chat
-----------

The Plone community uses `online chat <https://plone.org/support/chat>`_, specifically `Gitter <https://gitter.im/plone/public>`_.

Here are useful hints for using online chat:

- Remember that chat participants are volunteers; they are not paid to provide support.

- Do not ask permission to ask a question, but directly start the conversation having the all necessary input.

.. admonition:: Example

  Hi! I am trying to install PloneFormGen product, but it does not appear in the add on products list.

  When I start Zope in debug mode I get the following log entry.

  I pasted the log to `pastie.org <https://pastie.org/>`_ and here is the link for the log entry (post the link).

- Be specific - tell us why you are trying to accomplish something and then tell us what the problem is.
  Here are some guidelines how to form a good question for Internet discussion.

- Do not copy-paste text to chat.
  This disrupts other people chatting about other topics.

- Please paste the full traceback error log to `pastie.org <https://pastie.org/>`_ and then paste the link to your error log or code (from your browser's address bar) to the chat.

- Do not send direct messages to chat participants unless you have a clear reason to do so.

- Keep the chat window open at least 30 minutes so that someone has time to pick up your question. Be patient.

- Do not repeat yourself - people might be busy or not able to help with your problem.
  Silence does not mean we are ignoring you, it means that nobody is online right now who knows the answer to your question.

- Do not overuse CAPS-LOCK writing, since it is considered shouting and nobody likes when others shout at them.
  Do not use excessive exclamation marks (!!!) or question marks (???) as it makes you look unprofessional and discourages to help you.

- There are many people discussing simultaneously - if you address a message to a particular person, use his or her nick name.

- Chat is a real-time communication tool.
  Keep in mind, that since you write something, and send it, it cannot be taken back.

- Try to respond to all questions other users have.
  Chat is much more fluid and dynamic than the forum, do not worry if you forget about putting something in the first message – you can still keep up.

- Do not worry if you are not fluent in English - Plone is a global community.
  People will usually try to ask you more detailed questions in a way that the message gets through.


.. admonition:: Example

  **An ineffective chat question:**

  "Anyone here using product XYZ? Anyone here have problems installing XYZ?"

  **A question that is more likely to gain attention and a positive response:**

  "Hi, I'm using product XYZ on Plone 5.x.x,
  I have a problem with the feature that is supposed to do ABC

  I get error BlahBlahError — what might be wrong?

  Here is a link to the error log on pastie.org: (post the link)"

Tracebacks
----------

When there is an error, a Python program always products a traceback, a complete information where the application was when the error happened.

To help you with an error, a complete traceback log is needed, not just the last line which says something like "AttributeError".

Copy full tracebacks to your message (discussion forums) or pastie.org link (chat). The most reliable way to get the traceback output is to start Plone (Zope application server)
in foreground mode in your terminal / command line (see these `debugging tips <https://docs.plone.org/manage/troubleshooting/basic.html>`_)

First, shut down Plone if it's running as a service / background process. Then start Plone in foreground mode.

On Linux, OSX or similar systems this is (navigate to Plone folder first):

.. code-block:: shell

   bin/instance fg

On Windows command prompt this is

.. code-block:: bash

   cd "C:\Program Files\Plone"
   bin\buildout.exe fg

Zope outputs all debug information to the console where it was started in foreground mode.
When the error happens, the full traceback is printed to the console as well.

If Zope does not start in foreground mode it means that your add-on configuration is bad.
You need to fix it and the related traceback is printed as well.

In production mode, Zope ignores all add-ons which fail to load.

Credits
-------

This how-to originated as an informal, user-friendly alternative to Eric Raymond's `How to Ask Questions the Smart Way <http://www.catb.org/~esr/faqs/smart-questions.html>`_. ESR's doc is long and offensive, though once you realize that ESR is your crusty old merchant-marine uncle it can be fun and helpful.

The error report format is adapted from Joel Spolsky's comments on bug tracking, e.g., in `Joel on Software <https://www.joelonsoftware.com/articles/fog0000000029.html>`_.
