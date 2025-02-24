
![Logo](https://norteautopecas.com.br/style/public/img/logosNorte/Logo-Grupo%20Norte2.png)


# Painel Administrativo - Norte auto Peças - 2.0 - Back-End

Esta é a documentação do painel administrativo da empresa Norte Auto Peças.

## Pré-requisitos
Antes de iniciar o projeto, verifique se o seguinte software está instalado em sua máquina:

`python (versão 3.11.9 ou superior)`
`pip`

## Instalação e Execução
Siga as etapas abaixo para executar o projeto frontend localmente:

- Clone o repositório do projeto: `git clone (colocar o repositorio)`.

- Navegue até o diretório do projeto: `cd Painel-Administrativo-BackEnd`.

- Crie o ambiente virtual usando o comando `py -m venv .venv` dentro da pasta.

- Ative o ambiente virtual usando o comando `.venv\Scripts\activate` no cmd.

- Instale as dependencias usando o pip `py -m pip install requests`

## Stacks utilizada

**Front-end:** Next JS - (Version 15.1.3 | using app router)
- Material UI: https://mui.com/material-ui/getting-started/installation/

- TailwindCSS: https://v2.tailwindcss.com/docs

**Back-end:** python, Flask

- Flask: https://flask.palletsprojects.com/en/stable/
- ORM do banco de dados: SQLAlchemy: www.sqlalchemy.org
- Para o banco de dados foi usado o Oracle (interno da empresa).

## Recursos e Funcionalidades
- Autenticação, criação e edição de usuários.
- Inserir e visualizar as entradas e saidas do caixa das lojas por usuario.


# Documentação da API

## endpoint com as informações dos usuarios para Autenticação.

```http
  GET /usuario
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Retorna se o usuario está autenticado para realizar login ou não, caso tenha as informações do usuario, ele poderá realizar o login.

#### status 200 - bem sucedido irá retornar o seguinte json:

```
{
    "id": 8,
    "name": "nome do usuario",
    "password": "senha do usuario",
    "role": "regra de acesso do usuario"
}
```

```http
  POST /usuario
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Insere um novo usuario.

#### status 200 - bem sucedido irá retornar o seguinte json:

```
{
    "result": "Registro incluido com sucesso.",
    "status": 200,
    "usuario": {
        "name": "nome do usuario",
        "password": "senha do usuario"
    }
}
```


```http
  UPDATE /usuario/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Atualiza um usuario.

```http
  DELETE /usuario/${id}
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Deleta um usuario.


## endpoint que verifica as lojas que o usuario tem acesso.

```http
  GET /usuario/lojas
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Retorna quais lojas o usuario autenticado tem acesso.


## endpoint para as entradas e saidas de caixa da loja.

```http
  POST /cashbox/relatorio
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `loja` | `number` | **Obrigatório**. loja que o usuario tem permitido. |
| `data` | `date (DD/MM/YYYY)` | **Obrigatório**. data de inserção dos valores. |

#### Retorna os valores de entrada e saida dos caixas de acordo com a data e loja enviada

```http
  POST /cashbox/relatorio/periodo
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `loja` | `number` | **Obrigatório**. loja que o usuario tem permitido. |
| `data_inicial` | `date (DD/MM/YYYY)` | **Obrigatório**. data inicial de inserção dos valores. |
| `data_final` | `date (DD/MM/YYYY)` | **Obrigatório**. data final de inserção dos valores. |

#### Retorna os valores de entrada e saida dos caixas de acordo com o periodo selecionado.

#### status 200 - bem sucedido irá retornar o seguinte json:
```
{
    "Caixa": [
        {
            "data": "23/01/2025",
            "id": 39,
            "id_users": 1,
            "loja": 101,
            "num_doc": "TESTE",
            "origem": "TESTE",
            "status": true,
            "tipo": null,
            "tipo_operacao": "SAIDA",
            "valor": "5"
        },
        {
            "data": "23/01/2025",
            "id": 45,
            "id_users": 8,
            "loja": 101,
            "num_doc": "teste",
            "origem": "teste",
            "status": true,
            "tipo": null,
            "tipo_operacao": "ENTRADA",
            "valor": "88"
        },
        {
            "data": "31/01/2025",
            "id": 49,
            "id_users": 8,
            "loja": 101,
            "num_doc": "TESTE",
            "origem": "TT3",
            "status": true,
            "tipo": null,
            "tipo_operacao": "ENTRADA",
            "valor": "8"
        }
    ],
    "Saldo": {
        "Saldo total": 91.0,
        "entrada": 96.0,
        "saida": 5.0
    },
    "status": 200
}
```




```http
  POST /cashbox
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `loja` | `number` | **Obrigatório**. loja que o usuario tem permitido. |
| `data` | `date (DD/MM/YYYY)` | **Obrigatório**. data de inserção dos valores. |
| `tipo_operacao` | `string` | **Obrigatório**. Deve ser enviado se é `ENTRADA` ou `SAIDA` apenas! |
| `valor` | `number` | **Obrigatório**. valor da operação. |
| `numero_doc` | `string` | **opcional**. Numero do documento / nota fiscal. |
| `origem` | `string` | **opcional**. Observação. |
| `id_user` | `number` | **Obrigatório**. id do usuario autenticado. |
| `tipo` | `string` | **Obrigatório**.  tipo da entrada ou saida. "RECIBO" ou "NF / CF" |

#### Insere uma nova operacao no caixa.

#### status 200 - bem sucedido irá retornar o seguinte json:
```
{
    "caixas": {
        "date_operacao": "30/01/2025",
        "id": 85,
        "id_user": 8,
        "loja": 101,
        "numero_doc": "TESTE",
        "origem": "TESTEEE",
        "status": 1,
        "tipo": "RECIBO", 
        "tipo_operacao": "SAIDA",
        "valor": 80
    },
    "result": "Registro inserido com sucesso.",
    "status": 200
}
```


```http
  UPDATE /cashbox
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `id` | `number` | **Obrigatório**. id do caixa (obs: esse id não é do usuario e nem da loja, é o id da inserção do caixa.) |

#### Endpoint que altera o valor do status de caixa para 0 , isso é como tivesse deletando o valor do caixa, porem, preferi fazer dessa maneira para ter os registros no banco caso algum seja excluido de forma incorreta.

#### status 200 - bem sucedido irá retornar o seguinte json:
```
{
    "result": "Registro excluido com sucesso.",
    "status": 200
}
```
