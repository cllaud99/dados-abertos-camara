WITH fato_despesas AS (
    SELECT
        sd.id_deputado,
        sd.dt_despesa,
        sd.tipo_despesa,
        sd.cnpj_fornecedor,
        sd.vlr_liquido,
        sd.vlr_documento,
        sd.vlr_glosa,
        sd.cod_tipo_documento,
        td.cod_tipo_despesa,
        dd.sk_deputado
    FROM {{ ref('stg__despesas') }} sd
    LEFT JOIN
        {{ ref('int__tipos_despesas') }} td
        ON sd.tipo_despesa = td.tipo_despesa
    LEFT JOIN
        {{ ref('int__deputados_scd2') }} dd ON
        dd.id_deputado = sd.id_deputado
        -- Convertendo para tipo date
        AND sd.dt_despesa >= dd.dt_inicio AND sd.dt_despesa < dd.dt_fim::date
)

SELECT
    id_deputado,
    dt_despesa,
    cnpj_fornecedor,
    vlr_liquido,
    vlr_documento,
    vlr_glosa,
    cod_tipo_despesa,
    sk_deputado
FROM
    fato_despesas
