.. -*- coding: utf-8 -*-

Troubleshooting: solucionar problemas
=====================================

Incidencias Buildout
--------------------

Buildout puede ser muy frustrante para aquellos no familiarizados con el análisis a través del lenguaje robot autista. ¡No tema! Estos errores son casi siempre tienen una solución rápida y un con poco de comprensión le lleva a un largo camino. 

Errores ejecutando bootstrap.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Ni siquiera se puede llegar a correr buildout y entonces ya tendrá un error. Déjeme darle un ejemplo de esto::

    ...
     File "/usr/local/lib/python2.6/site-packages/distribute-0.6.13-py2.6.egg/pkg_resources.py", line 556, in resolve
        raise VersionConflict(dist,req) # XXX put more info here  
     pkg_resources.VersionConflict: (zc.buildout 1.5.1 (/usr/local/lib/python2.6/site-packages/zc.buildout-1.5.1-py2.6.egg), Requirement.parse('zc.buildout==1.5.2'))


Usted puede pensar que la diosa buildout está enfadada porque han pasado MESES desde que usted hizo un sacrificio humano para ella, pero sea fuerte y siga adelante. Buildout simplemente se ha dado cuenta de que la versión de buildout requerida por el archivo bootstrap.py que usted está intentando ejecutar no coincide con la versión de buildout en la biblioteca de python. En el error anterior, el sistema dispone de buildout 1.5.1 instalado y el archivo bootstrap.py quiere correr con 1.5.2.

Para solucionarlo, hay un par de opciones. En primer lugar, puede hacer que se ejecute buildout con la versión que ya se han instalado mediante la invocación de la etiqueta de versión. Esto le dice a su archivo bootstrap.py [Plone] para ejecutar muy bien con la versión que ya se ha instalado. En el caso de que el error pegado encima, que sería::

   > python bootstrap.py --version=1.5.1

Yo conozco personalmente que las versiones 1.4.4, 1.5.1, 1.5.2 y todo funciona de esta manera.

La otra opción es eliminar el paquete egg actual y forzar la actualización. En el caso de que el error anterior, todo lo que necesita para eliminar del paquete egg que tiene actualmente en ell sistema. ej::

  > rm -rf /usr/local/lib/python2.6/site-packages/zc.buildout-1.5.1-py2.6.egg

Al volver a ejecutar el archivo bootstrap.py, este buscará para el paquete egg para el buildout, ya que no hay uno, y luego ir a buscar el paquete egg con la nueva versión que se quiere para su construcción buildout.

De una de esas, digamos dos Ave Marías, con tres padres nuestros y ejecute de nuevo bootstrap.py. ¡Tada!

Otra cosa de la nota es que está ejecutando bootstrap efectivamente asocia al ejecutable python y todas sus bibliotecas a su buildout. Si tiene varias instalaciones Python y quiere cambiar a cual Python está asociando a su buildout, sólo tiene que volver a ejecutar bootstrap.py con el nuevo python (y vuelva a ejecutar el buildout). Usted puede obtener el mismo error anterior nuevamente, ahora que sabes cómo solucionarlo, usted puede pasar ese tiempo bebiendo cerveza en vez de aplastar el teclado. 

¡Hurra!

Cuando Mr. Developer no es feliz
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``mr.developer`` nunca es feliz, excepto cuando es. A pesar de que esto técnicamente no es un incidente buildout, pasa cuándo esta ejecutando buildout, entonces yo lo estoy poniéndolo en las incidencias buildout.

Cuándo trabajando con la instancia de desarrollo, especialmente con toda el movimiento de ida y vuelta de cambios entre github y svn, usted puedes tener una copia vieja de un paquete en le directorio ``src``. El error luce así::
 
    mr.developer: Can't update package 'Products.CMFPlone' because its URL doesn't match.


Mientras usted no tenga cualquier revisión de cambios pendiente, usted solo necesita remover el paquete del directorio ``src/`` y se vuelve a revisar para usted cuando se actualiza. 


Usted también se puede conseguir con errores tan divertidos tales como::

    Link to http://sphinx.pocoo.org/ ***BLOCKED*** by --allow-hosts


Estos errores están bien para ser ignorados SI y SÓLO SI las líneas que siguen diga::

    Getting distribution for 'Sphinx==1.0.7'.
    Got Sphinx 1.0.7.


Si buildout termina con un aviso de que algunos paquetes no se pudo descargar, entonces es probable que el paquete no se ha descargado. Esto es malo y puede causar todo tipo de errores al iniciar o tratar de hacer las cosas porque nunca se llegan a descargar el paquete.

Hay dos maneras de obtener este error desaparezca. Lo primero es eliminar todas las instancias del host filtrado. registrar minuciosamente todos los archivos y elimine cualquier lineas la cual diga así ``allow-hosts =`` y ``allow-hosts +=``. En teoría, mediante la restricción de los hosts del cual se va a descarga, buildout irá más rápido. Ya sea que realmente sucede o no, yo no puedo opinar. El punto es que son de seguramente se pueden eliminar.

La segunda opción es el permitir al host al cual ese apunta para ser añadido de algo como esto a su archivo .cfg::

    allow-hosts += sphinx.pocoo.org

Otra vez, esto es sólo necesario si el paquete no fue encontrado al final. 

¡Hurra!

Errores de ruta mr.developer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``ERROR: You are not in a path which has mr.developer installed (:file:`.mr.developer.cfg` not found).``

Cuando ejecuta algún comando :command:`./bin/develop`.

Para solucionar, simplemente ejecute el siguiente comando::

  ln -s plips/.mr.developer.cfg



Otros incidentes aleatorios
---------------------------
.. TODO: Esto necesita ser revalidada

Paquetes Sucios
^^^^^^^^^^^^^^^

"ERROR: Can't update package '[Some package]', because it's dirty."

Solución
~~~~~~~~
``mr.developer`` se queja porque un archivo se ha cambiado / añadido, pero no
se ha generado una revisión.

Utilice el comando :command:`bin/develop update --force`. Añadiendo ``*.pyc *~.nib *.egg-info
.installed.cfg *.pt.py *.cpt.py *.zpt.py *.html.py *.egg`` a su configuración subversion
global-ignores ha sido sugerido como una solución más permanente.


No module named zope 2
^^^^^^^^^^^^^^^^^^^^^^
``ImportError: No module named Zope2" when building using a PLIP cfg file.``

Parece no ser en realidad el caso. Eliminar el archivo :file:`mkzopeinstance.py` desde el directorio :file:`bin/` y
ejecute de nuevo el script buildout para corregir esto si usted está encontrando fastidioso.

No puede abrir el archivo '/Startup/run.py'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Dos posibles soluciones, usted esta usando Python 2.4 por equivocación, así que por favor use Python 2.6 en cambio. O, usted tal ves necesitar asegurarse que usted ejecuto el script :command:`bin/buildout …` después ejecutar el script :command:`bin/develop …`. Trate de remover los directorios :file:`parts/*`, :file:`bin/*`, el archivo :file:`.installed.cfg`, entonces ejecute de nuevo el archivo :file:`bootstrap.py` y ejecute de nuevo buildout, develop, buildout.

PIL perdido
^^^^^^^^^^^
El archivo :file:`pil.cfg` es incluido con esta configuración buildout para ayudar en instalación PIL. Ejecutar
:command:`bin/buildout -c pil.cfg` a instalar la librería PIL. Este método no funciona en Windows, así que
nosotros somos incapaces de correr él por defecto.


Incidencias con paquetes egg modificado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
El comando :command:`bin/develop status` el mostrara que el paquete egg ``Products.CMFActionIcons`` ha sido
modificado, pero no lo he tocado.  Y ejecutando este comando :command:`bin/develop up` esta previniendo 
la actualización de todos los paquetes egg.

Solución
~~~~~~~~

Editar el archivo :file:`~/.subversion/config` y añadir eggtest*.egg a la lista de ``global-ignores``

