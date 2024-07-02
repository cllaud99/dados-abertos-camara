with dim_fornecedores
AS
(
    select
        *
    FROM 
        {{ref("int_agregado_cnpj_nome_fornecedores")}}
)
select * from dim_fornecedores