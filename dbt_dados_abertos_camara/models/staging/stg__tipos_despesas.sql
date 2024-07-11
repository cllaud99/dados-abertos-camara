WITH source AS (
    SELECT * FROM {{ source('dados_abertos', 'lz_despesas') }}
),

despesas_totais AS (
    SELECT
        sd."tipoDespesa" AS tipo_despesa,
        SUM(sd."valorLiquido") AS total
    FROM
        source sd
    GROUP BY
        sd."tipoDespesa"
),

top_despesas AS (
    SELECT
        tipo_despesa,
        total,
        ROW_NUMBER() OVER (ORDER BY total DESC) AS ranking
    FROM
        despesas_totais
)

SELECT
    td.ranking AS cod_tipo_despesa,
    total::bigint AS total,
    td.tipo_despesa,
    CASE
        WHEN td.ranking <= 5 THEN td.tipo_despesa
        ELSE 'OUTROS'
    END AS agrupamento
FROM
    top_despesas td
ORDER BY
    td.total DESC
