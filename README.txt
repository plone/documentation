hi there. Please don't put anything here yet. We're working on a future version of the Plone documentation here.


thanks,

the documentation team


If you want to take a sneak peek at the docs, for now you can do the following on a *nix system:

git clone https://github.com/plone/papyrus
virtualenv --no-site-packages papyrus
cd papyrus
./bin/python bootstrap.py
bin/buildout
(wait a bit)
make externals
make html

and browse the results in build/html/

