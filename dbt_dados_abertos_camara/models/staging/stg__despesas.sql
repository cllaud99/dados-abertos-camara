WITH renamed AS
(
SELECT
	substring(file_name FROM '^[^_]+') AS id_deputado,
	"codTipoDocumento" AS cod_tipo_despesa,
	"tipoDespesa" AS tipo_despesa,
	"dataDocumento" AS dt_despesa,
	COALESCE(NULLIF("cnpjCpfFornecedor", ''), '-1') AS cnpj_fornecedor,
	UPPER("nomeFornecedor") AS nome_fornecedor,
	"valorLiquido" AS vlr_liquido,
	"valorDocumento" AS vlr_documento,
	"valorGlosa" AS vlr_glosa
FROM
	{{ref('raw__despesas')}} rd
)
SELECT * FROM renamed