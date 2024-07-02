WITH dim_tipos_documentos AS
(
SELECT
	id,
	initcap(tipo_documento) AS tipo_documento
FROM
	{{ref("stg__tipo_documentos")}} rtd
) SELECT * FROM dim_tipos_documentos