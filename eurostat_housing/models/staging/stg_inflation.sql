SELECT
    "Time frequency" AS time_frequency,
    "Unit of measure" AS unit_of_measure,
    "Classification of individual consumption by purpose (COICOP) - " as coicop_category,
    "Geopolitical entity (reporting)" AS country,
    "Time" AS year,
    value AS inflation_rate
FROM {{ source('raw', 'raw_inflation') }}