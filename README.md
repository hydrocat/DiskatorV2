# DiskatorV2
APS de banco de dados 2

Como Usar
=========

python3 main.py
***Note que a versão deve ser >= 3***

Quando aparecer o menu, entre com a opção correspondente:
1 - Sair
2 - Criar Arquivo
...

Nas opções de
    *Criar
    *Inserir
    *Deletar
O nome do arquivo precisa incluir a extenção

Na opção de __Listar__ apenas o nome da tabela é nescessário

Explicação
==========
Existem as seguintes classes/arquivos:
	*main.py
	*funcoes.py
	*menu.py
	*parser.py
e as funcionalidades são coordenadas por __main.py__

Funções.py
==========
	Contém uma classe que abstrai arquivos binarios e as funcionalidades nescessárias para a implentação do projeto. A saber:
       __init__(nome) é o construtor e recebe o nome do arquivo
       createArquivo(dados) escreve um arquivo binario segundo os meta-dados que é do tipo comandoSQL.
       inserirRegistro(reg) insere registros no arquivo (reg também é do tipo comandoSQL)
       deleteRegistro(dado) segue o padrão dos anteriores
       listarRegistro() imprime os dados contido no arquivo

Parser.py
=========
	Este arquivo tem um único método chamado "parse" que recebe um nome como parâmetro e retorna um objeto do tipo comandoSQL.

comandoSQL.py
=============
	Contem a definição de comandoSQL, que generaliza os comandos sql.Veja a hierarqia da classe:
	*ComandoSQL
		*nomeTabela
		*comando
		*dados
	Em que o atributo comando é "insert", "delete" ou "create"
	dados apresenta uma configuração diferente para cada tipo de comando:
	Caso insert:
	     dados= [
			[ <Nome Coluna>, <Valor> ]
		    	...
		 ]
	Caso delete:
	     dados = [
			[ <Nome Coluna>, <Valor>, <Comparador> ]
			...
		]
			 