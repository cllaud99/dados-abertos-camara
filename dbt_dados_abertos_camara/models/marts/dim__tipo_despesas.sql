WITH despesas_totais AS (
    SELECT *
    FROM
        {{ ref('stg__tipos_despesas') }}
)

SELECT * FROM despesas_totais
