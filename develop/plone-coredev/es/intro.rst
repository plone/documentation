.. -*- coding: utf-8 -*-

Como presentar corrección de fallos al núcleo de Plone
======================================================
Este documento supone que usted quiere corregir un fallo y detallará el proceso completo para hacerlo. Para más información en la redacción de PLIPS, por favor :doc:`valla aquí <plips>`.

Política sobre soporte a la Versión
-----------------------------------
Si usted está tratando de corregir fallos, tenga en cuenta que Plone tiene una `política sobre soporte al versionamiento <https://plone.org/support/version-support-policy>`_.

Dependencias
------------
* `Git <http://help.github.com/mac-set-up-git/>`_
* `Subversion <http://subversion.apache.org/>`_
* `Python <http://python.org/>`_ 2.6 o 2.7 incluyendo sus librerías de encabezados, usadas para el desarrollo.
* Si usted esta usando un Mac OSX, necesitara instalar `XCode <https://developer.apple.com/xcode/>`_. Usted puede hacer este a través de la app store o muchos otros métodos en que lo venden. Usted probablemente querrá instalar su propio python 2.6 entonces necesita fuera todos los archivos encabezados de las librerías cuál hace compilar algunas extensiones. Usted puede ignorar este consejo para empezar, pero créame, que usted tendrá que instalarlas mas adelante. Ellos siempre hacen...
* `Python Imaging Library (PIL) <http://www.pythonware.com/products/pil/>`_. Debe asegurarse instalar esto dentro del entorno apropiado de python.
* `VirtualEnv <http://www.virtualenv.org/en/latest/index.html>`_ en el apropiado entorno python.
* `GCC <http://gcc.gnu.org/>`_ para compilar ZODB, Zope y lxml.
* `libxml2 y libxslt <http://xmlsoft.org/XSLT/downloads.html>`_, incluyendo sus librerías de encabezados para desarrollo.


Instalando su Entorno de Desarrollo
-----------------------------------
El primer paso en corregir un fallo está consiguiendo ejecutar este `buildout <https://github.com/plone/buildout.coredev>`_ correctamente. Le recomendamos corregir un fallo en la branch más reciente y entonces `backporting <http://en.wikipedia.org/wiki/Backporting>`_ tan como sea necesario. `Github <https://github.com/plone/buildout.coredev/>`_ por defecto siempre apunta a la branch actualmente activa. Más información sobre el cambio de las branches de liberación a continuación.

Para instalar un entorno de desarrollo plone 4.2 debe ejecutar los siguientes comandos::

  > cd ~/buildouts # o donde tu quieras colocar sus cosas
  > git clone -b 4.2  https://github.com/plone/buildout.coredev ./plone42devel
  > virtualenv --no-site-packages plone42devpy
  > cd plone42devel
  > ../plone42devpy/bin/python bootstrap.py # (donde "python" es el ejecutable de su interprete python 2.6 o 2.7).
  > bin/buildout -v

Si se encuentra con problemas en este proceso, consulte la documentación :doc:`issues`.

Esto se ejecutará durante mucho tiempo, si es su primera ejecución de buildout (~ 20 minutos) o tal ves mas todo dependerá de su conexión a Internet. Una vez que se hace ejecutado el buildout, usted puede iniciar su nueva instancia Zope con el siguiente comando::

  > ./bin/instance fg

El usuario y contraseña por defecto para una instancia Zope de desarrollo es **admin/admin**.

Cambiar Branches
^^^^^^^^^^^^^^^^
Si su fallo es especifico en una branch o usted piensa que debería hacer `backport <http://en.wikipedia.org/wiki/Backporting>`_, usted puede cambiar fácilmente las branches. La primera ves usted tiene que obtener una branch, entonces usted debe hacer eso con el siguiente comando::

  > git checkout -t origin/4.1

Esto debería crear una branch local de 4.1 con el seguimiento de la una en el servicio github. A partir de entonces sólo se puede hacer con el siguiente comando::

  > git checkout 4.1

Para ver en qué branch usted se encuentra actualmente, solo ejecute el siguiente comando::

  > git branch

La línea con un * por él indicará qué branch actualmente estás trabajando.

.. important::
   ¡Asegúrese de volver a ejecutar buildout si estuviera en una branch diferente antes para obtener las versiones correctas de los paquetes, de lo contrario obtendrá un comportamiento extraño!

Para mas información sobre buildout, por favor ver la documentación sobre `buildout en el manual de desarrollador collective <http://developer.plone.org/reference_manuals/old/buildout/index.html>`_.


Comprobando paquetes para corregir
----------------------------------
La mayoría de paquetes no están por defecto en el directorio :file:`src/`, así que usted puede usar ``mr.developer`` para conseguir la versión mas reciente y asegurarse que usted siempre tiene la versión mas actualizada. Puede ser un poco intimidado al principio para averiguar qué paquetes están causando el fallo en cuestión, pero sólo pregunte en el IRC si necesitas algo de ayuda. Una vez que [usted cree] que sabe cuál(es) paquete(s) usted que desea, nosotros tenemos que obtener de la fuente del mismo.

Usted puede conseguir el código fuente del paquete con ``mr.developer`` o con el comando ``checkout``, o puedes ir directamente a editar :file:`checkouts.cfg`. Nosotros recomendamos el último pero describirá ambos. Al final, el archivo :file:`checkouts.cfg` tiene que ser configurado de cualquier manera así que también podrás empezar allí.

En el directorio raíz de su su buildout, abra el archivo :file:`checkouts.cfg` y añada su paquete si no es ya allí de la siguiente forma::

  auto-checkout =
          # mi paquetes modificados
          plone.app.caching
          plone.caching
          # otros paquetes
          ...

Entonces ejecutar de nuevo buildout para conseguir los códigos fuentes de los paquetes desde sus repositorios, con el siguiente comando::

  > ./bin/buildout

Alternativamente, nosotros podemos administrar los checkouts desde la línea de comando, usando el comando de mr.developer :command:`bin/develop` para conseguir la fuente de paquetes más reciente. Por ejemplo, si la incidencia esta en los paquetes ``plone.app.caching`` y ``plone.caching`` lo ejecuta con los siguientes comandos::

  > ./bin/develop co plone.app.caching
  > ./bin/develop co plone.caching
  > ./bin/buildout

¡No olvide volver a ejecutar buildout! En ambos métodos, ``mr.developer`` descargará el código fuente desde github (o de donde se definió) y colocara el paquete en el directorio :file:`src/`. Usted puede repetir este proceso con tantos paquetes cuando lo necesite. Para algunos más consejos en la forma de trabajo con ``mr.developer``, por favor :doc:`lea mas aquí <mrdeveloper>`.

Probando localmente
-------------------
En un mundo ideal, usted debería escribir un caso de prueba para su incidencia antes de tratar de corregir el fallo. En realidad esto rara ves sucede. No importa la forma cómo usted te acercas a resolver la falla, usted tiene que SIEMPRE probar la ejecución de los casos de prueba para ambos el módulo y plone.org antes de que usted genere una revisión con cualquiera de cambios.

¡Si usted no comienza con un caso de prueba, se ahorrará problemas potenciales y valida el fallo antes de llegar demasiado profundo en la incidencia!

Para correr una prueba para el módulo específico ejecute el siguiente comando::

  > ./bin/test -m plone.app.caching

Estos deberían ejecutarse todo sin fallos. ¡Por favor, no verifique nada adicional! Si usted no ha escrito su caso de prueba aun, este es un buen momento para escribir un caso de prueba para la falla que usted está reparando y asegúrese de que todo está funcionando como debería.

Después que las pruebas al nivel del módulo se ejecutan con su cambio realizado, por favor asegúrese de que los otros módulos no se ven afectados por el cambio realizado por usted, para esto ejecute todas las pruebas con el siguiente comando::

  > ./bin/alltests

.. note::

    Las pruebas toman un tiempo en ejecutarse. Una ves se allá convertido en el maestro de corrección de fallas, usted tal ves solo le deje hacer esto al servicio de ``jenkins`` hacer esta tarea por usted. Más sobre esto a continuación.

Actualizar el archivo CHANGES.rst y checkouts.cfg
-------------------------------------------------
Una ves todo las pruebas se ejecuten localmente en su maquina, usted debe estar **CASI** listo para generar una revisión de sus cambios. Un par de cosas hay que hacer antes de continuar.

Lo primero, por favor, edite el archivo :file:`CHANGES.rst` (o :file:`CHANGES.txt`, o :file:`HISTORY.txt`) en cada archivo que usted modifico y agregue un resumen de sus cambios. En esta nota el cambio será cotejada para la próxima versión Plone y es importante para los integradores y desarrolladores puedan ser capaz de ver lo que obtendrán si se actualizan.
Nuevas entradas al changelog debería ser agregadas en la partes superiores del archivo :file:`CHANGES.txt`.

*Lo más importante*, si no lo hizo antes, edite el archivo :file:`checkouts.cfg` en el directorio de buildout y agregar el paquete al cual le hizo sus cambios a la lista de ``auto-checkout``. Esto le permite al release manager de Plone saber que paquete ha sido actualizado para que cuando se de la próxima versión de Plone, este tendrá que fijar a la próxima versión del paquete al momento de generar un nuevo paquete Egg. LEER: esto es como su corrección viene en un paquete egg!

Tenga en cuenta que hay una separador de sección llamada ``# Test Fixes Only``. Asegúrese que su paquete egg este por encima de esa línea o su paquete egg probablemente no se hizo muy rápidamente. Esto le dice al release manager que los paquetes Egg por debajo de esta línea tienen pruebas que están actualizadas, pero no hay cambios en el código.

Modifique el archivo :file:`checkouts.cfg` también ejecute el comando buildbot, entonces el `servicio jenkins <https://jenkins.plone.org/>`_, actualizara el paquete egg y ejecutara todas las pruebas contra las pruebas que usted realizo. No sea que usted alguna vez volvería a sáltate ejecutar todas las pruebas, por supuesto... Más sobre esto a continuación.

Si su fallo esta en mas de una publicación (ej. 4.1 y 4.2), por favor, aplicar sus cambios en ambas branches y añadir al archivo :file:`checkouts.cfg`.

Generando una revisión y haciendo Pull Requests
-----------------------------------------------
¡Uf! Estamos en la recta final. Verifique su lista de actividades hechas en los últimos minutos:

 * ¿Usted corrigió el fallo original?
 * ¿Su código es consistente con nuestra :doc:`style`?
 * ¿Usted removió lineas extras de código y PDB persistentes?
 * ¿Usted escribió un caso de prueba para su fallo?
 * ¿Todos sus casos de prueba para los módulos y para Plone se ejecutan sin ningún problema?
 * ¿Usted actualizo el archivo :file:`CHANGES.rst` en cada paquete que usted modifico?
 * ¿Usted añadió sus paquetes cambiados al archivo :file:`checkouts.cfg`?

Si usted respondió *SI* a todas estas preguntas, ¡usted esta listo para presentar sus cambios! Un par de recordatorios rápidos:

 * Solamente generar una revisión directamente a la branch de desarrollo, si usted esta seguro que su código no causa ninguna falla y los cambios son pequeños y triviales. De lo contrario, por favor, haga un ``fork`` del repositorio aplicando sus revisiones allí y luego haga un ``pull request`` (mas abajo se explica como).
 * Por favor, trate de hacer un cambio por cada revisión. Si usted esta corrigiendo tres fallas, haga tres revisiones. De esta forma, es fácil ver que fue cambiado y donde se realizo el cambio, además es mas fácil hacer un ``roll back`` de cualquier cambio si es necesario. Si usted quiere hacer muchos cambios como limpiar espacios en blanco o renombrar variables, es especialmente importante hacer una revisión separada por esta razón.
 * Nosotros tenemos un grupo de guardianes que siguen los cambios y cada revisión aplicada para ver que ha sucedido de nuevo en el código fuente de nuestro favorito CMS! Si su revisión tiene algo REALMENTE no está bien, ellos le contactaran políticamente a usted, lo mas común que suceda es que inmediatamente revierten los cambios aplicados con sus revisiones. Hay personas no oficiales asignadas a esto si usted esta especialmente nervioso, entre en el canal IRC `#plone <http://webchat.freenode.net?channels=plone>`_ en freenode.net y pregunte por alguien que pueda ver sus cambios.

Generando revisiones al paquete Products.CMFPlone
-------------------------------------------------
Si usted esta trabajando un corregir un fallo en el paquete ``Products.CMFPlone``,
hay un par de otras cosas que debe tomar en cuenta.
Primero y mas importante,
puede ver que este paquete tiene varias branches.
Al momento de escribir este documento,
habían tres branches para ``4.1``, ``4.2``, y la ``master``, el cual es implícitamente 4.3.

¿Aun me sigue con la explicación? Entonces, usted tiene un corrección de fallas para 4.x.
Si la corrección es solamente para una versión,
asegúrese de obtener la branch y aplicar sus cambios allí.
Sin embargo, si la corrección del fallo es en múltiples branches.

Por ejemplo, el fallo inicia en la versión 4.1. Obtenga la branch 4.1 y aplicar sus cambios allí con varias revisiones por cada cambio con sus respectivas pruebas.

Si su corrección involucra una simple revisión de cambios,
usted puede usar el comando ``git cherry-pick`` para aplicar la misma revisión
a un branch diferente.

Primero cambie a la branch, con el siguiente comando::

  > git checkout 4.2

Y entonces con el comando ``git cherry-pick`` y el número de revisión del commit (usted puede obtener el número SHA hash desde el ``git log``), con el siguiente comando::

  > git cherry-pick b6ff4309

Tal ves allá conflictos; entonces, resuélvalos y seguir las instrucciones
que la herramienta git le da a usted para completar el comando ``git cherry-pick``.

Si su corrección involucra múltiples revisiones, entonces hacer un ``cherry-picking`` uno a uno puede resultar tedioso.
En este caso, las cosas son más fáciles, si usted hizo su corrección en una branch con una característica separada.

En ese escenario, primero fusione la branch característica a la branch 4.1, con los siguientes comandos::

  > git checkout 4.1
  > git merge my-awesome-feature

A continuación, regrese a la branch característica y haga una branch para `establecerlo` dentro de la branch 4.2, con los siguientes comandos::

  > git checkout my-awesome-feature
  > git checkout -b my-awesome-feature-4.2
  > git rebase ef978a --onto 4.2

(ef978a viene a ser la ultima revisión en el histórico de la branch característica antes
de que sea bifurcaba de la versión 4.1. Usted puede mirar el histórico de su repositorio git con el comando ``git log`` para encontrar este.)

Al llegar a este punto, la historia de la branch característica ha sido actualizada, pero no ha sido de hecho
fusionada con la versión 4.2 aún. Este le permite a usted resolver conflictos antes de que usted
lo fusione a la branch release 4.2. Hacerlo ahora así con los siguientes comandos::

  > git checkout 4.2
  > git merge my-awesome-feature-4.2


Generando revisiones al paquete Products.CMFPlone
-------------------------------------------------
Si usted esta trabajando un corregir un fallo en el paquete ``Products.CMFPlone``,
hay un par de otras cosas que debe tomar en cuenta.
Primero y mas importante,
puede ver que este paquete tiene varias branches.
Al momento de escribir este documento,
habían tres branches para ``4.1``, ``4.2``, y la ``master``, el cual es implícitamente 4.3.

¿Aun me sigue con la explicación? Entonces, usted tiene un corrección de fallas para 4.x.
Si la corrección es solamente para una versión,
asegúrese de obtener la branch y aplicar sus cambios allí.
Sin embargo, si la corrección del fallo es en múltiples branches.

Por ejemplo, el fallo inicia en la versión 4.1. Obtenga la branch 4.1 y aplicar sus cambios allí con varias revisiones por cada cambio con sus respectivas pruebas.

Si su corrección involucra una simple revisión de cambios,
usted puede usar el comando ``git cherry-pick`` para aplicar la misma revisión
a un branch diferente.

Primero cambie a la branch, con el siguiente comando::

  > git checkout 4.2

Y entonces con el comando ``git cherry-pick`` y el número de revisión (usted puede obtener el número SHA hash desde el ``git log``), con el siguiente comando::

  > git cherry-pick b6ff4309

Tal ves allá conflictos; entonces, resuélvalos y seguir las instrucciones
que la herramienta git le da a usted para completar el comando ``git cherry-pick``.

Si su corrección involucra múltiples revisiones, entonces hacer un ``cherry-picking`` uno a uno puede resultar tedioso.
En este caso, las cosas son más fáciles, si usted hizo su corrección en una branch con una característica separada.

En ese escenario, primero fusione la branch característica a la branch 4.1, con los siguientes comandos::

  > git checkout 4.1
  > git merge my-awesome-feature

A continuación, regrese a la branch característica y haga una branch para `establecerlo` dentro de la branch 4.2, con los siguientes comandos::

  > git checkout my-awesome-feature
  > git checkout -b my-awesome-feature-4.2
  > git rebase ef978a --onto 4.2

(ef978a viene a ser la ultima revisión en el histórico de la branch característica antes
de que sea bifurcaba de la versión 4.1. Usted puede mirar el histórico de su repositorio git con el comando ``git log`` para encontrar este.)

Al llegar a este punto, la historia de la branch característica ha sido actualizada, pero no ha sido de hecho
fusionada con la versión 4.2 aún. Este le permite a usted resolver conflictos antes de que usted
lo fusione a la branch release 4.2. Hacerlo ahora así con los siguientes comandos::

  > git checkout 4.2
  > git merge my-awesome-feature-4.2


Los branches y los forks y hacer revisiones directamente - ¡Por Dios!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Plone uso un repositorio svn, así que todo el mundo es familiar y acostumbrado a hacer revisiones directamente a las branches. Después de la migración de los repositorios svn a los repositorios git en el servicio github, la comunidad decidió mantener este espíritu. Si usted ha firmado el documento :doc:`contributor agreement <contributors_agreement_explained>`, usted puede hacer commit directamente a la branch (para plone esto sería la versión del branch, para más otros paquetes esto sería el branch llamado ``master``).

AUN ASÍ, hay unas cuantas situaciones donde una hacer un nuevo branch es apropiado. Si usted:
 * usted se esta iniciando,
 * usted no esta seguro acerca de sus cambios
 * quiere una revisión de comentario/código
 * están llevando a cabo un cambio no trivial

Entonces probablemente quieres crear una branch de cualquier paquete que está usando y entonces use la característica de `pull request <https://help.github.com/articles/using-pull-requests>`_ del servicio github para obtener revisión. Todo acerca de este proceso sería el mismo, excepto que necesita para trabajar en una branch. Tome de ejemplo el paquete ``plone.app.caching``. Después de comprobarlo con ``mr.developer``, cree su propia branch con los siguientes comandos::

  > cd src/plone.app.caching
  > git checkout -b my_descriptive_branch_name

.. note::

    Hacer un branch o fork es su elección. Yo prefiero hacer branch, y yo estoy escribiendo la documentación en esto usando el método de branch. Si usted hace un branch, nos ayuda porque nosotros *sabemos* que tienes permisos para aplicar revisiones a este branch. De cualquier forma, es tu decisión.

Proceda como le sea costumbre. Cuándo usted este a punto para hacer ``push`` de la corrección de su fallo, debe hacer un push a una branch remota con el siguiente comando::

  > git push origin my_descriptive_branch_name

Esto hará un branch remoto en el servicio github. Vaya a esta branch de la interfaz de usuario github y en la parte superior derecha habrá un botón que dice **"Pull Request"**. Este le permitirá hacer una solicitud dentro de un pull request en la branch principal. Hay personas que se ven una vez a la semana o más para revisar las solicitudes pull requests y confirmar si son o no es una buena corrección y le dará una retroalimentación cuando sea necesario. Los revisores son informales y muy agradables, así que no se preocupe - ¡que están ahí para ayudar! Si usted quieres retroalimentación inmediata, valla a la sala IRC con el enlace de ``pull request`` y pedida una revisión.

.. note::

    ¡todavía necesitas actualizar el archivo :file:`checkouts.cfg` en las branches correctas de proyecto buildout.coredev!

Jenkins
-------
¡Usted TODAVÍA no está listo! Por favor, compruebe que el servicio jenkins se asegure que sus cambios no hallan roto cosas. Se ejecuta cada media hora y tarda un rato para ejecutar la comprobación en una hora es bueno para verificar el resultado que arroje. Ten una cerveza y tu mirada sobre el `panel de control Jenkins <https://jenkins.plone.org/>`_.

Finalizando Tickets
-------------------
Si usted esta trabajando de un ticket asignado, por favor no olvide en volver a actualizar el ticket y agregar un enlace a sus revisión de cambios. Actualmente no tenemos una integración de nuestro sistema de ticket con el servicio github pero es una forma agradable de seguir sus cambios. Eso también le permite al reportero saber que usted preocupa. Si el fallo es realmente grave, considere en contactar al release manager y he invitarle a hacer un pronto lanzamiento.

FAQ
---
 * *¿Cómo puedo saber si se tomaron mis cambios de mi paquete?*
    Usted puede seguir el proyecto en github y mirar la `linea del tiempo de cambios <https://github.com/organizations/plone>`_. Usted también puede descargar el :file:`CHANGES.txt` de cada liberación de Plone para ver una lista comprensible de todos los cambios y validar que su contribuciones estén presente.

