with source as (
      select * from {{ source('dados_abertos', 'lz_infos_extras') }}
)
,
    renamed as (
    SELECT
	    id AS id_deputado,
	    sexo,
	    EXTRACT( YEAR FROM AGE(CURRENT_DATE, "dataNascimento"))::INTEGER AS idade,
	    "ufNascimento" AS uf_nascimento,
	    "municipioNascimento" AS naturalidade,
	    COALESCE(escolaridade,'Não informada') AS escolaridade
    FROM
	    source infos
    )
SELECT * FROM renamed