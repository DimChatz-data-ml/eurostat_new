with yearly_avg as(
    select country,year,round(avg(housing_wage_ratio),2) as avg_ratio
    from {{ref('marts_metrics')}}
    group by country,year
),

ranked as(
    select country,year,avg_ratio,
    rank() over(partition by year order by avg_ratio desc nulls last) as  affordability_rank
    from yearly_avg
    where avg_ratio is not null
)
select * from ranked