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
        END AS ordem_escolaridade,
        ("ultimoStatus"::jsonb)->>'situacao' AS situacao,
        ("ultimoStatus"::jsonb)->>'condicaoEleitoral' AS condicao_eleitoral
    FROM
	    source infos
    )
SELECT 
    id_deputado,
    sexo,
    idade,
    uf_nascimento,
    naturalidade,
    escolaridade,
    ordem_escolaridade,
    CASE
        WHEN idade <= 21 THEN '21-'
        WHEN idade > 20 AND idade <= 30 THEN '21-30'
        WHEN idade > 30 AND idade <= 40 THEN '31-40'
        WHEN idade > 40 AND idade <= 50 THEN '41-50'
        WHEN idade > 50 AND idade <= 60 THEN '51-60'
        WHEN idade > 60 THEN '61+'
        ELSE 'Idade desconhecida'
    END AS faixa_idade,
    situacao,
    condicao_eleitoral
FROM renamed