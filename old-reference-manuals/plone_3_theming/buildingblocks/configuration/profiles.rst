Profiles
========

Configuration and profiles

Configuration refers to the default behaviour of a site (for instance,
whether you allow people to sign up to your site, or how dates are
displayed). You're likely to want some of this behaviour to be embedded
in your theme.

There is also some overlap between Components, Skins, and Configuration.
For instance, the order of skin layers and the order in which viewlets
appear within a viewlet manager are considered aspects of configuration.

Profile
-------

A profile is a set of configuration files. Each file is written in
fairly simple XML and refers to a particular group of components or page
elements. There are two different types of profile, base profiles and
extension profiles. For theme purposes you will only ever need to use an
extension profile (i.e., a profile that extends the configuration of an
existing site).

A profile comes into being when it is wired up by ZCML. Here's the
version created by the plone3\_theme paster template:

::

    <genericsetup:registerProfile
     name="default"
     title="[your skin name]"
     directory="profiles/default"
     description='Extension profile for the "[your skin name]" Plone theme.'
     provides="Products.GenericSetup.interfaces.EXTENSION"
    />

You'll see that it points at a directory for the location of the XML
files and indicates that it is an extension profile by using an
interface.
