WITH source AS (
    SELECT * FROM {{ source('dados_abertos', 'lz_despesas') }}
),

renamed AS (
    SELECT
        cast(substring(file_name FROM '^[^_]+') AS int) AS id_deputado,
        "codTipoDocumento" AS cod_tipo_documento,
        "tipoDespesa" AS tipo_despesa,
        --"dataDocumento" AS dt_despesa,
        "valorLiquido" AS vlr_liquido,
        "valorDocumento" AS vlr_documento,
        "valorGlosa" AS vlr_glosa,
        cast(concat(ano, '-', mes, '-01') AS date) AS dt_despesa,
        coalesce(nullif("cnpjCpfFornecedor", ''), '-1') AS cnpj_fornecedor,
        upper("nomeFornecedor") AS nome_fornecedor
    FROM
        source
)

SELECT * FROM renamed
