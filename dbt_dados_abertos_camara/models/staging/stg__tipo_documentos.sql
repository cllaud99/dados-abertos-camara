WITH source AS (
    SELECT * FROM {{ source('seeds', 'seeds__tipos_documentos') }}
),

renamed AS (
    SELECT
        id AS id_tipo_documento,
        initcap(descricao) AS tipo_documento
    FROM
        source
)

SELECT * FROM renamed
