/*Apaga os relacionamentos*/


ALTER TABLE LABDATABASE.ALOCACAO DROP CONSTRAINT CARRO_ALOCACAO_FK;
ALTER TABLE LABDATABASE.ALOCACAO DROP CONSTRAINT CLIENTES_ALOCACAO_FK;


/*Apaga as tabelas*/
DROP TABLE LABDATABASE.ALOCACAO;
DROP TABLE LABDATABASE.CLIENTES;
DROP TABLE LABDATABASE.CATEGORIA;
DROP TABLE LABDATABASE.CARRO;

/*Apaga as sequences*/
DROP SEQUENCE LABDATABASE.CATEGORIA_CODIGO_CATEGORIA_SEQ;


/*Cria as tabelas*/




CREATE TABLE LABDATABASE.ALOCACAO (
                CPF VARCHAR2(11) NOT NULL,
                CHASSI VARCHAR2(17) NOT NULL,
                DATA_SAIDA DATE NOT NULL,
                DATA_ENTREGA DATE NOT NULL,
                CONSTRAINT FORNECEDORES_PK PRIMARY KEY (DATA_SAIDA, CPF, CHASSI)

);



CREATE TABLE LABDATABASE.CLIENTES (
                CPF VARCHAR2(11) NOT NULL,
                RG VARCHAR(9) NOT NULL,
                DATA_NASCIMENTO DATE NOT NULL,
                CNH VARCHAR(12) NOT NULL,
                NOME VARCHAR2(255) NOT NULL,
                ENDERECO VARCHAR(255) NOT NULL,
                
                CONSTRAINT CLIENTES_PK PRIMARY KEY (CPF)
);


CREATE TABLE LABDATABASE.CATEGORIA (
                CODIGO_CATEGORIA NUMBER NOT NULL,
                DESCRICAO VARCHAR2(255) NOT NULL,
                VALOR_DIARIA NUMERIC(9, 2) NOT NULL,
                CONSTRAINT PEDIDOS_PK PRIMARY KEY (CODIGO_CATEGORIA)
);


CREATE TABLE LABDATABASE.CARRO (
                CHASSI VARCHAR(17) NOT NULL,
                COR VARCHAR(25) NOT NULL,
                MODELO VARCHAR(30) NOT NULL,
                MARCA VARCHAR(30) NOT NULL,
                PLACA VARCHAR(7) NOT NULL,
                ANO NUMBER NOT NULL,
                CODIGO_CATEGORIA NUMBER NOT NULL, 
                CONSTRAINT PRODUTOS_PK PRIMARY KEY (CHASSI)
);






/*Cria as sequences*/
CREATE SEQUENCE LABDATABASE.CATEGORIA_CODIGO_CATEGORIA_SEQ;




/*Cria os relacionamentos*/
ALTER TABLE LABDATABASE.ALOCACAO ADD CONSTRAINT CARRO_ALOCACAO_FK
FOREIGN KEY (CHASSI)
REFERENCES LABDATABASE.CARRO (CHASSI)
NOT DEFERRABLE;

ALTER TABLE LABDATABASE.ALOCACAO ADD CONSTRAINT CLIENTES_ALOCACAO_FK
FOREIGN KEY (CPF)
REFERENCES LABDATABASE.CLIENTES (CPF)
NOT DEFERRABLE;

ALTER TABLE LABDATABASE.CARRO ADD CONSTRAINT CATEGORIA_CARRO_FK
FOREIGN KEY (CODIGO_CATEGORIA)
REFERENCES LABDATABASE.CARRO (CODIGO_CATEGORIA)
NOT DEFERRABLE;


/*Garante acesso total as tabelas*/
GRANT ALL ON LABDATABASE.ALOCACAO  TO LABDATABASE;
GRANT ALL ON LABDATABASE.CLIENTES TO LABDATABASE;
GRANT ALL ON LABDATABASE.CATEGORIA TO LABDATABASE;
GRANT ALL ON LABDATABASE.CARRO TO LABDATABASE;


ALTER USER LABDATABASE quota unlimited on USERS;