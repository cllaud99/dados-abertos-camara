WITH scd_updates AS (
    SELECT
        id_deputado,
        sigla_partido,
        descricao_status,
        dt_evento AS dt_inicio
    FROM
        {{ ref('stg__historico_deputado') }}
    WHERE
        id_legislatura = 57
        AND descricao_status ILIKE 'Alteração de partido'
),

dim_deputados AS (
    SELECT
        dep.id_deputado,
        dep.nome,
        dep.sigla_partido,
        dep.uf,
        dep.url_foto,
        info.sexo,
        info.idade,
        info.uf_nascimento,
        info.escolaridade,
        info.ordem_escolaridade,
        info.faixa_idade,
        info.situacao,
        info.condicao_eleitoral,
        COALESCE(scd.dt_inicio, '2000-01-01') AS dt_inicio,
        CONCAT(dep.id_deputado, '_', dep.sigla_partido) AS sk_deputado
    FROM
        {{ ref('stg__deputados') }} dep
    LEFT JOIN
        {{ ref('stg__infos_extras') }} info
        ON dep.id_deputado = info.id_deputado
    LEFT JOIN
        scd_updates scd
        ON
            dep.id_deputado = scd.id_deputado
            AND dep.sigla_partido = scd.sigla_partido
    ORDER BY scd.id_deputado ASC, dt_inicio ASC
),

tratamento_datas AS (
    SELECT
        *,
        COALESCE(
            LEAD(dt_inicio) OVER (PARTITION BY id_deputado ORDER BY dt_inicio),
            '2199-01-01'
        ) AS dt_fim,
        ROW_NUMBER()
            OVER (PARTITION BY id_deputado ORDER BY dt_inicio)
        AS versao,
        COALESCE(LEAD(dt_inicio)
            OVER (PARTITION BY id_deputado ORDER BY dt_inicio)
        IS null,
        false) AS status_atual
    FROM dim_deputados
)

SELECT * FROM tratamento_datas
