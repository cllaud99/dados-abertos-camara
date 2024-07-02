-- This is your dbt model file (dim_data.sql)

-- Define the model using Jinja and SQL
WITH date_sequence AS (
    SELECT '2018-01-01'::DATE + SEQUENCE.DAY AS datum
    FROM GENERATE_SERIES(0, 3650) AS SEQUENCE (DAY)
    GROUP BY SEQUENCE.DAY
)

SELECT
    TO_CHAR(datum, 'yyyymmdd')::INT AS id_dim_data,
    datum AS data_real,
    CASE
        WHEN EXTRACT(ISODOW FROM datum) = 1 THEN 'Segunda-feira'
        WHEN EXTRACT(ISODOW FROM datum) = 2 THEN 'Terça-feira'
        WHEN EXTRACT(ISODOW FROM datum) = 3 THEN 'Quarta-feira'
        WHEN EXTRACT(ISODOW FROM datum) = 4 THEN 'Quinta-feira'
        WHEN EXTRACT(ISODOW FROM datum) = 5 THEN 'Sexta-feira'
        WHEN EXTRACT(ISODOW FROM datum) = 6 THEN 'Sábado'
        WHEN EXTRACT(ISODOW FROM datum) = 7 THEN 'Domingo'
    END AS nome_dia,
    EXTRACT(ISODOW FROM datum) AS dia_da_semana,
    EXTRACT(DAY FROM datum) AS dia_do_mes,
    EXTRACT(DOY FROM datum) AS dia_do_ano,
    EXTRACT(MONTH FROM datum) AS mes_real,
    CASE
        WHEN EXTRACT(MONTH FROM datum) = 1 THEN 'Janeiro'
        WHEN EXTRACT(MONTH FROM datum) = 2 THEN 'Fevereiro'
        WHEN EXTRACT(MONTH FROM datum) = 3 THEN 'Março'
        WHEN EXTRACT(MONTH FROM datum) = 4 THEN 'Abril'
        WHEN EXTRACT(MONTH FROM datum) = 5 THEN 'Maio'
        WHEN EXTRACT(MONTH FROM datum) = 6 THEN 'Junho'
        WHEN EXTRACT(MONTH FROM datum) = 7 THEN 'Julho'
        WHEN EXTRACT(MONTH FROM datum) = 8 THEN 'Agosto'
        WHEN EXTRACT(MONTH FROM datum) = 9 THEN 'Setembro'
        WHEN EXTRACT(MONTH FROM datum) = 10 THEN 'Outubro'
        WHEN EXTRACT(MONTH FROM datum) = 11 THEN 'Novembro'
        WHEN EXTRACT(MONTH FROM datum) = 12 THEN 'Dezembro'
    END AS nome_mes,
    EXTRACT(QUARTER FROM datum) AS trimestre_real,
    CASE
        WHEN EXTRACT(QUARTER FROM datum) = 1 THEN '1°'
        WHEN EXTRACT(QUARTER FROM datum) = 2 THEN '2°'
        WHEN EXTRACT(QUARTER FROM datum) = 3 THEN '3°'
        WHEN EXTRACT(QUARTER FROM datum) = 4 THEN '4°'
    END AS nome_trimestre,
    EXTRACT(YEAR FROM datum) AS ano_real,
    CASE
        WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN TRUE
        ELSE FALSE
    END AS indicador_final_de_semana

FROM date_sequence
