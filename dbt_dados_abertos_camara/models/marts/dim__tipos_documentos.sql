WITH dim_tipos_documentos AS (
    SELECT
        id_tipo_documento,
        initcap(tipo_documento) AS tipo_documento
    FROM
        {{ ref("int__tipo_documentos") }}
)

SELECT * FROM dim_tipos_documentos
