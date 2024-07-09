with source as (
    select * from {{ source('seeds', 'seeds__tipos_documentos') }}
),
renamed AS
(
SELECT
	id as id_tipo_documento,
	initcap(descricao) AS tipo_documento
FROM
	source rtd
) SELECT * FROM renamed
