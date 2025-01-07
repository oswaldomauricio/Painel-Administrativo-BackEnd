
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

```http
  POST /usuario
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `name` | `string` | **Obrigatório**. Nome do usuario. |
| `password` | `string` | **Obrigatório**. Senha do usuario. |

#### Insere um novo usuario.


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
  GET /cashbox
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `id_loja` | `number` | **Obrigatório**. id da loja que o usuario tem permitido. |
| `data` | `date (DD/MM/YYYY)` | **Obrigatório**. data de inserção dos valores. |

#### Retorna os valores de entrada e saida dos caixas de acordo com a data e loja enviada

```http
  POST /cashbox
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `id_loja` | `number` | **Obrigatório**. id da loja que o usuario tem permitido. |
| `data` | `date (DD/MM/YYYY)` | **Obrigatório**. data de inserção dos valores. |
| `tipo_operacao` | `string` | **Obrigatório**. Deve ser enviado se é `ENTRADA` ou `SAIDA` apenas! |
| `valor` | `number` | **Obrigatório**. valor da operação. |
| `numero_doc` | `string` | **opcional**. Numero do documento / nota fiscal. |
| `origem` | `string` | **opcional**. Observação. |
| `id_user` | `number` | **Obrigatório**. id do usuario autenticado. |

#### Insere uma nova operacao no caixa.


```http
  UPDATE /cashbox
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `id` | `number` | **Obrigatório**. id do caixa (obs: esse id não é do usuario e nem da loja, é o id da inserção do caixa.) |

#### Endpoint que altera o valor do status de caixa para 0 , isso é como tivesse deletando o valor do caixa, porem, preferi fazer dessa maneira para ter os registros no banco caso algum seja excluido de forma incorreta.


