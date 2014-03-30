.. -*- coding: utf-8 -*-

Implementando PLIPS
===================

Todo sobre los PLIPS
--------------------
**¿Qué es un PLIP?**
    Del ingles, PLIP significa PLone Improvement Proposal, el cual es una propuesta de mejora a Plone. Eso es cuando un cambio a un paquete Plone que afectaría todo el mundo Las PLIPs van por un proceso diferente que la corrección de fallos debido a su ancho logrando efecto. El equipo del framework Plone 4.x revisa todas las PLIPs para ser seguro que es en el mejor interés de la comunidad para ser implementada y que es de calidad alta.

**¿Es un PLIP o una corrección de fallo?**
    En general, cualquier cosa que cambia el API de Plone en el backend o la UI en la portada tendría que ser archivado como PLIP. En caso de duda, se presentará como una PLIP. El equipo del framework esta ansioso al reducir es propia carga de trabajo y clasificarla de nuevo por usted.

**¿Quiénes pueden presentar PLIPs?**
    Cualquiera quién ha firmado el Plone core contributor agreement puede trabajar en un PLIP. No deje que la redacción le asuste: la firma del acuerdo es fácil y usted tendrá acceso casi inmediato.
    Usted no tiene que ser el más increíble programador en el mundo entero para poder presentar una PLIP. El equipo del Framework estará encantado de ayudarle en cualquier momento del proceso. La presentación de un PLIP puede ser un gran proceso de aprendizaje y animamos a la gente de todos los orígenes a presentar.  Cuando el PLIP es aceptado, un miembro del equipo del Framework "defenderá" su PLIP y a ser encargado de llevar a cabo esta mejorar hasta que este completada.
    Las PLIPs no solamente son código fuente monkeys. Si usted tiene ideas sobre nuevas formas de interactuar o de la interfaz de usuario sus ideas son mas que bienvenidas. Incluso te ayudaremos a la par con los implementores si necesario.

**¿Qué es un defensor PLIP?**
    Cuando usted presenta su PLIP y esta es aprobada, Un miembro del equipo de Framework que este especialmente animado a ver hecho realidad el PLIP sera asignado a su PLIP como un defensor. Ellos están ahí para animar hasta su culminación, así que responde a cualquier pregunta y proporcionar orientación necesaria.

    Un defensor debería:

      * Responda a las preguntas formuladas por el implementador tiene sobre el PLIP, técnica y de cualquier otra
      * Fomentar el autor PLIP por su constantemente retroalimentación y estímulo
      * Cuidar que el implementador logre la lineas de tiempo y coloque las cosas listas a tiempo
      * Asistir en la búsqueda de ayuda adicional cuando sea necesario para completar la implementación en un tiempo oportuno

    Ten en mente que los defensores están en modo pasivo por defecto. Si usted necesitas ayuda o asesoría, por favor, contacte a ellos lo mas pronto sea posible para activar el modo ayuda.

**Yo aun estoy nervioso. ¿Puedo yo involucrarme de otras formas primero?**
    Si quieres sentir el proceso y cómo funciona, nos ayudan a revisar los PLIPs terminar las implementaciones. Si usted quiere sentir el proceso y cómo funciona, ayúdenos a revisar los PLIPs para terminar las implementaciones. Simplemente pregunte a los miembros del equipo de Framework cual PLIPs esta disponible para revisar o verificar el estatus del PLIPs en el `siguiente enlace <https://dev.plone.org/report/24>`_. Asegúrese de decirnos como usted intenta revisar el PLIP uniéndose a la `lista de correo del equipo de Framework <https://lists.plone.org/mailman/listinfo/plone-framework-team>`_ y enviar un correo rápidamente.
    Entonces, siga las simples instrucciones para :doc:`revisar un PLIP <plipreview>`. ¡Gracias de antemano!

**¿Cuándo yo puedo presentar un PLIP?**
    ¡Hoy, mañana, en cualquier momento! Después que la PLIP es aceptada, el equipo del Framework tratara de juzgar la complejidad y el tiempo para completar y asignar este en un hito. Usted puede iniciar rápidamente su trabajo, y nosotros animamos a presentarlo 'rápido y furioso'.

**¿Cuándo el PLIP es debido?**
    Resumen: Tan pronto usted lo finalice.
    Técnicamente, nosotros queremos ver eso completado para la publicación a la cual fue asignada. Nosotros sabemos que todos tenemos ocupaciones que nos ponen muy ocupados y además de nuevos problemas hacen a los PLIPs más complicado si es así entonces los vamos a mover hacia la siguiente versión.
    En general, nosotros no queremos seguir un PLIP por mas de un año. Si su PLIP es aceptada y nosotros no vemos actividad en mas de un año, nosotros probablemente le preguntaremos para iniciar de nuevo el proceso.

**No le gusta mi PLIP :( Y ahora que?**
    Solo por que un PLIP no ha sido aceptado en núcleo no significa que sea una mala idea. A menudo, es el caso que hay implementaciones compitiendo y nosotros queremos ver eso evaluado como un añadido antes de recibir la "bendición" la implementación preferida. 

Información general del proceso
-------------------------------
#. Presentar un PLIP (en cualquier tiempo)
#. PLIP es aprobada para incluirse dentro de núcleo para ser dado en una publicación
#. El desarrollador implementa el PLIP (código, tests, documentación)
#. PLIP es presentado para ser revisado por un desarrollador
#. El equipo del Framework revisa el plip y ofrece un comentario
#. El desarrollador direcciona lo concerniente en al comentario y presenta de nuevo si es necesario. Esto puede ir y venir varias veces hasta que tanto el FWT y el desarrollador está satisfecho con el resultado.
#. El PLIP es aprobada para fusionarse. En raras circunstancias, un PLIP sera rechazado. Esto es usualmente a que el resultado del trabajo hecho por el desarrollador no responde al comentario o abandono del proceso.  ¡Aguante ahí!
#. Después de que todos los otros PLIPS son fusionado, una publicación se corta. Esperar por los nuevos fallos!

.. _como_presentar_plip:

Como presentar a PLIP
---------------------
 Si usted necesita ayuda en algún punto de este proceso, por favor, contacte a un miembro del equipo del framework personalmente o pida ayuda en la `lista de correo FWT <https://lists.plone.org/mailman/listinfo/plone-framework-team>`_.

Un PLIP es un ticket con una plantilla especial. Para iniciar, `abra un nuevo ticket <https://dev.plone.org/newticket>`_ y seleccione "PLIP" como el tipo de ticket. Un nueva plantilla de ticket se cargara y usted debería planear llenarla en todas sus secciones y campos.

Cuando escribe una PLIP, de se lo mas especifico que pueda al punto a tratar. Recuerde su audiencia - que le puede dar apoyo a su propuesta, las personas tendrán que ser capaces de leerla! Un buen PLIP es suficientemente claro para un usuario conocedor de Plone este disponible a entender la propuesta de cambios, y suficientemente detallada para que el release manager y otros desarrolladores entiendan el completo impacto de la propuesta puede tener el código base. Usted no tiene que listar cada línea de código que necesidades de ser cambiadas, pero usted también debe dar una indicación que usted tenga sobre alguna idea de como el cambio puede ser viablemente implementado.

Si el cambio es menor entonces un ticket en el sistema de seguimiento debe ser suficiente, añadido como una mejora. El punto clave acá es que cada cambio necesita documentación para que otros usuarios puedan ver que cambios hay de nuevo. Esto puede ser en el formulario de un registro de en el sistema de incidencia, o un PLIP en el caso de que es un cambio mayor. Un fallo o cambio menor normalmente no necesita ir a través del proceso de revisión - que hace un PLIP.

Después que su plip es escrita, solicite un comentario de sus ideas en la lista de correo plone-developers. En este proceso de evaluación, usted quiere asegurarse de que el cambio no afectará negativamente a otras personas en un accidente. Otros pueden ser capaces de señalar puntos de riegos o incluso ofrecer una mejor o soluciones existentes. 

Cuándo este feliz con el comentario, :ref:`presente un PLIP <como_presentar_plip>`. Por favor, use la plantilla proveída (XXX: put the template here? Can we just have a custom ticket type?). Por favor, note un par de cosas. Es muy rara ves que la sección de “Risks” estará vacío o nula. Si usted busca esto es el caso y su PLIP no tiene más nada que un cambio trivial, quizás con algo más investigación debería estar listo. 

El campo seconder es REQUERIDO. Nosotros enviaremos el PLIP de regreso a usted si ese campo no es llenado. En la actualidad, sólo alguien más que piensa que su PLIP es una buena idea, un +1. En el futuro cercano, vamos a empezar a preguntar al secunde que es un socio de la codificación, o alguien que esté dispuesto y sea capaz de terminar el PLIP si algo le ocurriera al implementador.

Todo lo demás debe explicarse por sí mismo en el ticket de su PLIP. Si le dio pereza escribir estas PLIP tan documentado. Estoy apostando a este último.

Evaluando PLIPs
^^^^^^^^^^^^^^^
Después de presentar su PLIP, el equipo Framework tendrá un par de semanas para conocer y le harán de conocimiento si el PLIP es aceptado. Si el PLIP no es aceptado, por favor, se sienta mal! Nosotros animamos a que la mayoría de los PLIPs pasen a través del proceso de add on al principio, si es posible para asegurarse de que la mayoría de la comunidad lo use.

Toda la comunicación con usted ocurrirá en ticket PLIP ticket en si mismo por favor, este pendiente a su bandeja de entrada de su correo electrónico por cada cambios aplicado al ticket.

Estos son los criterios por del equipo framework que va a revisar en su revisión del paquete:
 * ¿Cual es el tamaño y estatus del trabajo necesitado para culminarlo? ¿Esta listo un add-on y esta bien establecido?
 * ¿Esta idea esta bien cocinada y se expresa con claridad?
 * ¿El trabajo propuesto en Plone deber estar ahora, en el futuro?
 * ¿Es esta PLIP más apropiado a ser calificado como un add-on?
 * ¿Es esta PLIP demasiado arriesgada?

Vea la pagina :doc:`plipreview` para más información.

Implementando su PLIP
----------------------
Usted puede iniciar el desarrollo en cualquier momento - pero si usted yendo a modificar el Plone en si mismo, usted podría querer esperar para ver si sus ideas son aprobadas primero para salvarse algún trabajo que no sea necesario. 

Reglas Generales
^^^^^^^^^^^^^^^^
 * Cualquiera de los nuevos paquetes debe estar en una branch bajo el namespace plone en github. Así usted no tenga el desarrollo allí, pero ese debe estar allí cuando este presentado. Nosotros recomendamos usar branches en el repositorio github.com/plone y se detallará abajo.
 * Lo mas importante, los revisores PLIP debe estar disponible a ejecutarse con buildout y cada cosa debería "solo trabajar" (tm).
 * Cualquier nuevo código fuente debería:
    * Estar :doc:`documentado apropiadamente <documentation>`
    * Tener el código fuente limpio
    * Usa los idiomas actuales de desarrollo
    * `Estar probado <http://collective-docs.plone.org/en/latest/testing_and_debugging/index.html>`_

Creando una nueva branch PLIP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. TODO: Esto necesita actualizar para las branches

Cree un archivo de configuración buildout para su PLIP en la carpeta llamada ``plips``.
Dar un nombre descriptivo, iniciando con el numero de plip; 
por ejemplo ``plip-1234-widget-frobbing.cfg``. Es archivo sera definido en el
branches/trunks que usted esta trabajando con su PLIP. Esto debería lucir algo 
así como lo siguiente:

En el archivo ``plips/plip-1234-widget-frobbing.cfg``::

 [buildout]
 extends = plipbase.cfg
 auto-checkout +=
     plone.somepackage
     plone.app.someotherpackage
 
 [sources]
 plone.somepackage = git git://github.com/plone/plone.somepackage.git branch=plip-1234-widget-frobbing
 plone.app.someotherpackage = git git://github.com/plone/plone.app.somepackage.git branch=plip-1234-widget-frobbing
 
 [instance]
 eggs +=
     plone.somepackage
     plone.app.someotherpackage
 zcml +=
     plone.somepackage
     plone.app.someotherpackage

Utilice la misma convención de nombre cuando haga un branch existente a paquetes existentes, y siempre usted 
debería siempre hacer branch paquetes cuando esta trabajando en las PLIPs.

Finalizando
^^^^^^^^^^^
Antes de hacer que su PLIP este listo para revisar, por favor añada un archivo dando un conjunto de instrucciones al revisor PLIP.

Este debería ser llamado ``plip_<number>_notes.txt``. Este debe incluir (pero no es limitado a solo eso):
 * Las direcciones URLs que apuntan a toda la documentación creada/actualizada
 * Cualquier inquietud, las incidencias aún permanecen
 * Cualquier cosas buildout extrañas
 * XXX: ¿Algo mas?

Una ves que allá finalizado, por favor, actualice su ticket indicar que esta listo para ser revisado. El equipo del Framework asignara 2 a 3 personas para revisar su PLIP. Ellos seguirán las lineas guías definidas en :doc:`plipreview`.

Después de que el PLIP ha sido aceptado por el equipo de framework y el release manager, se le pedirá que fusionar su trabajo dentro de la línea de desarrollo principal. La fusión de la PLIP no es la parte más difícil, pero hay que pensar en ello cuando se desarrolla. Usted tendrá que interactuar con un gran número de personas para conseguir que todo quede preparado. La fusión puede causar problemas con otros PLIPs que vienen en camino. Durante la fase de fusión debe estar preparado para ayudar con todas las características y fallos que puedan surgir.

Si todo ha ido según lo previsto en el próximo lanzamiento de Plone contendrá su PLIP en ella. Se espera contar con su ayuda para dar soporte a esa característica después de haber sido lanzado en Plone (dentro de lo razonable).
