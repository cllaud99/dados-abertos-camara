with source as (
      select * from {{ source('dados_abertos', 'lz_historico_deputado') }}
),
renamed AS
(
SELECT
	id AS id_deputado,
	"siglaPartido" AS sigla_partido,
	"descricaoStatus" AS descricao_status,
	CAST( "dataHora" AS date ) AS dt_evento,
	"idLegislatura" as id_legislatura
FROM
	source rd
)
SELECT * FROM renamed
