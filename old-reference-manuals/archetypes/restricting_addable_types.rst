==========================
Restricting addable types
==========================

.. admonition:: Description

		The constrain-types machinery and how it drives the "restrict..."
		option under the "add item" menu.

As of Plone 2.1, the “add item” menu supports a “restrict…” page that
lets the user decide which items can and cannot be added to that folder.
This functionality is defined in a pair of interfaces in
``CMFPlone.interfaces.constrains``, ``IConstrainTypes`` for read-only access
and ``ISelectableConstrainTypes`` for the mutators.
The canonical implementation of these interfaces is in
``ATContentTypes.lib.constraintypes``. This provides storage for the
constraint mode (more below) and the list of locally allowed and
“preferred” types. The preferred types are the ones that appear in the
list immediately, and the rest of the allowed types appear behind a
“more…” item.
The constraint type mode can be ``ACQUIRE`` (the default), ``DISABLED`` or
``ENABLED``. When disabled, the settings in ``portal\_types`` are used. When
enabled, the list of types explicitly set are used. When set to acquire,
the parent folder`s types will be used \*if\* the parent is of the same
portal type as the folder in question. If they are of different types
the settings in ``portal\_types`` apply.
The rest of the ``ConstrainTypesMixin`` class overrides CMFCore`s
``allowedContentTypes`` and ``invokeFactory`` methods to ensure the
constraints are enforced.
