select  COALESCE(w.country, i.country,h.country) AS country,
        COALESCE(w.year,i.year,left(h.year,4)) as year,
        w.time_frequency,w.unit_of_measure as wage_unit,
        i.unit_of_measure as inflation_unit,
        w.gross_wage_eur,i.coicop_category,
        i.inflation_rate,
        h.purchase_category,
        h.unit_of_measure AS housing_unit,
        h.time_frequency AS housing_frequency,
        h.house_price_index
from {{ref('stg_wages')}} w
full join {{ref('stg_inflation')}} i
on w.country=i.country and w.year=i.year 
full join {{ref('stg_housing')}} h
on coalesce(w.country,i.country)=h.country and  coalesce(w.year,i.year)=left(h.year,4)