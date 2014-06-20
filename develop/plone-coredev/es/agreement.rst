.. -*- coding: utf-8 -*-

Contribuyendo al núcleo de Plone
================================

Hay muchas personas y compañías quiénes confían en Plone diariamente, por tanto nosotros tenemos que introducir algún nivel de control en la calidad del código fuente. Todo el código de fuente de Plone es hospedado en un repositorio git en https://github.com/plone, solo para los miembros del equipo de desarrollado que tienen derecho de hacer revisiones.

El enviar el acuerdo de contribuciones (contributors agreement) no garantiza que se otorguen acceso al repositorio, pero una vez que lo envía siempre lo tenemos en el archivo para cuando usted está listo para contribuir. Nosotros pedimos que antes de solicitar el acceso de escritura al núcleo de Plone, usted debe familiarizarse un poco con la comunidad, ya que le ayudará a acelerar su iniciación:

* Preguntar y (especialmente) responder a preguntas en el sitio web `stack overflow <http://stackoverflow.com/>`_ y canal :doc:`IRC <culture>` con un enfoque para conocer un poco a los desarrolladores activos.

* Asistir una `conferencia <http://plone.org/events/conferences>`_ / un `simposio <http://plone.org/events/regional>`_ o participar en un `sprints <http://plone.org/events/sprints>`_ / `tune-ups <http://plone.org/events/plone-tuneups>`_. Hay abundancia de oportunidades de conocer la comunidad y comenzar a contribuir a través de varias sesiones de programación, ya sea en persona o en la web. Usted puede incluso ser capaz de obtener acceso inmediato en una conferencia si usted ha demostrando sus habilidades de programación y las personas adecuada asisten.

* Puede iniciarse en la contribuciones en el repositorio de `collective <http://collective.github.com/>`_. No se preocupe por hacer todo perfecto o no complique al pedir ayuda, de esta forma usted nos hace saber a nosotros como mejorar nuestro código juntos como una comunidad.

* **Parches / Patches:** Históricamente nosotros animamos a las personas para entregar parches *(patches)* al colector del ticket. Estos tickets suelen ser ignorados para siempre. Técnicamente, para que nosotros aceptemos su parche usted debe firmar el *contributor agreement*. Si usted quiere contribuir a corregir del código, por favor sólo debe firmar el acuerdo y pasar por el proceso estándar github de pull request descrito hasta que se sienta cómodo para pasar revisión. Si el ticket es trivial, o está arreglando la documentación, no es necesario firmar el *contributor agreement*.

Una vez te se allá familiarizado usted mismo con la comunidad y usted está entusiasmado para contribuir al núcleo:

* Firme y envié un correo con el contributor agreement ubicado en http://plone.org/foundation/contributors-agreement/agreement.pdf/at_download/file, entonces sea bien por correo postal a la dirección indicada o escanear y enviar por correo electrónico a assignments@plone.org. Esto ofrece protección de derechos de autor y se asegura de que la Fundación Plone que sea capaz de ejercer un cierto control sobre el código base, asegurándose de que no es apropiado para fines poco éticos de alguien. Para preguntas acerca de por qué el acuerdo está requerido, por favor ver :doc:`Contributor’s Agreement for Plone Explained <contributors_agreement_explained>`.

Si usted no esta seguro por dónde empezar o solo querer más dirección, siéntase libre de usar el canal IRC, las listas de correo, Twitter, etc... y pedir ayuda. Si bien no existe un proceso oficial de tutoría, hay un montón de personas dispuestas a actuar en ese rol y le guiará por los pasos de involucrarse en la comunidad. Una manera común de empezar las contribuciones es participar en un día de tune-up de Plone. Los Tune-ups está llenado con una buena mezcla de programadores recién iniciados y experimentados igualmente. Para más información, por favor ver http://plone.org/tuneup.

**¡Sea bienvenido a la comunidad Plone!**


Lidiar con los pull requests en GitHub
--------------------------------------

Antes de que podamos ``merge`` un ``pull request``, tenemos que comprobar que el autor ha firmado el acuerdo del contribuyente.

Si están listados en https://github.com/plone?tab=members, el autor ha firmado para que podamos seguir adelante y hacer un ``merge``.

Si no están en la lista, todavía hay una posibilidad de que han firmado el acuerdo del contribuyente.
Verifique eso en el canal IRC `#plone-framework <http://webchat.freenode.net?channels=plone-framework>`_.

Los ``pull requests`` sin el acuerdo del contribuyente sólo puede ser fusionadas en casos triviales, y sólo por el encargado de la liberación de Plone o *release manager*.
