WITH agregado_cnpj AS (
    SELECT
        cnpj_fornecedor,
        COUNT(*) AS qtd_referencias,
        SUM(vlr_liquido) AS total_liquido,
        SUM(vlr_glosa) AS total_glosa,
        SUM(vlr_documento) AS total_documento
    FROM
        {{ ref('int__despesas') }}
    GROUP BY
        cnpj_fornecedor
),

frequencia_nome AS (
    SELECT
        cnpj_fornecedor,
        nome_fornecedor,
        COUNT(*) AS qtd_referencias
    FROM
        {{ ref('int__despesas') }}
    GROUP BY
        cnpj_fornecedor, nome_fornecedor
),

most_frequent_name AS (
    SELECT
        cnpj_fornecedor,
        nome_fornecedor,
        ROW_NUMBER()
            OVER (
                PARTITION BY cnpj_fornecedor
                ORDER BY qtd_referencias DESC, nome_fornecedor ASC
            )
        AS rn
    FROM
        frequencia_nome
)

SELECT
    a.cnpj_fornecedor,
    mfn.nome_fornecedor
FROM
    agregado_cnpj a
INNER JOIN
    most_frequent_name mfn
    ON
        a.cnpj_fornecedor = mfn.cnpj_fornecedor
WHERE
    mfn.rn = 1
ORDER BY
    a.cnpj_fornecedor
