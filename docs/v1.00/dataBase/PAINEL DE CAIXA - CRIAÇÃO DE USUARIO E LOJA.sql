--------------------------------COMO CRIAR UM NOVO USUARIO NO PAINEL DE CAIXAS-----------------------------------

--------------------------------VERIFICAR USUARIOS---------------------------------------------------------------
SELECT U.* FROM ANALYTICS.D_USERS U

-- AQUI VOCÊ PODE VERIFICAR TODOS OS USUARIOS QUE TEM NO PAINEL.
-- ROLE É A PERMISSÃO QUE O USUARIO TEM DENTRO DO PAINEL
--USER É O PADRAO, ADMIN PODE SER USADO PARA DEIXAREM EXCLUIR VALOR CASO PASSE DA DATA PARA LANÇAMENTO.

---------------------------------INSERIR USUARIO NOVO------------------------------------------------------------
INSERT INTO ANALYTICS.D_USERS (ID, NAME, PASSWORD, ROLE)
VALUES (
    (SELECT MAX(U.ID) + 1 FROM ANALYTICS.D_USERS U), --NAO ALTERAR ESSA LINHA, POIS ELA PEGA O ID MAIOR E ADICIONA + 1
    'TESTE', -- TROCAR PELO NOME DO USUARIO
    'SENHA', -- SENHA DO USUARIO
    'USER' -- COLOCAR A REGRA DO USUARIO, SE FOR DE LOJA É 'USER' E 'ADMIN' PARA PERMISSAO PRIVILEGIADA
);



---------------------------------DELETAR USUARIO------------------------------------------------------------------
DELETE FROM ANALYTICS.D_USERS
WHERE NAME = 'NOME DO USUARIO';








------------------------------------------------------------------------------------------------------------------
--------------------------------COMO ADICIONAR UMA LOJA PARA UM USUARIO-------------------------------------------

--------------------------------VERIFICAR LOJA DOS USUARIOS-------------------------------------------------------
SELECT S.ID, S.LOJA, U.NAME, S.ID_USERS
  FROM ANALYTICS.D_USER_STORES S, ANALYTICS.D_USERS U
 WHERE 
       U.ID = S.ID_USERS
       AND U.NAME = 'oswaldo';
 
---------------------------------INSERIR LOJA PARA O USUARIO--------------------------------------------------------

INSERT INTO ANALYTICS.D_USER_STORES (ID, LOJA, ID_USERS)
VALUES (
    (SELECT MAX(S.ID) + 1 FROM ANALYTICS.D_USER_STORES S), --NAO ALTERAR ESSA LINHA, POIS ELA PEGA O ID MAIOR E ADICIONA + 1
    'LOJA DO USUARIO', -- TROCAR PELA LOJA QUE O USUARIO TERÁ ACESSO.
    (SELECT U.ID FROM ANALYTICS.D_USERS U WHERE NAME = 'oswaldo') -- TROQUE AQUI PELO NOME DO USUARIO.
);

---------------------------------DELETAR LOJA DO USUARIO--------------------------------------------------------------
DELETE FROM ANALYTICS.D_USER_STORES
WHERE ID_USERS = (
    SELECT ID FROM ANALYTICS.D_USERS
    WHERE NAME = 'oswaldo' -- TROCAR PELO NOME DO USUARIO QUE DESEJA DELETAR
)
AND LOJA = 'LOJA DO USUARIO'; -- TROCAR PELA LOJA QUE QUER TIRAR O ACESSO.





