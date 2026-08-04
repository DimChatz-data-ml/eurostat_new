SELECT
    "Time frequency" AS time_frequency,
    "Unit of measure" AS unit_of_measure,
    "Geopolitical entity (reporting)" AS country,
    "Time" AS year,
    value AS gross_wage_eur
FROM {{ source('raw', 'raw_wages') }}
