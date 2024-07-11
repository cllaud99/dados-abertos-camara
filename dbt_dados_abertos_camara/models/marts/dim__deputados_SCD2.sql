WITH dim_deputados AS (
    SELECT *
    FROM
        {{ ref('int__deputados_scd2') }}
)

SELECT * FROM dim_deputados
