WITH documentos AS (
    SELECT
        *
    FROM
        {{ref('stg__despesas')}}
)
SELECT * FROM documentos
