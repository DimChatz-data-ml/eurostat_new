SELECT
    "Time frequency" AS time_frequency,
    "Purchases" AS purchase_category,
    "Unit of measure" AS unit_of_measure,
    "Geopolitical entity (reporting)" AS country,
    "Time" AS year,
    value AS house_price_index
FROM {{ source('raw', 'raw_housing') }}
WHERE "Purchases" = 'Total'
 AND "Unit of measure" = 'Quarterly index, 2015=100'