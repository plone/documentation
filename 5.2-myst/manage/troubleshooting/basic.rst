=======================
 Basic troubleshooting
=======================

.. admonition:: Description

        Here is some info for basic Plone troubleshooting, especially with add-on modules


Start Plone as foreground / debug mode
----------------------------------------

Plone runs on the top of Zope application service.
Zope is a Python process and will appear as "python ....." in your task manager process list.

Zope will report any problems with code when it is launched in foreground mode (attached to a terminal).

* Basic command-line knowledge is needed in order to proceed

First stop Zope if it is running as a background process

* On Windows: use Plone Control Panel or Windows Control Panel Services section to shutdown Plone first

* On Linux: use /etc/init.d/plone stop or related command to shutdown Plone

Use the command

.. code-block:: console

        bin/instance fg

or Windows command-line command (note that Plone location may depend on where you installed it)

.. code-block:: console

        cd "C:\Program files\Plone"
        bin\instance.exe fg

to start Plone.

All errors will be printed into the terminal.
The error is printed as Python *traceback*.
It is important to copy-paste all lines of this traceback, not just the last line.

If there is no start up error you will see the line::

  INFO Zope Ready to handle requests

as the last line of the startup sequence.


No such file or directory: 'zope.conf'
+++++++++++++++++++++++++++++++++++++++++

Example:

.. code-block:: console

    sudo /Applications/Plone/zinstance/bin/plonectl start
    instance: Error: error opening file /Applications/Plone/zinstance/parts/instance/etc/zope.conf: [Errno 2] No such file or directory: '/Applications/Plone/zinstance/parts/instance/etc/zope.conf'

This means that running ``bin/buildout`` script did not complete successfully.
Re-run buildout and see what's wrong.

Dropping into pdb
+++++++++++++++++++++++

If you need to inspect start-up errors in Python's :doc:`debugger </develop/debugging/pdb>`.

Activate Python configuration associated with your ``bin/instance`` script:

.. code-block:: console

    source ~/code/collective.buildout.python/python-2.6/bin/activate

Start Plone pdb enabled:

.. code-block:: console

    python -m pdb bin/instance fg

Check if Plone is up and responds to requests
-----------------------------------------------

Enter to the computer running Plone (SSH in on UNIX).

Use ``telnet`` command to connect Plone port and see if you get valid HTTP response from Plone

.. code-block:: console

     telnet localhost 8080

Then do a human HTTP user agent simulation by typing::

     GET / HTTP/1.0<enter><enter>

Plone response looks like this::

    Trying 127.0.0.1...
    Connected to localhost.localdomain.
    Escape character is '^]'.
    GET / HTTP/1.0

    HTTP/1.0 200 OK
    Server: Zope/(2.13.10, python 2.6.6, linux2) ZServer/1.1
    Date: Wed, 01 Feb 2012 09:59:40 GMT
    Content-Length: 1614
    Content-Type: text/html; charset=utf-8
    Connection: close

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

    <head>
    <base href="http://xxx.fi:9980/" />

If you get the answer from Plone (based on HTTP response headers) then Plone is running and you have problem elsewhere in your firewall/server/front-end web server configuration.

Consult your operating system manual for fixing your problem.

Cleaning up bad add-on uninstalls
------------------------------------

Many low quality Plone add-ons do not uninstall cleanly.

You need to remove persistent objects from the site database *after* add-on uninstall while *code is still in buildout*.

Otherwise your Plone site may not

* Pack properly

* Start properly

* Migrate to new version

For more information see :doc:`manual-remove-utility`


Not able to log in
------------------

It might happen that you start your instance with an empty database and you are not able to log in even if you are absolutely sure about your password.
If you work on localhost throw away the localhost related cookies in your browser and restart.

If you have lost the Zope Admin Password you can create an emergency user:

* http://quintagroup.com/services/support/tutorials/zope-access


More info
----------

* :doc:`common exceptions which you might encounter when starting Zope </manage/troubleshooting/exceptions>`

* `Plone community support guidelines for asking help <https://plone.org/help>`_
