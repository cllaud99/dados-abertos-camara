WITH fato_despesas AS (
    SELECT
        sd.id_deputado,
        sd.dt_despesa,
        sd.tipo_despesa,
        sd.cnpj_fornecedor,
        sd.vlr_liquido AS vlr_liquido,
        sd.vlr_documento AS vlr_documento,
        sd.vlr_glosa AS vlr_glosa,
        sd.cod_tipo_documento,
        td.cod_tipo_despesa,
        dd.sk_deputado AS sk_deputado
    FROM {{ ref('stg__despesas') }} sd
    LEFT JOIN
        {{ ref('stg__tipos_despesas') }} td ON td.tipo_despesa = sd.tipo_despesa
    LEFT JOIN
        {{ ref('dim__deputados_SCD2') }} dd ON dd.id_deputado = sd.id_deputado
                                        AND sd.dt_despesa >= dd.dt_inicio AND sd.dt_despesa < dd.dt_fim::date -- Convertendo para tipo date
)
SELECT
    id_deputado,
    dt_despesa,
    cnpj_fornecedor,
    vlr_liquido AS vlr_liquido,
    vlr_documento AS vlr_documento,
    vlr_glosa AS vlr_glosa,
    cod_tipo_despesa,
    sk_deputado
FROM
    fato_despesas
