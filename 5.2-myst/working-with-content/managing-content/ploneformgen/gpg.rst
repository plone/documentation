======================
Using GnuPG encryption
======================

.. admonition:: Description

    The Gnu Privacy Guard may be used to encrypt emails sent by PloneFormGen.

.. warning::

    Encryption is serious business, and this how-to does not teach you about it or about the Gnu Privacy Guard. You should develop expertise with both of these before attempting to enable PFG encryption.

Using GPG encryption with PloneFormGen requires:

1) That gpg be installed on your system and available on the search path
or in a common location (e.g., /usr/bin);

2) That gpg, when executed as a subprocess of Zope/Plone, be able to
find a public keyring;

3) That gpg, when executed as a subprocess of Zope/Plone, have the
rights to read the public keyring;

4) That you, as administrator, understand how gpg works, and be able to
maintain the public keyring.

PloneFormGen tries to find the gpg binary when it's installed, when the
product code is refreshed, and when you restart Zope. If it finds it
you will see an "encryption" field set in the mailer adapter form. If
you don't see the "encryption" fieldset, it means PloneFormGen didn't
find a gpg binary. Fix this by adding the path to the gpg binary to the
PATH environment variable when you start Zope.

gpg will typically look for a public keyring in the current user's home
directory, .gnupg subdirectory. If it's not finding it, consider the
possibility that the user id you're using to maintain your keys isn't the
same one that you're using to run Zope. You may need to use the
GNUPGHOME environment variable to point to your .gnupg directory. Make
sure your Zope process can open the directory and read the file!

.. note:: Windows

    gpg can work in a Windows environment, but you'll need to have a
    command-line gpg. http://www.cygwin.com/ is a good, free source.
