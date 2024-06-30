with source as (
      select * from {{ source('dados_abertos', 'lz_deputados') }}
),
renamed as (
    select    
	deputados.id AS id_deputado,
	deputados.nome,
	deputados."siglaPartido" AS sigla_partido,
	deputados."siglaUf"  AS uf,
	deputados."urlFoto" AS url_foto
    from source deputados
)
select * from renamed