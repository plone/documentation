=====================================
Add Your Changes To Multiple Branches
=====================================

.. topic:: Description

   How to cherry-pick your changes from one branch to another branch.


As this documentation is kept for multiple Plone versions,
there are times when a pull request should be merged to more than one branch.

Follow these steps to do so:

Make the changes targeting the latest release and create a pull request.

Once the pull request gets merged,
get to your terminal and *cherry-pick* the commits on the other branches.

For example,
after your pull request with one single commit (commit id ``abcdef``) on branch 5.1 got merged,
do the following to bring those changes to branch 5.0

.. code-block:: shell

    git clone git@github.com:plone/documentation
    cd documentation
    git checkout 5.0
    git cherry-pick abcdef
    git push

If it should go to even more branches, repeat the last three steps above.

If there are more than one single commit in the pull request,
repeat the :command:`cherry-pick` command as many times as needed.

.. note::  If the cherry-pick fails to apply the commit cleanly,
   you can use a diff tool to see what's the problem and solve it as you do with code.
