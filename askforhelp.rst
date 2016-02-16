===============
Asking for help
===============


Guidelines and Examples
=======================

If you need help with an error or problem: before asking the question, please take a few minutes to read the guidelines below. It is important to know how to state questions, because once you learn it, answers will come much faster.


Asking help on discussion forums and mailing lists
--------------------------------------------------

By stating a **well-phrased question** you increase the likelihood of fast and helpful response to your question.

Here are some general key rules users need to follow in creating a new topic.

- ALWAYS start with searching, that means, before you create a topic. Most of your questions were probably already answered by someone else in the past. Save your and our time by searching the web first.

Where to search:

- Google - Before asking for help, make a Google search with related keywords. Pick meaningful keywords from the log entry.

- `StackOverflow <http://stackoverflow.com/questions/tagged/plone?sort=faq>`_ - some FAQs are maintained here.

- :doc:`Troubleshooting </manage/troubleshooting/index>` tips and common error messages - for enabling debug mode and common tracebacks.

- `GitHub issue tracker <https://github.com/plone/Products.CMFPlone/issues>`_ - for known related issues

- `Documentation issue tracker <https://github.com/plone/documentation/issues>`_ - for documentation related issues

If at any point you see any kind of error message (including error codes) – put them in the topic. Never write anything like “I see some error message”. Be specific.

See  :doc:`Basic troubleshooting </manage/troubleshooting/basic>` in case of an error

Follow the structure of the forum by creating your topic in a proper location (subforum). If you are in doubt where to create your topic, post to the `general questions <https://plone.org/support/forums/general>`_ forum.

Follow the netiquette while visiting and writing on forum or mailing list (give respect = get respect). This includes:

- Be patient – Sometimes the problem cannot be solved within minutes or hours. You might need to bump the topic few times till an experienced person comes to the site and sees it but usually if you do not see any response after 24h it probably means we cannot answer your question.
- Do not use bad words. Respect others and what they are doing.
- Do not completely edit/erase your posts after you posted them on the forum (except for small corrections - they are allowed) Remember that once you sent them, they belong to the community and shall be used by anyone who needs it.

How to write a good topic
^^^^^^^^^^^^^^^^^^^^^^^^^

Keep in mind, that if you ask a question and all you hear is silence, it might be a good indicator that something is wrong with your topic. Read the hints below and try to match your topic with specified pattern.

**Subject lines:** most people will read a message only if it appears to be intelligent. Your subject line is your sales pitch, so you should make your subject line specific and easy to understand.

.. note::

  **A poor subject line:**

  GET METHOD!! URGENT HELP!!!!

  **A better subject line:**

  FooError in Passing GET variables to FormController

The big picture - An opening sentence should state the general problem that you wish to solve.

**A snapshot of your environment** - For Plone and for other relevant products: provide version numbers. e.g., "I'm running Plone 5.0.2 under Python 2.7.10."

**Steps to reproduce the issue** - Give information about your ideas of how this error appeared, what caused it or anything that could lead to reproducing the error on another computer. The expected result .

Asking help in real time chat (IRC)
-----------------------------------

Plone community real time chat is at the  `#plone <irc://irc.freenode.net/#plone>`_ IRC channel on the freenode IRC network.

If you're not already familiar with IRC, you can visit the `support area <https://plone.org/support>`_, which offers a web page that connects you to our chat room right in your web browser.


Here are couple of useful hints while connecting to IRC network:

- Do not ask permission to ask a question, but directly start the conversation having the all necessary input. Follow the example below:

    Hi! I am trying to install PloneFormGen product, but it does not appear in the add on products list.

    When I start Zope in debug mode I get the following log entry.

    I pasted the log to `pastie.org <http://pastie.org/>`_ and here is the link for the log entry http://pastie.org/123123

- Be specific - tell us why you are trying to accomplish something and then tell us what the problem is. Here are some guidelines how to form a good question for Internet discussion.

- Do not copy-paste text to chat. This disrupts other people chatting about other topics. Instead please paste the full traceback error log to `pastie.org <http://pastie.org/>`_ and then paste the link to your error log or code (from your browser's address bar) to the chat.

- Do not send direct messages to chat participants unless you have a clear reason to do so
- Keep the chat window open at least 30 minutes so that someone has time to pick up your question. Be patient.

- Do not repeat yourself - people might be busy or not able to help with your problem.  Silence doesn't mean we're ignoring you, it means that nobody is online right now who knows the answer to your question.

- Do not overuse CAPS-LOCK writing, since it is considered shouting and nobody likes when others shout at them. Do not use excessive exclamation marks (!!!) or question marks (???) as it makes you look unprofessional and discourages to help you.

- There are many people discussing simultaneously - if you address a message to a particular person, use his or her nick name. Hint: you can use Tab key to autocomplete nick name after typing few letters.

- IRC is a real-time communication tool. Keep in mind, that since you write something, and send it, it cannot be taken back.

- Try to respond to all questions other users have. IRC is much more fluent and faster than forum, so don’t worry if you forget about putting something in the first message – you can still keep up.

- Do not worry if you are not fluent in English - Plone is a global community, and people will usually try to ask you more detailed questions in a way that the message gets through.


.. note::

  **Examples**

  An ineffective IRC question:

  "Anyone here using product XYZ? Anyone here have problems installing XYZ?"

  A question that is more likely to gain attention and a positive response:

  "Hi, I'm using product XYZ on Plone 5.x.x, I have a problem with the feature that is supposed to doABC— I get error BlahBlahError — what might be wrong? Here is a link to the error log on pastie.org:http://pastie.org/123123"

Tracebacks
----------

When there is an error, a Python program always products a traceback, a complete information where the application was when the error happened. To help you with an error, a complete traceback log is needed, not just the last line which says something like "AttributeError".

Copy full tracebacks to your message (discussion forums) or pastie.org link (IRC). The most reliable way to get the traceback output is to start Plone (Zope application server) on foreground mode in your terminal / command line.

First, shutdown Plone if it's running as service / background process. Then start Plone on foreground mode.

On Linux, OSX or similar systems this is (navigate to Plone folder first):

.. code-block:: console

  bin/instance fg

On Windows command prompt this is

.. code-block:: console

  cd "C:\Program Files\Plone"
  bin\buildout.exe fg

Zope outputs all debug information to the console where it was started in foreground mode. When the error happens, the full traceback is printed to the console as well.

If Zope does not start in foreground mode it means that your add-on configuration is bad and you need to fix it and the related traceback is printed as well. In production mode, Zope ignores all add-ons which fail to load.




Credits
^^^^^^^

This how-to originated as an informal, user-friendly alternative to Eric Raymond's `How to Ask Questions the Smart Way <http://www.catb.org/~esr/faqs/smart-questions.html>`_. ESR's doc is long and offensive, though once you realize that ESR is your crusty old merchant-marine uncle it can be fun and helpful.

The error report format is adapted from Joel Spolsky's comments on bug tracking, e.g., in `Joel on Software <http://www.joelonsoftware.com/articles/fog0000000029.html>`_.
