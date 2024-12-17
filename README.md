API de controle de caixa - Norte Auto Peças

- Objetivo: Criar uma API para monitorar o controle, recebimento, e saida dos caixas das lojas. Tendo assim um controle e acesso melhor para a diretoria, e para quem realiza as conferencias.

- Estrutura: Irei criar uma API, e o Front-end.
	Terminar apos a finalização da ideia.

- Linguagem utilizada: Python - framework (Flask) no back-end;

- Banco de dados que sera usado é o Oracle - PL SQL
	ip - 
	porta - 
	type - 

- Criar uma tabela onde sera enviado os valores de saida e entrada.
	Modelar as tabelas depois e explicar abaixo ou colocar imagem.


- Como deve funcionar a aplicação?

	no front-end terá o formulario com as informações que serão usadas para enviar para o banco de dados.
	
	(DADOS NECESSARIOS PARA ENVIO)

	* Loja , Tipo de Operação (Entrada ou Saida), data de lançamento da operação, valor da operação, numero da nota fiscal ou documento, origem e descrição.
		- isso será para envio enviar os dados para o banco de dados.

	
	(DADOS NECESSARIOS PARA CONSULTAR)

	* Será necessario somente a loja e a data da operação.

Lembrando, cada usuario deverá ter seu login e as lojas que ele trabalha (pode ser mais de uma loja, porem, ele so pode inserir uma loja por vez.



------------------------------------------------------------calculo---------------------------------------------------------------------

(valor de entrada - valor de saida) - saldo do dia anterior.


Metodos GET

	- /entradas (consultar somente os valores de entradas)
		* para consultar o usuario deve necessariamente passar os seguitens argumentos.
			Loja
			Data
	- /saidas (consultar somente os valores de saidas)
		* para consultar o usuario deve necessariamente passar os seguitens argumentos.
			Loja
			Data
	- /entradasESaidas (consultar os 2 tipos de dados ao mesmo tempo)
		* para consultar o usuario deve necessariamente passar os seguitens argumentos.
			Loja
			Data