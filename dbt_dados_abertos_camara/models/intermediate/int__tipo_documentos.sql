WITH documentos AS (
    SELECT
        *
    FROM
        {{ref('stg__tipo_documentos')}}
)
SELECT * FROM documentos
