with
    renamed as (
    SELECT
	    id AS id_deputado,
	    sexo,
	    EXTRACT( YEAR FROM AGE(CURRENT_DATE, "dataNascimento"))::INTEGER AS idade,
	    "ufNascimento" AS uf_nascimento,
	    "municipioNascimento" AS naturalidade,
	    COALESCE(escolaridade,'Não informada') AS escolaridade
    FROM
	    {{ref('raw__infos_extras')}} infos
    )
SELECT * FROM renamed