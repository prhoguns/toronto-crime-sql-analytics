-- Q14. Do Neighbourhood Improvement Areas (the City's designated priority neighbourhoods) have higher crime rates?
-- Technique: aggregate to neighbourhood then to designation, population-weighted rate.
with per_hood as (
    select
        n.tsns_designation,
        n.neighbourhood_id,
        n.population_2021,
        n.median_income_2020,
        count(*) as incidents_2024
    from incidents i
    join neighbourhoods n using (neighbourhood_id)
    where occurrence_year = 2024
    group by 1, 2, 3, 4
)
select
    tsns_designation,
    count(*) as neighbourhoods,
    sum(population_2021) as population,
    sum(incidents_2024) as incidents_2024,
    round(1000.0 * sum(incidents_2024) / sum(population_2021), 1) as per_1000_residents,
    round(median(median_income_2020)) as median_of_median_income
from per_hood
group by 1
order by per_1000_residents desc;
