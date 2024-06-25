WITH renamed AS
(
SELECT
	id,
	initcap(descricao) AS tipo_documento
FROM
	{{ref("raw__tipo_documentos")}} rtd
) SELECT * FROM renamed