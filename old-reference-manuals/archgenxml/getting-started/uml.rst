===
UML
===

.. contents :: :local:

.. admonition:: Description

        A brief introduction to UML and pointers to further readings.

UML |---| the Unified Modeling Language |---| is a graphical language
designed to describe software through formalised diagrams. There are several
different types of diagrams available, but the ones most relevant to ArchGenXML
are:

* The **class** diagram
* The **state** diagram

Class diagrams are used to draw *interfaces*, *content types* (represented as
classes) and *tools* (represented as classes with the ``portal_tool``
stereotype), as well as the *attributes* and *public operations* on these. In
addition, associations in the diagram show how objects are aggregated within or
referenced from one another.

The goal of model-driven development is to create the "blueprints" for your
software in a well-defined, easily-communicated format: the UML model and
diagram thereof. You can design your model using visual tools until you have a
structure which adequately represents your needs, and ArchGenXML will generate
the necessary code.

For all but the simplest products, you will have to customise that code
somewhat, filling in method bodies, creating new page templates, etc., but
ArchGenXML takes care of all the boilerplate for you. With tagged values and
stereotypes you can customise the generated code with a surprising degree of
flexibility and control, and when you need to hand-code something, ArchGenXML
won't overwrite your changes (provided you stick to the protected code
sections, clearly marked in the source code).

This manual does not aim to teach you UML and object-oriented, model-driven
software development. There are several other fine manuals about that on the
web. A very good starting point is the `OMG UML Resource Page
<http://www.uml.org/>`_, including its web-links to tutorials.

For a quick-start read `Practical UML
<http://bdn.borland.com/article/0,1410,31863,00.html>`_
chapters 'class-diagram' and 'state-chart-diagram'.

.. |---| unicode:: U+02014 .. em dash
