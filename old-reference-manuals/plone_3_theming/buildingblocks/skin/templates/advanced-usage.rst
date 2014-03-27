Advanced Usage
==============

In this part we'll look at some more advanced features of the Template
Attribute Language, including a more in-depth look at the TAL Expression
Syntax (TALES).

Mixing and Matching Statements
------------------------------

As you have seen in the example template, you can put more than one TAL
statement on the same tag. There are three limits you should be aware
of, however:

#. Only one of each kind of statement can be used on a single tag. Since
   HTML does not allow multiple attributes with the same name, you can't
   have two ``tal:define`` on the same tag.

#. Both of ``tal:content`` and ``tal:replace`` cannot be used on the
   same tag, since their functions conflict.

#. The order in which you write TAL attributes on a tag does not affect
   the order in which they execute. No matter how you arrange them, the
   TAL statements on a tag always execute in the following order:
   ``define``, ``condition``, ``repeat``, ``content`` / ``replace``,
   ``attributes``.

To get around these limits, you can add another tag and split up the
statements between the tags. If there is no obvious tag type that would
fit, use ``span`` or ``div``.

For example, if you want to define a variable for each repetition of a
paragraph, you can't place the ``tal:define`` on the same tag as the
``tal:repeat``, since the definition would happen before all of the
repetitions. Instead, you would write either of the following:

::

          <div tal:repeat="ph phrases">
            <p tal:define="n repeat/ph/number">
            Phrase number <span tal:replace="n">1</span> is
            <b tal:content="ph">Phrase</b>.</p>
          </div>

          <p tal:repeat="ph phrases">
            <span tal:define="n repeat/ph/number">
            Phrase number <span tal:replace="n">1</span> is
            <b tal:content="ph">Phrase</b>".</span>
          </p>

Note: the definition of "n" is actually not much useful in this example
because we could have directly used "repeat/ph/number" in the replace
attribute which only occurs once, but it serves our purpose.

Statements with Multiple Parts
------------------------------

If you need to set multiple attributes on a tag, you can't do it by
placing multiple ``tal:attributes`` statements on the tag, and splitting
them across tags is useless.

Both the ``tal:attributes`` and ``tal:define`` statements can have
multiple parts in a single statement. You separate the parts with
semicolons (``;``), so any semicolon appearing in an expression in one
of these statements must be escaped by doubling it (``;;``). Here is an
example of setting both the ``src`` and ``alt`` attributes of an image:

::

          <img src="default.jpg"
               tal:attributes="src item/icon; alt item/id">

Here is a mixture of variable definitions:

::

          <span tal:define="global logo context/logo.gif; ids context/objectIds">

**Note:** in Plone 4 or newer you can use *context/items* instead of
*context/objectIds*.

String Expressions
------------------

String expressions allow you to easily mix path expressions with text.
All of the text after the leading ``string:`` is taken and searched for
path expressions. Each path expression must be preceded by a dollar sign
(``$``). If it has more than one part, or needs to be separated from the
text that follows it, it must be surrounded by braces (``{}``). Since
the text is inside of an attribute value, you can only include a double
quote by using the entity syntax ``&quot;``. Since dollar signs are used
to signal path expressions, a literal dollar sign must be written as two
dollar signs (``$$``). For example:

::

          <span tal:replace="string:Just text."/>
          <span tal:replace="string:© $year, by Me."/>
          <span tal:replace="string:Three ${vegetable}s, please."/>
          <span tal:replace="string:Your name is ${user/getUserName}!"/>
          <span tal:replace="string:She answered &quot;$answer&quot;."/>
          <span tal:replace="string:This product costs $price $$."/>

Nocall Path Expressions
-----------------------

An ordinary path expression tries to render the object that it fetches.
This means that if the object is a function, Script, Method, or some
other kind of executable thing, then the expression will evaluate to the
result of calling the object. This is usually what you want, but not
always. For example, if you want to put a DTML Document into a variable
so that you can refer to its properties, you can't use a normal path
expression because it will render the Document into a string.

If you put the ``nocall:`` expression type prefix in front of a path, it
prevents the rendering and simply gives you the object. For example:

::

          <span tal:define="doc nocall:context/aDoc"
                tal:content="string:${doc/id}: ${doc/title}">
          Id: Title</span>

This expression type is also valuable when you want to define a variable
to hold a function or class from a module, for use in a Python
expression.

Other Builtin Variables
-----------------------

You have already seen some examples of the builtin variables
``template``, ``user``, ``repeat``, and ``request``. Here is a more
complete list of the other builtin variables and their uses:

nothing
    A false value, similar to a blank string, that you can use in
    ``tal:replace`` or ``tal:content`` to erase a tag or its contents.
    If you set an attribute to ``nothing``, the attribute is removed
    from the tag (or not inserted), unlike a blank string. Equivalent to
    ``None`` in Python.
default
    A special value that doesn't change anything when used in
    ``tal:replace``, ``tal:content``, or ``tal:attributes``. It leaves
    the template text in place.
options
    The *keyword* arguments, if any, that were passed to the template.
attrs
    A dictionary of attributes of the current tag in the template. The
    keys are the attributes names, and the values are the original
    values of the attributes in the template.
root
    The root Zope object. Use this to get Zope objects from fixed
    locations, no matter where your template is placed or called.
context
    The object on which the template is being called. This is often the
    same as the *container*, but can be different if you are using
    acquisition. Use this to get Zope objects that you expect to find in
    different places depending on how the template is called.
here
    An (older) alias for *context*.
container
    The container (usually a Folder) in which the template is kept. Use
    this to get Zope objects from locations relative to the template's
    permanent home.
request
    Contains the complete information about the current HTTP request
    that Zope is processing. See `this page in the zope.org
    wiki <http://wiki.zope.org/zope2/REQUESTX>`_ for further info about
    the request object.
modules
    The collection of Python modules available to templates. See the
    section on writing Python expressions.
view
    For templates called from a Zope 3-style view *only*, this variable
    refers to the associated view class. This may then contain functions
    and variables prepared explicitly for the template to output

Alternate Paths
---------------

The path ``template/title`` is guaranteed to exist every time the
template is used, although it may be a blank string. Some paths, such as
``request/form/x``, may not exist during some renderings of the
template. This normally causes an error when the path is evaluated.

When a path doesn't exist, you often have a fallback path or value that
you would like to use instead. For instance, if ``request/form/x``
doesn't exist, you might want to use ``context/x`` instead. You can do
this by listing the paths in order of preference, separated by vertical
bar characters (``|``):

::

          <h4 tal:content="request/form/x | context/x">Header</h4>

Two variables that are very useful as the last path in a list of
alternates are ``nothing`` and ``default``. Use ``nothing`` to blank the
target if none of the paths is found, or ``default`` to leave the
example text in place.

You can also test the existence of a path directly with the ``exists:``
expression type prefix. A path expression with ``exists:`` in front of
it is true if the path exists, false otherwise. These examples both
display an error message only if it is passed in the request:

::

          <h4 tal:define="err request/form/errmsg | nothing"
              tal:condition="err" tal:content="err">Error!</h4>

          <h4 tal:condition="exists:request/form/errmsg"
              tal:content="request/form/errmsg">Error!</h4>

Dummy Elements
--------------

You can include page elements that are visible in the template but not
in generated text by using the builtin variable ``nothing``, like this:

::

          <tr tal:replace="nothing">
            <td>10213</td><td>Example Item</td><td>$15.34</td>
          </tr>

This can be useful for filling out parts of the page that will take up
more of the generated page than of the template. For instance, a table
that usually has ten rows will only have one row in the template. By
adding nine dummy rows, the template's layout will look more like the
final result.

Inserting Structure
-------------------

Normally, the ``tal:replace`` and ``tal:content`` statements quote the
text that they insert, converting ``<`` to ``&lt;``, for instance. If
you actually want to insert the unquoted text, you need to precede the
expression with the ``structure`` keyword. Given a variable
``copyright`` with a string value of "© 2008 By <b>Me</b>", the
following two lines:

::

          <span tal:replace="copyright">Copyright 2008</span>
          <span tal:replace="structure copyright">Copyright 2008</span>

...will generate "© 2001 By <b>Me</b>" and "© 2001 By **Me**",
respectively.

This feature is especially useful when you are inserting a fragment of
HTML that is stored in a property or generated by another Zope object.
For instance, you may have news items that contain simple HTML markup
such as bold and italic text when they are rendered, and you want to
preserve this when inserting them into a "Top News" page. In this case,
you might write:

::

          <p tal:repeat="article topnewsitems"
             tal:content="structure article">A News Article</p>

Basic Python Expressions
------------------------

A Python expression starts with ``python:``, followed by an expression
written in the Python language. Python is a simple and expressive
programming language. If you have never encountered it before, you
should read one of the excellent tutorials or introductions available at
the official website `http://www.python.org <http://www.python.org/>`_.

A Page Template Python expression can contain anything that the Python
language considers an expression. You can't use statements such as
``if`` and ``while``, and Zope's security restrictions are applied.

Comparisons
^^^^^^^^^^^

One place where Python expressions are practically necessary is in
``tal:condition`` statements. You usually want to compare two strings or
numbers, and there isn't any other way to do that. You can use the
comparison operators ``<`` (less than), ``>`` (greater than), ``==``
(equal to), and ``!=`` (not equal to). You can also use the boolean
operators ``and``, ``not``, and ``or``. For example:

::

            <p tal:repeat="widget widgets">
              <span tal:condition="python:widget.type == 'gear'">
              Gear #<span tal:replace="repeat/widget/number">1</span>:
              <span tal:replace="widget/name">Name</span>
              </span>
            </p>

Sometimes you want to choose different values inside a single statement
based on one or more conditions. You can do this with the ``test``
function, like this:

::

            You <span tal:define="name user/getUserName"
                  tal:replace="python:test(name=='Anonymous User', 'need to log in', default)">
                  are logged in as
                  <span tal:replace="name">Name</span>
                </span>

            <tr tal:define="oddrow repeat/item/odd"
                tal:attributes="class python:test(oddrow, 'oddclass', 'evenclass')">

Using other Expression Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can use other expression types inside of a Python expression. Each
type has a corresponding function with the same name, including
``path()``, ``string()``, ``exists()``, and ``nocall()``. This allows
you to write expressions such as:

::

            "python:path('context/%s/thing' % foldername)"
            "python:path(string('context/$foldername/thing'))"
            "python:path('request/form/x') or default"

The final example has a slightly different meaning than the path
expression "request/form/x \| default", since it will use the default
text if "request/form/x" doesn't exists *or* if it is false.

Getting at Zope Objects
-----------------------

Much of the power of Zope involves tying together specialized objects.
Your Page Templates can use Scripts, SQL Methods, Catalogs, and custom
content objects. In order to use them, you have to know how to get
access to them.

Object properties are usually attributes, so you can get a template's
title with the expression "template.title". Most Zope objects support
acquisition, which allows you to get attributes from "parent" objects.
This means that the Python expression "context.Control\_Panel" will
acquire the Control Panel object from the root folder. Object methods
are attributes, as in "context.objectIds" and "request.set". Objects
contained in a folder can be accessed as attributes of the folder, but
since they often have Ids that are not valid Python identifiers, you
can't use the normal notation. For example, instead of writing
"context.penguin.gif", you must write "getattr(context, 'penguin.gif')".

Some objects, such as ``request``, ``modules``, and Zope Folders support
item access. Some examples of this are:

::

          request['URL'], modules['math'], and context['thing']

When you use item access on a Folder, it doesn't try to acquire the
name, so it will only succeed if there is actually an object with that
Id contained in the folder.

Path expressions allow you to ignore details of how you get from one
object to the next. Zope tries attribute access, then item access. You
can write "context/images/penguin.gif" instead of
"python:getattr(context.images, 'penguin.gif')", and "request/form/x"
instead of "python:request.form['x']".

The tradeoff is that path expressions don't allow you to specify those
details. For instance, if you have a form variable named "get", you must
write "python:request.form['get']", since "request/form/get" will
evaluate to the "get" *method* of the form dictionary.

Using Scripts
-------------

Script objects are often used to encapsulate business logic and complex
data manipulation. Any time that you find yourself writing lots of TAL
statements with complicated expressions in them, you should consider
whether you could do the work better in a script.

Each script has a list of parameters that it expects to be given when it
is called. If this list is empty, then you can use the script by writing
a path expression. Otherwise, you will need to use a Python expression,
like this:

::

          "python:context.myscript(1, 2)"
          "python:context.myscript('arg', foo=request.form['x'])"

If you want to return more than a single bit of data from a script to a
page template, it is a good idea to return it in a dictionary. That way,
you can define a variable to hold all the data, and use path expressions
to refer to each bit. For example, supposing we have a ``getPerson``
script which returns a dictionary like ``{'name':'Fred', 'age':25}``:

::

          <span tal:define="person context/getPerson"
                tal:replace="string:${person/name} is ${person/age}">
          Name is 30</span> years old.

Calling DTML
------------

DTML is another templating language made available by Zope, mostly
replaced by ZPT nowadays, but still in use. You can read more about it
in `the relevant chapter of the Zope
Book <http://www.zope.org/Documentation/Books/ZopeBook/current/DTML.stx>`_.

Unlike Scripts, DTML Methods don't have an explicit parameter list.
Instead, they expect to be passed a client, a mapping, and keyword
arguments. They use these to construct a namespace.

When Zope's ZPublisher publishes a DTML object, it passes the context of
the object as the client, and the REQUEST as the mapping. When one DTML
object calls another, it passes its own namespace as the mapping, and no
client.

If you use a path expression to render a DTML object, it will pass a
namespace with ``request``, ``context``, and the template's variables
already on it. This means that the DTML object will be able to use the
same names as if it were being published in the same context as the
template, plus the variable names defined in the template.

Python Modules
--------------

The Python language comes with a large number of modules, which provide
a wide variety of capabilities to Python programs. Each module is a
collection of Python functions, data, and classes related to a single
purpose, such as mathematical calculations or regular expressions.

Several modules, including "math" and "string", are available in Python
Expressions by default. For example, you can get the value of *pi* from
the math module by writing "python:math.pi". To access it from a path
expression, however, you need to use the ``modules`` variable. In this
case, you would use "modules/math/pi". Please refer to the Zope Book or
a DTML reference guide for more information about these modules.

The "string" module is hidden in Python expressions by the "string"
expression type function, so you need to access it through the
``modules`` variable. You can do this directly in an expression in which
you use it, or define a global variable for it, like this:

::

          tal:define="global mstring modules/string"
          tal:replace="python:mstring.join(slist, ':')"

Modules can be grouped into packages, which are simply a way of
organizing and naming related modules. For instance, Zope's Python-based
Scripts are provided by a collection of modules in the "PythonScripts"
subpackage of the Zope "Products" package. In particular, the "standard"
module in this package provides a number of useful formatting functions
that are standard in the DTML "Var" tag. The full name of this module is
"Products.PythonScripts.standard", so you could get access to it using
either of the following statements:

::

          tal:define="pps modules/Products.PythonScripts.standard"
          tal:define="pps python:modules['Products.PythonScripts.standard']"

Most Python modules cannot be accessed from Page Templates, DTML, or
Scripts unless you add Zope security assertions to them. That's outside
the scope of this document, and is covered by the `Zope Security
Guide <http://www.zope.org/Documentation/Books/ZDG/current/Security.stx>`_.

Special HTML attributes
-----------------------

The HTML boolean attributes checked\ *,* selected, *nowrap*, *compact*,
*ismap*, *declare*, *noshade*, *disabled*, *readonly*, *multiple*,
*selected* and *noresize* are treated differently by tal:attributes. The
value is treated as true or false (as defined by tal:condition). The
attribute is set to attr=”attr” in the true case and omitted otherwise.
If the value is default, then it is treated as true if the attribute
already exists, and false if it does not. For example, each of the
following lines:

::

    <input type="checkbox" checked tal:attributes="checked default">
    <input type="checkbox" tal:attributes="checked string:yes">
    <input type="checkbox" tal:attributes="checked python:42">

will render as:

::

    <input type="checkbox" checked="checked">

while each of these:

::

    <input type="checkbox" tal:attributes="checked default">
    <input type="checkbox" tal:attributes="checked string:">
    <input type="checkbox" tal:attributes="checked nothing">

will render as:

::

    <input type="checkbox">

This article contains information and examples from the `Zope Book <http://docs.zope.org/zope2/zope2book/source/index.html>`_, © 
`Zope Developers Community. <http://docs.zope.org/zope2/zope2book/source/Contributions.html>`_
