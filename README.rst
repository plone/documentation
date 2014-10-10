========================================
This is the official Plone Documentation
========================================

maintained by the Plone Docs-Team

You can read the documentation on http://docs.plone.org

If you want to contribute, please read:

http://docs.plone.org/about/contributing.html

thanks,

the documentation team




If you want to have a full and complete copy of the docs and the supporting buildout,
for now you can do the following on a \*\nix system::

    git clone https://github.com/plone/papyrus.git
    virtualenv --no-site-packages papyrus
    (make sure you have a 2.7 virtualenv)
    cd papyrus
    ./bin/python bootstrap.py
    bin/buildout
    (wait a bit, as this also enables robot-framework it needs to download quite a few eggs)
    make externals
    (this fetches the external packages whose docs-folder is part of this documentation)
    make html

and browse the results in ``build/html/``

