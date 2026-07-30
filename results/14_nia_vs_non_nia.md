# Q14. Do Neighbourhood Improvement Areas (the City's designated priority neighbourhoods) have higher crime rates?

```sql
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
```

| tsns_designation | neighbourhoods | population | incidents_2024 | per_1000_residents | median_of_median_income |
|:---|---:|---:|---:|---:|---:|
| Neighbourhood Improvement Area (formerly Downsview-Roding-CFB) | 2 | 39,390 | 962 | 24.4 | 34,200 |
| Neighbourhood Improvement Area | 29 | 510,400 | 9074 | 17.8 | 30,200 |
| Not an NIA or Emerging Neighbourhood | 115 | 1,950,690 | 32641 | 16.7 | 40,400 |
| Neighbourhood Improvement Area (formerly Woburn) | 2 | 53,665 | 678 | 12.6 | 28,300 |
| Emerging Neighbourhood | 10 | 207,145 | 2510 | 12.1 | 31,600 |

_5 rows._
