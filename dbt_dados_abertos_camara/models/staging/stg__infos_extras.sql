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
	    COALESCE(NULLIF(escolaridade, ''), 'Não Informada') AS escolaridade,
		CASE
			WHEN escolaridade = 'Não Informada' THEN -1
			WHEN escolaridade = 'Ensino Fundamental' THEN 0
            WHEN escolaridade = 'Primário Incompleto' THEN 1
            WHEN escolaridade = 'Secundário' THEN 2
            WHEN escolaridade = 'Ensino Médio Incompleto' THEN 3
            WHEN escolaridade = 'Ensino Médio' THEN 4
            WHEN escolaridade = 'Superior Incompleto' THEN 5
            WHEN escolaridade = 'Superior' THEN 6
            WHEN escolaridade = 'Pós-Graduação' THEN 7
            WHEN escolaridade = 'Mestrado Incompleto' THEN 8
            WHEN escolaridade = 'Mestrado' THEN 9
            WHEN escolaridade = 'Doutorado Incompleto' THEN 10
            WHEN escolaridade = 'Doutorado' THEN 11
            ELSE -1
        END AS ordem_escolaridade
    FROM
	    source infos
    )
SELECT * FROM renamed