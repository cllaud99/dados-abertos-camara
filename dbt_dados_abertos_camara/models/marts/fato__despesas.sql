-- models/fato_despesas.sql

WITH fato_despesas AS (
    SELECT
        id_deputado,
        dt_despesa,
        tipo_despesa,
        cnpj_fornecedor,
        vlr_liquido AS vlr_liquido,
        vlr_documento AS vlr_documento,
        vlr_glosa AS vlr_glosa,
        sd.cod_tipo_despesa
    FROM {{ ref('stg__despesas') }} sd
)
SELECT
    *
FROM
    fato_despesas
