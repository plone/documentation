.. -*- coding: utf-8 -*-

Guía de estilos
===============

Python, como cualquier lenguaje de programación, puede ser escrito en un número de estilos. ¡Somos los primeros en admitir que Zope y Plone no son los mejores ejemplos de la integridad estilística, pero eso no nos impide intentarlo!

Si no estas familiarizado con `PEP 8 <http://www.python.org/dev/peps/pep-0008>`_ - la guía de estilo de la python, por favor, tome un momento para leer y ponerse al día. Nosotros no requerimos, pero nosotros, como comunidad realmente, realmente lo apreciamos.

Convenciones de nombre
----------------------
¡Por encima de todo, ser coherente con cualquier código que usted está modificando! Históricamente, el código es todo camel case, pero muchas nuevas bibliotecas se encuentran en la convención PEP8. La lista de correo es la explosión de debates sobre que es lo mejor, así que nosotros vamos a dejar el ejercicio de decidir qué hacer con el usuario de esta lista.

Convenciones de Archivo
-----------------------
En Zope 2, los nombres de archivos que solía ser así MixedCase. En Python, y así en Plone yendo de frente, preferimos todos los nombres de archivos en minúsculas. Esto tiene la ventaja de que usted puede ver inmediatamente si se refiere a un módulo / archivo o una clase::

  from zope.pagetemplate.pagetemplate import PageTemplate

comparar eso a::

  from Products.PageTemplates.PageTemplate import PageTemplatePageTemplate

Los nombres de archivos debe ser ordenados y descriptivos. Piensa acerca de como un import podría leerse::

  from Products.CMFPlone.utils import safe_hasattr

comparar eso a::

  from Products.CMFPlone.PloneUtilities import safe_hasattr

A la primera es, obviamente, mucho más fácil de leer, menos redundante y por lo general estéticamente más agradable.

.. note::
    Este ejemplo es casi tan terrible como el que viene. Necesitamos una mejor.

Reglas específicas
------------------
 * ¡No utiliza tabuladores en código de Python! Use espacios como indentado, a 4 espacios para cada nivel. Nosotros no **"requerimos"** `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_, pero mucha gente lo usa y eso es bueno para usted.
 * Indentar apropiadamente, incluso en HTML.
 * Nunca usar una excepción bare. Cualquier cosa como ``except: pass`` es probable que sea revertido instantáneamente
 * Evitar ``tal:on-error``, desde estas excepciones swallows
 * No use ``hasattr()`` - esto son swallows exceptions, por favor, en este caso use ``getattr(foo, 'bar', None)``. El problema con las swallowed exceptions,no es sólo el informe de errores pobre. Esto también puede enmascarar conflictos de errores (``ConflictErrors``), que indican que algo ha ido mal en el `nivel de la ZODB <http://developer.plone.org/troubleshooting/transactions.html#conflicterror>`_!
 * Nunca, coloque ningún código HTML dentro del código Python y lo retorne como una cadena
 * No adquirir nada menos que sea absolutamente necesario, especialmente herramientas. Por ejemplo, en vez de utilizar ``context.plone_utils``, use::

    from Products.CMFCore.utils import getToolByName
    plone_utils = getToolByName(context, 'plone_utils')

 * No coloque mucho de la lógica en las Plantillas de pagina Zope - ZPT (use `Views <http://developer.plone.org/views/index.html>`_ en este caso!)
 * Recuerde agregar etiquetas `i18n <http://developer.plone.org/i18n/index.html>`_ en ZPTs y código Python
