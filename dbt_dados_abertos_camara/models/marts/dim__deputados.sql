WITH dim_deputados
AS
(
SELECT
	deputados.id_deputado,
	deputados.nome,
	deputados.sigla_partido,
	deputados.uf,
	deputados.url_foto,
	infos.sexo,
	infos.idade,
	infos.uf_nascimento,
	infos.escolaridade,
	infos.ordem_escolaridade,
	infos.faixa_idade
FROM
	{{ref("stg__deputados")}} deputados
LEFT JOIN
	{{ref("stg__infos_extras")}} infos ON
	infos.id_deputado = deputados.id_deputado
)
SELECT * FROM dim_deputados