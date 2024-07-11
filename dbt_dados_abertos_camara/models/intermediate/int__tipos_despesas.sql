WITH source AS (
    SELECT * FROM {{ ref('stg__tipos_despesas') }}
),

despesas_totais AS (
    SELECT
        sd.tipo_despesa AS tipo_despesa,
        SUM(valor_liquido) AS total
    FROM
        source sd
    GROUP BY
        sd.tipo_despesa
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
