Revisando PLIP's
================

Expectativas
------------
Uma boa revisão de PLIP leva aproximadamente 4 horas, então se programe corretamente. Quando terminar, se tiver acesso ao núcleo, comite a revisão no diretório de PLIP's e referencie a PLIP na mensagem do seu commit. Se não tiver acesso, anexe sua revisão ao ticket aberto da PLIP.

Configurando o ambiente
-----------------------
Siga as instruções em [wiki:DevelopmentEnvironment setting up a development environment], "Obtendo o Código". Você deverá fazer o checkout do branch ao qual a PLIP está vinculada. Ao invés de rodar o buildout usando o arquivo de buildout padrão, você deverá rodar a configuração específica para a PLIP::

  > ./bin/buildout -c plips/plipXXXX.cfg

Revisão de funcionalidade
-------------------------
Existem várias coisas que podem ser abordadas em uma revisão de PLIP, dependendo da sua natureza. A lista abaixo não é, absolutamente, uma lista completa, mas um ponto de partida sobre o que pode ser observado em uma revisão:

Geral
-----
 * A PLIP realmente faz o que os implementadores propuseram? Existem variações incompletas?
 * Ocorreram erros durante a execução do buildout? As migrações funcionaram?
 * Os erros e mensagens de status fazem sentido? Estão internacionalizados corretamente?
 * Existem considerações sobre a performance? O implementador as observou?

Erros
-----
 * Existem erros? Nada é muito grande ou muito pequeno.
 * Os campos manipulam dados estranhos? E situações como strings em campos de data ou campos obrigatórios deixados em branco?
 * A validação não está pouco exigente nem exigente demais?

Qestões de usabilidade
----------------------
 * A implementação está usável?
 * Como usuários finais iniciantes reagirão à mudança?
 * A PLIP necessita de uma revisão de usabilidade? Se você considerar que sim, altere o estado para "please review" e adicione uma nota nos comentários.
 * A PLIP está consistente com o resto do Plone? Por exemplo, se existe uma configuração no painel de controle, o novo formulário se adequa aos outros painéis?
 * Tudo está fluindo bem para usuários iniciantes e avançados? Existem fluxos que parecem estranhos?
 * Existem permissões novas e elas funcionam apropriadamente? A atribuição de papéis (roles) faz sentido?

Questões de documentação
------------------------
 * A documentação correspondente é suficiente para usuários finais, seja ele desenvolvedor ou usuário Plone?
 * A mudança está bem documentada?

Reporte erros/solicitações no Trac, como faria com qualquer outro erro do Plone. Referencie a PLIP no erro, atribua a seu desenvolvedor e adicione uma tag para a PLIP como plip-xxx, pois fica mais fácil do desenvolvedor encontrar, se precisar. Também coloque prioridade no ticket. A PLIP não será mesclada até que os erros sejam corrigidos.

Revisão de Código
-----------------

Python
^^^^^^
 * O código é possível de manter?
 * O código está documentado corretamente?
 * O código segue os padrões da PEP8? Quanto?
 * Está importando módulos obsoletos?

Javascript
^^^^^^^^^^
 * O javascript segue os padrões utilizados? Veja a referência em http://plone.org/documentation/manual/developer-manual/client-side-functionality-javascript/javascript-standards/referencemanual-all-pages
 * O javascript funciona em todas os navegadores suportados atualmente? Como está o desempenho?

ME/TAL
^^^^^^
 * A PLIP usa views apropriadas e evita implementar muita lógica?
 * Existe algum loop no código que pode ter, potencialmente, problema de desempenho?
 * Existem linhas de código obsoletas ou no estilo antigo, como DateTime?
 * O HTML renderizado é compatível com as normas? Os ids e classes são usadas apropriadamente?

Exemplos de revisões de PLIP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-davisagli.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip10886-review-cah190.txt
 * https://svn.plone.org/svn/plone/buildouts/plone-coredev/branches/4.1/plips/plip9352-review-rossp.txt
