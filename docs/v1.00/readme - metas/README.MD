# Seção de Metas 📈

Nesta seção, estará as rotas para as metas das lojas.




## META LOJAS



```http
  POST /metas/mes/lojas
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `loja`      | `string` | **Obrigatório**. A loja que o usuário tem acesso. |
| `data`      | `string` | **Obrigatório**. A data no formato '01/MM/YYYY'. |




### Query que busca as metas da loja pelo mês!

```sql
SELECT 
            MF.UF,
            MF.COD_FILIAL,
            MF.DATA AS DATA_META,
            MES_META,
            VENDAS.TOTAL_VENDAS,
            MF.META,
            TRUNC(((VENDAS.TOTAL_VENDAS / MF.META) * 100),2) AS PERCENTUAL
        FROM (
            SELECT
                EMP_CODG AS COD_FILIAL,
                EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,     
                SUM((CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END)) AS TOTAL_VENDAS
            FROM ANALYTICS.COMISSAO C
            WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
            GROUP BY EMP_CODG, EXTRACT(MONTH FROM C.COMIS_EMISSAO), EXTRACT(YEAR FROM C.COMIS_EMISSAO)
        ) VENDAS
        LEFT JOIN ANALYTICS.METAS_FILIAIS MF ON VENDAS.COD_FILIAL = MF.COD_FILIAL AND VENDAS.MES_META = MF.MES AND VENDAS.ANO_META = MF.ANO_META
        WHERE VENDAS.COD_FILIAL = ${loja} and MF.DATA = TO_DATE('${data}', 'DD/MM/YYYY')
        order by MF.COD_FILIAL, MES_META
```


### Query que busca as metas da loja pela semana!


```sql
SELECT 
        A.COD_FILIAL,
        A.UF,
        A.DATA,
        A.DATA_INICIO,
        A.DATA_FIM,
        A.META_SEMANAL,
        SUM(VENDAS.TOTAL_VENDAS) AS TOTAL_VENDAS_SEMANA,
        TRUNC(((SUM(VENDAS.TOTAL_VENDAS) / A.META_SEMANAL) * 100), 2) AS PERCENTUAL
    FROM (
        SELECT 
          MF.COD_FILIAL,
          MF.UF,
          MF.MES,
          MF.GERENTE,
          MF.ANO_META,
          MF.DATA,
          MS.DATA_INICIO,
          MS.DATA_FIM,
          TRUNC(((MF.META / MD.QTD_DIAS) * MS.QTD_DIAS),2) AS META_SEMANAL  ---- DIMINUI O CALCULO DAS METAS SEMANAIS
     FROM ANALYTICS.METAS_FILIAIS MF
     LEFT JOIN ANALYTICS.PARAMETRO_META_SEMANA MS ON MF.DATA = MS.DATA
     LEFT JOIN ANALYTICS.PARAMETRO_META_DIAS MD ON MD.DATA = MF.DATA  ---- INCLUI ESSE LEFT JOIN PARA PEGAR AUTOMATICO A QUANTIDADE DE DIAS DO MES
    ) A
    LEFT JOIN (
        SELECT
            C.EMP_CODG AS COD_FILIAL,
            TRUNC(C.COMIS_EMISSAO) AS DATA,
            (CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END) AS TOTAL_VENDAS
        FROM ANALYTICS.COMISSAO C
        WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
    ) VENDAS
    ON VENDAS.DATA BETWEEN A.DATA_INICIO AND A.DATA_FIM AND A.COD_FILIAL = VENDAS.COD_FILIAL
    WHERE A.DATA = TO_DATE(${data}, 'DD/MM/YYYY') -- Definir o mês
    AND A.COD_FILIAL = ${loja} -- Definir a loja
    GROUP BY
        A.COD_FILIAL,
        A.UF,
        A.DATA,
        A.DATA_INICIO,
        A.DATA_FIM,
        A.META_SEMANAL
    ORDER BY  
        A.COD_FILIAL, A.DATA, A.DATA_INICIO
```
## METAS VENDEDORES

Buscar as metas dos vendedores de cada loja

```http
  POST /metas/mes/vendedores
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `loja`      | `string` | **Obrigatório**. A loja que o usuário tem acesso. |
| `data`      | `string` | **Obrigatório**. A data no formato '01/MM/YYYY'. |



#### Query que faz a busca no banco de dados:

```sql
SELECT 
                        MV.COD_FILIAL,
                        MV.NOME_VENDEDOR,
                        EXTRACT(MONTH FROM MV.DATA_META) AS MES,
                        EXTRACT(YEAR FROM MV.DATA_META) AS ANO,     
                        MV.DATA_META AS DATA,
                        VENDAS.TOTAL_VENDAS,
                        MV.META,
                        TRUNC(((VENDAS.TOTAL_VENDAS / MV.META) * 100), 2) AS PERCENTUAL
                    FROM ANALYTICS.METAS_VENDEDORES MV
                    LEFT JOIN
                    (
                        SELECT
                            CASE 
                                WHEN FUNC_USUARIO IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA'
                                WHEN FUNC_USUARIO IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'  
                                ELSE FUNC_USUARIO 
                            END AS NOME_VENDEDOR,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,     
                            SUM((CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END)) AS TOTAL_VENDAS
                        FROM VELIT.COMISSAO C
                        WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                        GROUP BY 
                            CASE 
                                WHEN FUNC_USUARIO IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA' 
                                WHEN FUNC_USUARIO IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'    
                                ELSE FUNC_USUARIO 
                            END,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO),
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO)
                    ) VENDAS
                    ON VENDAS.NOME_VENDEDOR = 
                        CASE 
                            WHEN MV.NOME_VENDEDOR IN ('ESMERALDAS', 'ESMERALDASERVICO') THEN 'ESMERALDA' 
                            WHEN MV.NOME_VENDEDOR IN ('STHEFANY', 'STHEFANYSERVICO') THEN 'STHEFANY'    
                            ELSE MV.NOME_VENDEDOR 
                        END
                    AND VENDAS.MES_META = EXTRACT(MONTH FROM MV.DATA_META) 
                    AND VENDAS.ANO_META = EXTRACT(YEAR FROM MV.DATA_META)
                    WHERE MV.COD_FILIAL = '${lojaVendedor}' -- Seleciona o número da filial
                    AND MV.DATA_META = TO_DATE('${dataVendedor}', 'DD/MM/YYYY') -- Seleciona a data
                    ORDER BY PERCENTUAL DESC
```


### Retorno da API


```
STATUS 200 - OK

{
    "meta_vendedores_mensal": [
        {
            "ANO": 2025,
            "DATA": "01/01/2025",
            "LOJA": 102,
            "MES": 1,
            "META": 150000.0,
            "PORCENTAGEM": 91.78,
            "TOTAL_VENDAS": 137682.74,
            "VENDEDOR": "KELVIN"
        },
        {
            "ANO": 2025,
            "DATA": "01/01/2025",
            "LOJA": 102,
            "MES": 1,
            "META": 190000.0,
            "PORCENTAGEM": 79.5,
            "TOTAL_VENDAS": 151061.9,
            "VENDEDOR": "DARLAN"
        },
        {
            "ANO": 2025,
            "DATA": "01/01/2025",
            "LOJA": 102,
            "MES": 1,
            "META": 100000.0,
            "PORCENTAGEM": 51.77,
            "TOTAL_VENDAS": 51772.73,
            "VENDEDOR": "WSANTOS"
        },
        {
            "ANO": 2025,
            "DATA": "01/01/2025",
            "LOJA": 102,
            "MES": 1,
            "META": 90000.0,
            "PORCENTAGEM": 17.53,
            "TOTAL_VENDAS": 15778.19,
            "VENDEDOR": "LUCASSOUZA"
        }
    ],
    "status": "200"
}
```



```
STATUS 400 
{
    "error": "Não existem metas para esse vendedor",
    "status": "400"
}
```
## METAS SEMANAIS VENDEDORES


```http
  POST /metas/semanal/vendedor
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `nome_vendedor`      | `string` | **Obrigatório**. O Nome do vendedor que foi clicado. |
| `data`      | `string` | **Obrigatório**. A data no formato '01/MM/YYYY' (passada ao clicar no nome do vendedor conforme exemplo abaixo). |



#### Query que faz a busca no banco de dados:

```sql
SELECT 
            A.COD_FILIAL,
            A.NOME_VENDEDOR,
            A.DATA,
            A.DATA_INICIO,
            A.DATA_FIM,
            A.META_SEMANAL,
            SUM(VENDAS.TOTAL_VENDAS) AS TOTAL_VENDAS_SEMANA,
            TRUNC(((SUM(VENDAS.TOTAL_VENDAS)/ A.META_SEMANAL)*100),2) AS PERCENTUAL
       FROM (
        SELECT 
        MV.COD_FILIAL,
        MV.NOME_VENDEDOR,
        MV.DATA_META AS DATA,
        MS.DATA_INICIO,
        MS.DATA_FIM,
        TRUNC(((MV.META / MD.QTD_DIAS) * MS.QTD_DIAS),2) AS META_SEMANAL 
   FROM ANALYTICS.METAS_VENDEDORES MV
   LEFT JOIN ANALYTICS.PARAMETRO_META_SEMANA MS ON MV.DATA_META = MS.DATA
   LEFT JOIN ANALYTICS.PARAMETRO_META_DIAS MD ON MD.DATA = MV.DATA_META
      ) A
      LEFT JOIN (
           SELECT
             C.FUNC_USUARIO AS NOME_VENDEDOR,
             TRUNC(C.COMIS_EMISSAO) AS DATA,
             (CASE WHEN C.COMIS_TIPO_VENDA = 'DE' THEN C.COMIS_VALOR_VENDA * -1 ELSE C.COMIS_VALOR_VENDA END) AS TOTAL_VENDAS
         FROM VELIT.COMISSAO C
         WHERE TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
               ) VENDAS
        ON VENDAS.DATA BETWEEN A.DATA_INICIO AND A.DATA_FIM AND A.NOME_VENDEDOR = VENDAS.NOME_VENDEDOR
        WHERE A.NOME_VENDEDOR = '${nomeVendedor}'  --------- Selecionar o Vendedor
        AND A.DATA = TO_DATE('${dataVendedor}', 'DD/MM/YYYY') ------------------- Selecionar a data de inicio
        GROUP BY
            A.COD_FILIAL,
            A.NOME_VENDEDOR,
            A.DATA,
            A.DATA_INICIO,
            A.DATA_FIM,
            A.META_SEMANAL
     ORDER BY  A.NOME_VENDEDOR, A.DATA, A.DATA_INICIO
```


Buscar as metas dos vendedores de cada loja por SEMANA, será usado quando o usuário clicar no nome do vendedor, deve aparecer uma nova tabela em baixo mostrando a meta da semana desse vendedor.

## exemplo abaixo:

![Meta](https://i.ibb.co/84YVgfgH/image.png)

## METAS REGIONAIS

#### Somente alguns usuários tem acesso a esse relatorio, então deve ser feito um select no banco usando o comando abaixo para trazer qual a regional que o usuário tem acesso:

```http
  POST /metas/regional/usuarios
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `id`      | `string` | **Obrigatório**. ID do usuário logado. |


```sql
 SELECT * FROM ANALYTICS.REGIONAIS_USERS WHERE id_users = {ID}
```

### Regional

Com a informação se o usuário tem ou não acesso, podemos fazer o envio para a URL abaixo.


```http
  POST /metas/regional
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `NOME_REGIONAL`      | `string` | **Obrigatório**. enviar o nome da regional que foi pego na requisição acima. |
| `DATA`      | `string` | **Obrigatório**. A data no formato '01/MM/YYYY'|



```sql
SELECT 
                    REGIONAL,
                    DATA,
                    SUM(TOTAL_VENDAS) AS VENDAS,
                    SUM(META) AS META_TOTAL,
                    TRUNC((SUM(TOTAL_VENDAS) / SUM(META)) * 100, 2) AS PERCENTUAL
                FROM (
                    SELECT
                        MF.REGIONAL,
                        MF.DATA,
                        MF.META,
                        VENDAS.TOTAL_VENDAS
                    FROM
                        METAS_FILIAIS MF
                    LEFT JOIN (
                        SELECT
                            EMP_CODG AS COD_FILIAL,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,
                            SUM(CASE
                                    WHEN C.COMIS_TIPO_VENDA = 'DE' THEN
                                        C.COMIS_VALOR_VENDA * -1
                                    ELSE
                                        C.COMIS_VALOR_VENDA
                                END) AS TOTAL_VENDAS
                        FROM
                            ANALYTICS.COMISSAO C
                        WHERE
                            TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                        GROUP BY
                            EMP_CODG,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO),
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO)
                    ) VENDAS ON VENDAS.COD_FILIAL = MF.COD_FILIAL
                        AND VENDAS.MES_META = EXTRACT(MONTH FROM MF.DATA)
                        AND VENDAS.ANO_META = EXTRACT(YEAR FROM MF.DATA)
                    WHERE
                        REGIONAL = '${Regional}'
                        AND MF.DATA = TO_DATE('${dataRegional}', 'DD/MM/YYYY')
                )
                GROUP BY 
                    REGIONAL, DATA
                ORDER BY 
                    PERCENTUAL DESC
```


#### Buscar a meta das lojas que o regional tem acesso.


```http
  POST /metas/regional/loja
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `NOME_REGIONAL`      | `string` | **Obrigatório**. enviar o nome da regional que foi pego na requisição acima. |
| `DATA`      | `string` | **Obrigatório**. A data no formato '01/MM/YYYY'|

```sql
SELECT 
                    METAS.REGIONAL,
                    METAS.UF,
                    METAS.COD_FILIAL,
                    METAS.DATA,
                    SUM(TOTAL_VENDAS) AS VENDAS,
                    SUM(METAS.META) AS META_TOTAL,
                    TRUNC((SUM(TOTAL_VENDAS) / SUM(METAS.META)) * 100, 2) AS PERCENTUAL
                FROM (
                    SELECT
                        MF.REGIONAL,
                        MF.UF,
                        MF.COD_FILIAL,
                        MF.DATA,
                        MF.META,
                        
                        VENDAS.TOTAL_VENDAS
                    FROM
                        METAS_FILIAIS MF
                    LEFT JOIN (
                        SELECT
                            EMP_CODG AS COD_FILIAL,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO) AS MES_META,
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO) AS ANO_META,
                            SUM(CASE
                                    WHEN C.COMIS_TIPO_VENDA = 'DE' THEN
                                        C.COMIS_VALOR_VENDA * -1
                                    ELSE
                                        C.COMIS_VALOR_VENDA
                                END) AS TOTAL_VENDAS
                        FROM
                            ANALYTICS.COMISSAO C
                        WHERE
                            TRUNC(C.COMIS_EMISSAO) >= TO_DATE('01/01/2024', 'DD/MM/YYYY')
                        GROUP BY
                            EMP_CODG,
                            EXTRACT(MONTH FROM C.COMIS_EMISSAO),
                            EXTRACT(YEAR FROM C.COMIS_EMISSAO)
                    ) VENDAS ON VENDAS.COD_FILIAL = MF.COD_FILIAL
                        AND VENDAS.MES_META = EXTRACT(MONTH FROM MF.DATA)
                        AND VENDAS.ANO_META = EXTRACT(YEAR FROM MF.DATA)
                    WHERE
                        MF.REGIONAL = '${Regional}'
                        AND TRUNC(MF.DATA) = TO_DATE('${dataRegional}', 'DD/MM/YYYY')
                ) METAS
                GROUP BY 
                    METAS.REGIONAL, METAS.COD_FILIAL, METAS.DATA, METAS.UF
                ORDER BY 
                    COD_FILIAL ASC
```


### Exemplo de como deve ficar no dashboard:

![Meta](https://i.ibb.co/SwhngX5v/image.png)