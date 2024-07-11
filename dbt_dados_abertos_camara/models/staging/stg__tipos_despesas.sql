WITH source AS (
    SELECT * FROM {{ source('dados_abertos', 'lz_despesas') }}
),

despesas_totais AS (
    SELECT
        sd."tipoDespesa" AS tipo_despesa,
        sd."valorLiquido" AS valor_liquido
    FROM
        source sd

)

SELECT * FROM despesas_totais
