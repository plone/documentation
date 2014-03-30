.. -*- coding: utf-8 -*-

Mr. Developer
=============

Esta configuración buildout usa mr.developer para administrar los paquetes de desarrollo. Ver 
http://pypi.python.org/pypi/mr.developer para mayor información o ejecutar 
el comando :command:`bin/develop help` para un lista de comando disponibles.

El mas común flujo de trabajo para obtener todas la ultimas actualizaciones es::

  > git pull
  > bin/develop rb

Esto te conseguirá la versión mas reciente de la configuración **coredev**, compruebe y actualice todos los paquetes vía Subversion en el directorio :file:`src` y ejecute buildout para configurar el asunto.

De vez en cuando puedes comprobar si alguna cosas pendiente::

  > bin/develop st

Si esto imprime alguna líneas con un signo de interrogación delante, usted puede limpiarlo con::

  > bin/develop purge

Esto sacará los paquetes del directorio :file:`src/` los cuáles ya no son necesarios, cuando estos han sido reemplazados por una apropiada liberación en formato Egg de estos paquetes.
