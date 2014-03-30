.. -*- coding: utf-8 -*-

Cómo actualizar estas documentaciones
=====================================

Estos documentos actualmente son almacenados con el directorio :file:`/docs`. Para actualizarles, por favor, hacer un checkout desde el buildout coredev y actualizar allá. Hacer los cambios en la rama de versión más reciente (como de esta ``4.4``)::

  > git clone git@github.com:plone/buildout.coredev.git
  > cd buildout.coredev
  > git checkout 4.4

Para probar sus cambios localmente, inicie de nuevo el buildout y entonces::

  > bin/sphinx-build docs docs/build

Sphinx colocara en un directorio que usted puede consultar en tu navegador web para validar. Por ejemplo: ``file:///home/user/buildout.coredev/docs/build/index.html``

Por favor asegúrese en validar todos los avisos y los errores antes de generar una revisión para estar seguro que los documentos queden válido. Una vez todo está a listo para ir, haga commit y push de sus cambios.

El comando ``git cherry-pick`` hace commits en la rama más reciente a la rama actualmente liberada (como de esta escritura ``4.3``) si estos cambios aplican a aquella versión (usted puede conseguir el SHA hash de registro :command:`git log`)::

  > git checkout 4.3
  > git cherry-pick b6ff4309

Tal ves allá conflictos; entonces, resuélvalos y seguir las instrucciones 
que la herramienta git le da a usted para completar el comando :command:`git cherry-pick`.
