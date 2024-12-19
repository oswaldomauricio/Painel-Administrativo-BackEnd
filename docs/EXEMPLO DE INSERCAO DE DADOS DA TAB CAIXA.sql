SELECT * FROM analytics.d_users;
SELECT * FROM analytics.d_user_stores;
SELECT * FROM analytics.f_caixa;


INSERT INTO analytics.d_users (NAME, PASSWORD, ROLE)
VALUES ('oswaldo', '44844', 'ADMIN');

INSERT INTO analytics.d_user_stores (ID, LOJA, ID_USERS)
VALUES (1, 101, 1);

INSERT INTO analytics.f_caixa (
    ID, DATA, NUM_DOC, ORIGEM, TIPO_OPERACAO, VALOR, STATUS, ID_USERS, ID_STORES
)
VALUES (
    3, -- ID único para o registro
    SYSDATE, -- Data atual
    'DOC12345', -- Número do documento
    'Sistema Teste', -- Origem do registro
    'SAIDA', -- Tipo de operação
    100.52, -- Valor da operação
    1, -- Status (ex.: 1 = Ativo)
    1, -- ID_USERS referente ao usuário com ID 1 em d_users
    1  -- ID_STORES referente à loja com ID 1 em d_user_stores
);
