# API de controle de caixa - Norte Auto Peças

![Logo](https://norteautopecas.com.br/style/public/img/logosNorte/Logo-Grupo%20Norte2.png)

## Objetivo

Criar uma API para monitorar o controle, recebimento, e saida dos caixas das lojas. Tendo assim um controle e acesso melhor para a diretoria, e para quem realiza as conferencias.

Com o crescimento de demandas, mais funcionalidades seram implementadas.

## Dependencias


```sh
instalar a versão do python > 3.11: https://www.python.org/downloads/
```



```sh
instale a versão do visual studio 2022, e dentro do programa instale a versão Visual Studio Enterprise 2022 preview pois é necessario para algumas depencias de banco de dados que so rodam se estiver instalados: https://https://visualstudio.microsoft.com/pt-br/vs/
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

- cd (caminho da pasta de destino).

- .\.venv\Scripts\activate

- flask run --host=0.0.0.0

ou se preferir, execute o arquivo localizado nos docs "docs/inicializar/iniciar - backend - caixa.bat".

lembrando, é importante ter todas as dependencias instaladas para que funcione corretamente.

## Linguagem e frameworks utilizados.

Para o backend foi escolhido o Python com o framework Flask.

Utilizei o Flask pydantic para mapeamento das rotas e metodos (pode ser conferido na rota abaixo.)

```sh

/apidoc/swagger#/  
```

Para o banco de dados foi usado o BD da Oracle e usei o SQLAlchemy para ORM.  
 

## Planejamento

Criação e monitoramento de Saídas e Entradas do caixa das lojas.

Deve ser adicionado esses valores de acordo com a loja, e deve ser validado se o usuário tem acesso aquela rota ou não.

# Endpoints de Usuarios

## GET


```sh
/usuario
Endpoint que retorna o usuario passando o 'name' e 'password'
```

```sh
/usuario/lojas
Endpoint que retorna o as lojas do usuario e o usuario passando o 'name' e 'password'
```

## POST

```sh
/usuario
Endpoint que cria um usuario novo passando o 'name' e 'password'
```

## UPDATE

```sh
/usuario/`${id}`
Endpoint que atualiza as informações de usuario passando o 'name' e 'password'
```

## DELETE

```sh
/usuario/`${id}`
Endpoint que deleta o login do usuario passando o 'name' e 'password'
```

