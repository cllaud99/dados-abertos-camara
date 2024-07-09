WITH fato_despesas AS (
    SELECT
        sd.id_deputado,
        sd.dt_despesa,
        sd.tipo_despesa,
        sd.cnpj_fornecedor,
        sd.vlr_liquido AS vlr_liquido,
        sd.vlr_documento AS vlr_documento,
        sd.vlr_glosa AS vlr_glosa,
        sd.cod_tipo_despesa,
        td.id_tipo_despesa
    FROM {{ ref('stg__despesas') }} sd
    LEFT JOIN
        {{ref('stg__tipos_despesas')}} td ON
        td.tipo_despesa = sd.tipo_despesa
)
SELECT
        id_deputado,
        dt_despesa,
        cnpj_fornecedor,
        vlr_liquido AS vlr_liquido,
        vlr_documento AS vlr_documento,
        vlr_glosa AS vlr_glosa,
        cod_tipo_despesa,
        id_tipo_despesa
FROM
    fato_despesas
