WITH despesas_totais AS (
    SELECT
        *
    FROM
        {{ ref('stg_tipos_despesas') }} 
) SELECT * FROM despesas_totais