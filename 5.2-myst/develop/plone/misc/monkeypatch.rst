====================
 Monkey-patching
====================

A monkey patch (also spelled monkey-patch, MonkeyPatch) is a way to
extend or modify the runtime code of dynamic languages (e.g. Smalltalk,
JavaScript, Objective-C, Ruby, Perl, Python, Groovy, etc.) without
altering the original source code.

Plone community promotes conflict free way to do monkey patching
using `collective.monkeypatcher package
<https://pypi.python.org/pypi/collective.monkeypatcher>`_.

Patching constants
====================

Some modules (typically ``config.py`` files) include constant
definitions used throughout the package. Given that
``collective.monkeypatcher`` is intended to patch methods
you'll not be able to patch a constant straightforward. Instead you'll
have to make use of the ``handler`` option::

    <monkey:patch
        description="Add new terabyte constant"
        class="Products.CMFPlone.CatalogTool.CatalogTool"
        original="SIZE_CONST"
        replacement=".patches.patched_size_const"
        handler=".patches.apply_patched_const"
        />

And your ``patches.py`` module should include this::


    NEW_SIZE_CONST = {'kB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024, 'TB': 1024*1024*1024*1024}

    patched_size_const = lambda : NEW_SIZE_CONST  # Now we have a callable method!

    def apply_patched_const(scope, original, replacement):
        setattr(scope, original, replacement())
        return


This way the **original** ``SIZE_CONST`` constant would be replaced by
the result of the lambda function, which is our new constant.

Patching @property methods
==========================

If you are to patch a ``@property`` decorated method you can use the
``handler`` configuration option::


    <monkey:patch
        description="Performance boost in foldercontents"
        class="plone.app.content.browser.foldercontents.FolderContentsTable"
        original="items"
        replacement=".patches.patched_items"
        handler=".patches.apply_patched_property"
        />


And your ``patches.py`` module should include this::


    def items(self):
        ...  # The body of your patched method


    def apply_patched_property(scope, original, replacement):
        # This is actually the same as apply_patched_const above
        setattr(scope, original, replacement())
        return

    patched_items = lambda : property(items)  # We get a @property decorated method!


This way the **original** ``items`` method would be replaced by the
result of the lambda function, which is a ``@property`` decorated
method written in a different way.
