WITH despesas_totais AS (
    SELECT
        cod_tipo_despesa,
        tipo_despesa,
        agrupamento
    FROM
        {{ ref('stg__tipos_despesas') }}
)

SELECT * FROM despesas_totais
