with wages_2015 as(
    select DISTINCT country,gross_wage_eur
    from {{ref('marts_core')}}
    where year='2015'
),

base as(
select 
mc.country,
mc.year,
mc.time_frequency,
mc.wage_unit,
mc.inflation_unit,
mc.gross_wage_eur,
mc.coicop_category,
mc.inflation_rate,
mc.purchase_category,
mc.housing_unit,
mc.housing_frequency,
mc.house_price_index,
wages_2015.gross_wage_eur AS wage_2015,
round((mc.gross_wage_eur::numeric/wages_2015.gross_wage_eur)*100,2) as wage_2015_index
from {{ref('marts_core')}} mc
left join wages_2015
on mc.country=wages_2015.country
)
SELECT 
    *,
ROUND((house_price_index / NULLIF(wage_2015_index, 0))::numeric, 2) AS housing_wage_ratio
FROM base