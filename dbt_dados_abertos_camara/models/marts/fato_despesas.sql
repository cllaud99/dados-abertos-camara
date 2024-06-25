WITH fato_despesas AS
(
SELECT
	id_deputado,
	date_trunc('month',
	dt_despesa) AS mes_ano_despesa,
	cnpj_fornecedor,
	SUM(vlr_liquido) AS vlr_liquido,
	SUM(vlr_documento) AS vlr_documento,
	SUM(vlr_glosa) AS vlr_glosa,
	COUNT(1) AS qtd_linhas
FROM
	{{ref('stg__despesas')}}  sd
GROUP BY
	id_deputado,
	date_trunc('month',
	dt_despesa),
	cnpj_fornecedor
)
SELECT
	*
FROM
	fato_despesas