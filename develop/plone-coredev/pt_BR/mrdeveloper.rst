Mr. Developer
=============

Esse buildout usa o mr.developer para gerenciar o desenvolvimento do pacote. Veja
http://pypi.python.org/pypi/mr.developer para maiores informações ou execute
'bin/develop help' para obter uma lista de comandos disponíveis.

A forma mais comum de obter as últimas atualizações é:

  $ git pull
  $ bin/develop rb

Isto lhe trará a versão mais recente da configuração do coredev, faça o checkout, atualize todos os pacotes do Subversion na pasta src e execute buildout para configurar tudo.

De vez em quando você pode verificar se existem modificações não comitadas nos repositórios baixados pelo mr.developer:

  $ bin/develop st

Se alguma linha for impressa com um ponto de interrogação na frente, você pode limpar a lista com o seguinte comando:

  $ bin/develop purge

Isso irá remover os pacotes desnecessários de src/, já que foram substituídos por versões de eggs mais adequadas.
