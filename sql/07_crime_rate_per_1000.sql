-- Q7. Raw counts favour big neighbourhoods. Which have the highest and lowest 2024 rate per 1,000 residents?
-- Technique: join to census population, UNION ALL of two ordered LIMITs.
with rates as (
    select
        n.neighbourhood_name,
        n.population_2021,
        count(*) as incidents_2024,
        round(1000.0 * count(*) / n.population_2021, 1) as per_1000
    from incidents i
    join neighbourhoods n using (neighbourhood_id)
    where i.occurrence_year = 2024
    group by 1, 2
)
(select 'highest' as bucket, * from rates order by per_1000 desc limit 10)
union all
(select 'lowest' as bucket, * from rates order by per_1000 asc limit 10)
order by bucket, per_1000 desc;
