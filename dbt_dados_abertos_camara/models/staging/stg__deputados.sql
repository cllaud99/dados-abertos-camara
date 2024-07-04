WITH source AS (
    SELECT * FROM {{ source('dados_abertos', 'lz_deputados') }}
),
renamed AS (
  SELECT    
        deputados.id AS id_deputado,
        deputados.nome,
        deputados."siglaPartido" AS sigla_partido,
        deputados."siglaUf" AS uf,
        deputados."urlFoto" AS url_foto
    FROM source deputados
)
SELECT * 
FROM renamed