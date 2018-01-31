How to set up your editor
=========================


`EditorConfig <http://editorconfig.org/>`_ provides a way to share the same configuration for all major source code editors.

You only need to install the plugin for your editor of choice, and add the following configuration on ``~/.editorconfig``.

.. code-block:: ini

    [*]
    indent_style = space
    end_of_line = lf
    insert_final_newline = true
    trim_trailing_whitespace = true
    charset = utf-8

    [*.{cfg,py}]
    indent_size = 4

    [*.{css,dtml,html,js,pt,xml,zcml,zpt}]
    indent_size = 2

    [Makefile]
    indent_style = tab


dotfiles
--------

Some Plone developers use dotfiles similar to these: `plone.dotfiles <https://github.com/plone/plone.dotfiles>`_. This might inspire you with your own dotfiles/configuration settings.

