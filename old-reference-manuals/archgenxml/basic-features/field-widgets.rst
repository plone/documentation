=======
Widgets
=======

.. contents :: :local:

.. admonition:: Description

        Setting up the Widgets for each field.

ArchGenXML will pick a default widget for your fields and fill in default labels and descriptions. For example, a ``string`` field gets a ``StringWidget`` by default, but a ``selection`` field type gets ``SelectionWidget`` on a StringField! You can override this in two ways. So ArchGenXML mixes up fields and widgets slightly for convinience reasons. Anyway, you can override all predefined definitions using widget options.

Widget options are specified with the prefix ``widget:``. As with normal field tagged values, unrecognised options will be passed straight through to the widget definition.

The most common widget options are:

widget:type -- sets the widget type used. Its the name of the widget class. You can use all widgets shipped within the Archetypes-Framework by just providing this tagged value. To use 3rd-Party widgets you additionally need to import the class using the *imports* tagged value on class level.

``widget:label`` -- sets the widget's label

``widget:description`` -- sets the widget's description

``widget:label_msgid`` -- overrides the default label message id (i18n)

``widget:description_msgid`` -- overrides the default description message id (i18n)

``widget:i18n_domain`` -- sets the i18n domain (defaults to the product name)

You may also use widget-specific options, such as ``widget:size`` where they apply. Look up possible widget-specific options at the documentation of the widget you want to use.


Changing the default widgets
----------------------------
To change the widget used for one field-type for a whole model, a product, a package or just for all fields in one class you can set on the product, package or class level the tagged value ``default:widget:FIELDNAMEABBREVIATION`` to ``WIDGETNAME``. For example use the tagged value ``default:widget:Reference`` set it to ``ReferenceBrowserWidget`` to use the ReferenceBrowserWidget instead of the ReferenceWidget. You might also want to also use the ``imports`` tagged value and set it to ``from ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget`` on your class to ensure that you get the widget definition imported into your class.

Creating new widgets
--------------------
To define a new widget add a class to your model with the ``<<widget>>`` stereotype.
