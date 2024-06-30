with source as (
    select * from {{ref("stg__tipo_documentos")}}
),
renamed AS
(
SELECT
	id,
	initcap(descricao) AS tipo_documento
FROM
	source rtd
) SELECT * FROM renamed