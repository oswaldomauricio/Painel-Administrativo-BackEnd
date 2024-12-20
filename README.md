# API de controle de caixa - Norte Auto Peças

## Objetivo

Criar uma API para monitorar o controle, recebimento, e saida dos caixas das lojas. Tendo assim um controle e acesso melhor para a diretoria, e para quem realiza as conferencias.

Com o crescimento de demandas, mais funcionalidades seram implementadas.

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