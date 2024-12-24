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

```sh
/cashbox
Endpoint que retorna os valores de entrada e saida dos caixas, deve ser passado o id da loja 'id_loja' e 'data'
```


## POST

```sh
/usuario
Endpoint que cria um usuario novo passando o 'name' e 'password'
```

```sh
/cashbox
Endpoint que insere os valores de caixa, deve ser passado os argumentos abaixo.
exemplo
{
    "id_loja": 41,
    "data": "02/12/2024",
    "tipo_operacao": "ENTRADA",
    "valor": 104,
    "numero_doc": 152,
    "origem": "testeinsert",
    "id_user": 29
}
```

## UPDATE

```sh
/usuario/`${id}`
Endpoint que atualiza as informações de usuario passando o 'name' e 'password'
```

```sh
/cashbox
Endpoint que altera o valor do status de caixa para 0 , isso é como tivesse deletando o valor do caixa, porem, preferi fazer dessa maneira para ter os registros caso algum seja excluido de forma errada.

deve ser enviado o id do caixa como o exemplo abaixo:

{
    "id": 1
}
```


## DELETE

```sh
/usuario/`${id}`
Endpoint que deleta o login do usuario passando o 'name' e 'password'
```