.. -*- coding: utf-8 -*-

==========
Mr. Roboto
==========

GitHub push
===========

When a push happens on GitHub, ``mr.roboto`` is triggered so starts to analyze the push.

* If it's on ``buildout-coredev`` it starts the job of the branch that has been pushed.
  In this case we send to plone-cvs the commit to keep track of the commits on that list.
* If it's on a package that's on the :file:`sources.cfg` of a ``buildout-coredev`` it starts the coredev jobs that are linked to that package and a kgs job with that package.
  This kgs job is a snapshot of the last working version of the ``buildout.coredev`` with the newest version of the package that is involved on the push.
  This jobs are really fast as we only test the package applied to the kgs plone/python version ``coredev`` buildout.
* If it's on a plip specification it runs the job that is configured Through The Web on ``mr.roboto`` interface. (http://jenkins.plone.org/roboto/plips)

Job finishes
============

When jenkins finish a job it does a callback to ``mr.roboto`` in order to :

* If it comes from a ``coredev`` job,
  all the ``coredev`` jobs related to that push are finished writes a comment on the GitHub commit with all the information
  (once and with all the information so no more empty mails from gh notification system)
* If it comes from a kgs job and all the kgs jobs are finished,
  (that may take max 10 min)
  and some has failed we send a mail to testbot mailing list saying that a commit failed on kgs job.
  We also send a mail to `plone-cvs <https://lists.sourceforge.net/lists/listinfo/plone-cvs>`_ with the information to keep track of all the commits.
* If it comes from a kgs job and all the kgs jobs are finished,
  and all are working we send a mail to `plone-cvs <https://lists.sourceforge.net/lists/listinfo/plone-cvs>`_ with the information to keep track of all the commits.

For all kgs jobs jenkins sends a mail to the author with the results when is finished.

All the notifications has a url like: http://jenkins.plone.org/roboto/get_info?push=9a183de85b3f48abb363fa8286928a10.

On this url there is the commit, who, the diff, the files and the result for each jenkins job.


* `plone-testbot <http://lists.plone.org/mailman/listinfo/plone-testbot>`_ mailing list is receiving only when a test fails on kgs environment and may take max 10 min from the push.
* `plone-cvs <https://lists.sourceforge.net/lists/listinfo/plone-cvs>`_ always has the commit there with the diff and the information and may take 10 min to get there after the push.
* author receives the results of tests failing against kgs on 10 min

.. note::
    In case of integration errors with other packages that may fail because of the push kgs will not be aware of that,
    so it's important that at the end
    (and after the 50' that takes the ``coredev`` jobs you also check the latest version of ``coredev`` with your push)
