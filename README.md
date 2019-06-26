API para crud simples de cadastro de contatos.

API feita com python usando Flask, SQLAlchemy, Marshmallow. 
Banco de dados usado foi PostgreSQL. A biblioteca python para conexão é psycopg2.

Código de criação das tabelas.
```
CREATE TABLE public.pessoas
(
    id bigint NOT NULL DEFAULT nextval('pessoas_id_seq'::regclass),
    nome character varying COLLATE pg_catalog."default",
    cpf character varying COLLATE pg_catalog."default",
    email character varying COLLATE pg_catalog."default",
    datanascimento date,
    CONSTRAINT pessoa_pk PRIMARY KEY (id),
    CONSTRAINT cpf_unique UNIQUE (cpf)

)

CREATE TABLE public.telefones
(
    ddd character varying COLLATE pg_catalog."default",
    id bigint NOT NULL DEFAULT nextval('telefones_id_seq'::regclass),
    numero character varying COLLATE pg_catalog."default",
    pessoa_id bigint,
    CONSTRAINT telefones_pkey PRIMARY KEY (id),
    CONSTRAINT pessoa_id_fk FOREIGN KEY (pessoa_id)
        REFERENCES public.pessoas (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
```
Sequences usados:
```
CREATE SEQUENCE public.pessoa_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

CREATE SEQUENCE public.telefone_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;
```