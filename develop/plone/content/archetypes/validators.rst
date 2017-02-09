==========
Validators
==========


Introduction
============

This page has tips how to validate fields defined in Archetypes schema.

List of default validators
==========================

* https://github.com/plone/Products.validation/blob/master/Products/validation/validators/BaseValidators.py

Creating a validator
====================

A custom validator should return True if valid, or an error string if validation fails.
This is especially important to remember when chaining validators together.
See the tutorials below for further details:

* http://play.pixelblaster.ro/blog/archive/2006/08/27/creating-an-archetypes-validator

* http://www.pererikstrandberg.se/blog/index.cgi?page=PloneArchetypesFieldValidator
