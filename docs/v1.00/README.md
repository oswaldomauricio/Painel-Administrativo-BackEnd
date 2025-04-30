# API de controle de caixa - Norte Auto Peças

![Logo](https://norteautopecas.com.br/style/public/img/logosNorte/Logo-Grupo%20Norte2.png)

## Objetivo

Criar uma API para monitorar o controle, recebimento, e saida dos caixas das lojas. Tendo assim um controle e acesso melhor para a diretoria, e para quem realiza as conferencias.

Com o crescimento de demandas, mais funcionalidades seram implementadas.

## Dependencias de execução

```sh
instalar a versão do python > 3.11: https://www.python.org/downloads/
```



```sh
instale a versão do visual studio 2022, e dentro do programa instale a versão Visual Studio Enterprise 2022 preview pois é necessario para algumas depencias de banco de dados que so rodam se estiver instalados: https://https://visualstudio.microsoft.com/pt-br/vs/
```

```sh
Baixe o instant Client versão > 23.0 e adicione no c:/ da sua maquina:

https://www.oracle.com/br/database/technologies/instant-client/winx64-64-downloads.html

ele serve para as instancias / conexão do banco de dados.
```


## Instalação e Execução
Siga as etapas abaixo para executar o projeto frontend localmente:

- Clone o repositório do projeto: `git clone (colocar o repositorio)` 
https://github.com/oswaldomauricio/Painel-Administrativo-BackEnd.

- Navegue até o diretório do projeto: `cd caminho do projeto na sua maquina/Painel-Administrativo-BackEnd`.

- Crie o ambiente virtual usando o comando `py -m venv .venv` dentro da pasta.

- Ative o ambiente virtual usando o comando `.venv\Scripts\activate` no cmd.

- Instale as dependencias usando o pip `pip install -r requirements.txt`

- Caso dê erro, baixe o visual studio interprise 2022 e tente novamente!

## Como iniciar o projeto

Abra um terminal no windows e execute os seguintes comandos.

- cd (caminho da pasta de destino)

- .\.venv\Scripts\activate

- flask run --host=0.0.0.0

ou se preferir, execute o arquivo localizado nos docs "docs/inicializar/iniciar - backend - caixa.bat".

lembrando, é importante ter todas as dependencias instaladas para que funcione corretamente.


## Como iniciar o Front-End

verifique no link abaixo o repositorio no github para ver a documentação de como inicializa-lo.

https://github.com/oswaldomauricio/painel_administrativo_FrontEnd