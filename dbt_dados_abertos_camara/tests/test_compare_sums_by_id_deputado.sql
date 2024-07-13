WITH
    fato_agg AS (
        SELECT
            id_deputado,
            ROUND(SUM(vlr_liquido)::NUMERIC, 2) AS total_vlr_liquido
        FROM {{ ref('fato__despesas') }}
        GROUP BY id_deputado
    ),
    stg_agg AS (
        SELECT
            id_deputado,
            ROUND(SUM(vlr_liquido)::NUMERIC, 2) AS total_vlr_liquido
        FROM {{ ref('stg__despesas') }}
        GROUP BY id_deputado
    )
SELECT
    fato_agg.id_deputado,
    fato_agg.total_vlr_liquido AS fato_total,
    stg_agg.total_vlr_liquido AS stg_total
FROM fato_agg
FULL OUTER JOIN stg_agg
    ON fato_agg.id_deputado = stg_agg.id_deputado
WHERE COALESCE(fato_agg.total_vlr_liquido, 0) <> COALESCE(stg_agg.total_vlr_liquido, 0)
