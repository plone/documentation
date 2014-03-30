.. -*- coding: utf-8 -*-

Revisando PLIPs
===============

Expectativas
------------
Una buena revisión del PLIP toma aproximadamente 4 horas así que por favor haga planes en consecuencia. Cuando haya terminado, si usted tiene acceso al núcleo por favor comprometerse con la revisión de los plips y hacer referencia a la PLIP en el mensaje de confirmación. Si no tienes acceso, por favor adjuntar su revisión al ticket PLIP en si mismo.

Instalando el entorno
---------------------
Seguir las instrucciones en `definiendo un entorno de desarrollo <https://dev.plone.org/wiki/DevelopmentEnvironment>`_ para "obtener el código fuente". Usted necesitará a tener una copia al branch del repositorio del cual el PLIP fue asignado. En vez de correr el buildout con el archivo predeterminado buildout, usted lo ejecutara el archivo especifico de configuración del plip::

  > ./bin/buildout -c plips/plipXXXX.cfg

Revisión de funcionalidad
-------------------------
Hay varias cosas que podría ser dirigido en una revisión PLIP que depende de la naturaleza del PLIP. Esto es de ninguna manera una lista exhaustiva, pero un sitio para empezar. Las cosas para pensar aproximadamente cuándo este revisando:

General
-------
 * ¿Este PLIP realmente hace lo que los implementadores propusieron? ¿Hay variaciones incompletas? 
 * ¿Hubo allí algunos errores al ejecutar el buildout? ¿Hizo el trabajo de migración?
 * ¿No mensajes de error y los mensajes de estado tiene sentido? ¿Son correctas las internacionalizaciones?
 * ¿Hay alguna consideraciones de rendimiento? ¿El implementador de este PLIP se dirigió a ellos si es así?

Errores
-------
 * ¿Hay algún error? Nada es demasiado grande ni pequeño.
 * ¿Los campos a manejar data estrafalarias? ¿Cómo son las cadenas en los campos de fecha o los campos nulos son requeridos?
 * Es validación y cuestión de puro sentido? ¿Es demasiado restrictiva o no es lo suficiente restrictivo?

Incidentes de usabilidad
------------------------
 * ¿Es usable la implementación? 
 * ¿Cómo los usuarios finales novatos responden al cambio? 
 * ¿Hace este PLIP necesidad una revisión de usabilidad? Si usted piensa que este PLIP necesita una revisión de usabilidad, por favor, cambiar el estado a "please review" y agregue una nota a estos comentarios. 
 * ¿El PLIP es compatible con el resto de Plone? Por ejemplo, si hay configuración de panel del control, hacer esta forma nueva funciona en con el resto de los panel de control. 
 * ¿Todo se comporta bien para principiantes y usuarios avanzados? ¿Hay algún flujo de trabajo que se ofrece una experiencia extraña?
 * ¿Hay permisos nuevos y ellos trabajan correctamente? ¿Esas asignaciones de roles hacen con sentido?

Incidencias de la documentación
-------------------------------
 * ¿Hay suficiente documentación disponible correspondiente para el usuario final, ya sea programador o usuario plone?
 * ¿Este cambio en si mismo esta correctamente documentado?

Por favor, reporte fallos/incidencias en el sistema de ticket Trac como si se tratara de cualquier fallo Plone. Haga referencia al PLIP en el fallo, asigne a su implementador, y añadir una etiqueta para el PLIP en forma de plip-xxx. De este modo el implementor puede encontrar ayuda si lo necesita. Por favor, también priorizar el ticket. El PLIP no será fusionado hasta que todo los fallos bloqueadores y críticos están corregido.

Revisión de Código
------------------

Python
^^^^^^
 * ¿Es este código fuente mantenible?
 * ¿Esta el código fuente adecuadamente documentado?
 * ¿El código fuente se adhiere al estándar PEP8 (más o menos)?
 * ¿Están importando módulos obsoletos?

Javascript
^^^^^^^^^^
 * ¿El javascript conocer a nuestro conjunto de normas javascript? Ver http://developer.plone.org/templates_css_and_javascripts/javascript.html
 * ¿El Javascript funciona en todos los navegadores soportados actualmente? ¿Es eficaz? 

ME/TAL
^^^^^^
 * ¿La vista de usuario del PLIP adecuadamente y evitando demasiada lógica?
 * ¿Hay algún código fuente en un bucle que podría ser un problema de rendimiento?
 * ¿Hay alguna líneas de código con estilo obsoleto o viejo ME/TAL como el uso de DateTime?
 * ¿Es compatible con lo que dicta el estándar html? ¿Los ids y class CSS utilizado son apropiados?

Ejemplos de revisiones de PLIP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-davisagli.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip10886-review-cah190.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-rossp.txt
