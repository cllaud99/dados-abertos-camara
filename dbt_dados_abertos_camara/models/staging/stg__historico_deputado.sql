WITH source AS (
    SELECT * FROM {{ source('dados_abertos', 'lz_historico_deputado') }}
),

renamed AS (
    SELECT
        id AS id_deputado,
        "siglaPartido" AS sigla_partido,
        "descricaoStatus" AS descricao_status,
        "idLegislatura" AS id_legislatura,
        CAST("dataHora" AS date) AS dt_evento
    FROM
        source
)

SELECT * FROM renamed
