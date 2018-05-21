=====================
Templating In TinyMCE
=====================

TinyMCE in Plone 5 is adapted to allow templating engine for its content.

Right now parametrized templates are not implemented.

Enable
======

* On Control Panel -> TinyMCE -> Toolbar -> custom plugins add::

    template|+plone+static/components/tinymce-builded/js/tinymce/plugins/template

* On Control Panel -> TinyMCE -> Toolbar -> toolbar::

    undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | unlink plonelink ploneimage | template

Configure Templates
===================

For each template we need a file available on the browser, we assume for this
example to use a diazo file at ++theme+example/templates/template.html with
the content:

.. code-block:: html

    <div class="mceTmpl">
        <h1>Template</h1>
        <img src="++theme+example/templates/img/img1.png"/>
        <div class="row">
            <div class="col-md-6">
                <h2>Header</h2>
            </div>
            <div class="col-md-6">
                <h2>Header</h2>
            </div>
        </div>
    </div>

In order to define it::

    [
        {
            "title": "Template example",
            "url": "++theme++example/templates/template.html",
            "description": "Title with two columns"
        },
        {
            "title": "Template example2",
            "url": "++theme++example/templates/template2.html",
            "description": "Title with three columns."
        }
    ]
