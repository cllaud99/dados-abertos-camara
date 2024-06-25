WITH
	renamed AS
(
SELECT
	deputados.id AS id_deputado,
	deputados.nome,
	deputados."siglaPartido" AS sigla_partido,
	deputados."siglaUf"  AS uf,
	deputados."urlFoto" AS url_foto
FROM
	{{ref('raw__deputados')}}  deputados
)
SELECT * FROM renamed