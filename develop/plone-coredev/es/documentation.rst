.. -*- coding: utf-8 -*-

Escribiendo documentación

Documentación de Plone
----------------------

Como una comunidad, Plone mantienen muchos tipos de documentación:

* Documentos *mantenidos*. Esto es un conjunto limitado de documentación que está pretendido para ser cuidadosamente dirigido y regularmente actualizado.

  * `Manual de Usuario <https://plone.org/documentation/manual/plone-4-user-manual>`_.
  * `Instalando Plone <http://plone-spanish-docs.readthedocs.org/en/latest/manuales/instalando_plone.html>`_, la versión original de esta documentación en Ingles esta disponible como `Installing Plone <https://plone.org/documentation/manual/installing-plone>`_.
  * `Referencia de Temas <http://developer.plone.org/#theme-development>`_
  * `Manual de Desarrollo <http://developer.plone.org/>`_

  Las mejoras a los documentos mantenidos pueden ser discutidos en la lista de correo `plone-docs <https://lists.sourceforge.net/lists/listinfo/plone-docs>`_.

* Documentos *editado colectivamente en comunidad*. Estos son abiertos para contribuciones por cualquier que lo deseo hacer. Esto dirige a una riqueza de información que es de más ampliamente variando calidad.

  * `Base de conocimiento en plone.org <https://plone.org/documentation/kb>`_. Cualquiera con una cuenta en plone.org es libre de editarlo.
  * `Documentación para el programador en Plone Collective <http://developer.plone.org/index.html>`_. Cualquiera tal ves puede `contribuir <http://collective-docs.readthedocs.org/en/latest/introduction/developermanual.html>`_.

Documentando un paquete
-----------------------

Lo básico
~~~~~~~~~

Al menos, su paquete tendría que incluir las siguientes formas de documentación

  :file:`README.rst`
    El archivo README es el primer punto de partida para la mayoría de personas a su paquete. Este será incluido en la página PyPI en su paquete Egg, y en la página de su repositorio github. Este tendrá que ser formateado utilizando `reStructuredText (reST) <http://docutils.sourceforge.net/rst.html>`_ para conseguir el formato apropiado por aquellos sistemas.

    :file:`README.rst` tendría que incluir:

    * Una breve descripción del propósito del paquete
    * Información de instalación (Cómo consigo que funcione?)
    * Información de compatibilidad (qué versiones de Plone trabaja con que?)
    * Enlaces a otras fuentes de documentación
    * Enlaces para reportar errores, listas de correo, y otras maneras de conseguir ayuda.

  El manual (a.k.a. documentación narrativa)

    El manual va a una profundidad más lejana para personas que quieren saber todo acerca de cómo para utilizar el paquete.

    Este incluye temas como los siguientes:

    * ¿Qué características poseen?
    * Documentos ¿Cómo usar? (¡doctests que no estén en Inglés!)
    * Información aproximadamente de la arquitectura
    * Común gotchas

    El manual debería considerar varias audiencias quiénes pueden necesitar tipos diferentes de información

    * Los usuarios finales quiénes utilizan Plone para editar contenido pero no administran el sitio.
    * Los administradores del sitio quiénes instalan y configurar el paquete.
    * Los integradores quiénes necesitan extender la funcionalidad del paquete desde el código fuente.
    * Los administradores de sistemas quiénes necesitan mantener que el servidor ejecute el software.

    Los paquetes sencillos con funcionalidad limitada pueden ser una página sola de narrativa documentación. En este caso es más sencillo de incluir él un extendido :file:`README.rst`. Algunos ejemplos excelentes de una página sencilla de archivo readme son https://pypi.python.org/pypi/plone.outputfilters y https://github.com/plone/plone.app.caching

    Si su proyecto es moderadamente complejo, puedes querer instalar su documentación con páginas múltiples. La manera mejor de hacer este es para añadir Sphinx a su proyecto y hospedar su documentos en readthedocs.org de modo que reconstruye la documentación siempre que aplica un cambio en github.com Si tú hace esto, su :file:`README.rst` debe que enlazar fuera sitio a la documentación.

  Referencia (a.k.a.  documentación de API)

    Una referencia de API proporciona información sobre la API pública del paquete (eso es, el código que el paquete expone para uso de código externo.)  Eso significa para el acceso aleatorio a recordar el lector de cómo una clase particular o un método trabajo, más que para leer enteramente.

    Si el código base está escrito con docstrings, la documentación de la API puede ser automáticamente generada utilizando Sphinx.

  :file:`CHANGES.txt`
    El changelog o registro de cambios es un registro de todos los cambios que hizo al paquete y quién les hicieron, con los cambios más recientes en la parte superior. Esto está mantenido por separado del historial de revisión del git para dar una posibilidad de mensajes mas amigables al usuario al registrar cuándo las liberaciones estuvieran listas.

    Un changelog se parece a algo así::

      Changelog
      =========

      1.0 (2012-03-25)
      ----------------

      * Documented changelogs.
        [davisagli]

    Ver https://raw.github.com/plone/plone.app.caching/master/CHANGES.rst para un ejemplo completo.

    Si un cambio sucedió relacionado a un error en el sistema de ticket, en la entrada changelog tendría que incluir un enlace a aquel asunto.

  Licencias
    Información sobre la licencia del código abierto utilizada para el paquete tendría que ser colocado dentro del directorio :file:`docs`.

    Para paquetes del núcleo Plone, esto incluye :file:`LICENSE.txt` y :file:`LICENSE.GPL`.


Utilizando Sphinx
~~~~~~~~~~~~~~~~~

Referencias reST:
 * `Documentación Shpinx orientada a Plone <http://developer.plone.org/reference_manuals/active/writing/index.html>`_
 * `Manual básico Sphinx reST <http://sphinx-doc.org/rest.html>`_

