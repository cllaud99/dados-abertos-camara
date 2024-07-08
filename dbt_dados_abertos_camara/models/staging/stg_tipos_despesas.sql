with source as (
      select * from {{ source('dados_abertos', 'lz_despesas') }}
), despesas_totais AS (
    SELECT
        sd."tipoDespesa" AS tipo_despesa,
        SUM(sd."valorLiquido") AS total
    FROM
        source AS sd
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
    ROW_NUMBER() OVER () AS id_tipo_despesa, -- Adicionando índice como chave primária
    td.tipo_despesa,
    CASE 
        WHEN td.ranking <= 8 THEN td.tipo_despesa
        ELSE 'OUTROS'
    END AS agrupamento
FROM
    top_despesas AS td
ORDER BY
    td.total DESC