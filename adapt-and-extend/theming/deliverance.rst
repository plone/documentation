===================
 Deliverance
===================

.. contents :: :local:

Introduction
------------

This page contains info for using Deliverance theming proxy with Plone.

Simple start script
--------------------

Example::

        #!bin/bash
        #
        # Run in /srv/plone/yourbuildoutfolder as plone user
        #
        # Deliverance will run in port 9000
        #
        # 1. Login http://yoursite.com:9000/.deliverance/login admin/x
        #
        # 2. Get debug output http://yoursite.com:9000/?deliv_log
        
        # Deliverance Python files are added to PYTHONPATH
        # and they are maintained under SVN version control
        export PYTHONPATH=src/plonetheme.yoursite/deliverance
        # Start virtualenv tuned for deliverance
        source deliverance-install/py25/bin/activate
        deliverance-proxy src/plonetheme.yoursite/deliverance/etc/deliverance.xml


Buildout restart snippet
--------------------------------

For *rundeliverance.sh* see above.

Example::

        #!/bin/sh
        # Restart script
        sudo -H -u yourdeliveranceuser kill `cat path/to/deliverance/var/deliverance.pid`
        sudo -H -u yourdeliveranceuser nohup bash rundeliverance.sh &
        
