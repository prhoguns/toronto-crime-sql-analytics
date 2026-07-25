# Q7. Raw counts favour big neighbourhoods. Which have the highest and lowest 2024 rate per 1,000 residents?

```sql
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
```

| bucket | neighbourhood_name | population_2021 | incidents_2024 | per_1000 |
|:---|:---|---:|---:|---:|
| highest | Yonge-Bay Corridor | 12,645 | 794 | 62.8 |
| highest | Mimico-Queensway | 17,045 | 1023 | 60 |
| highest | Downtown Yonge East | 17,700 | 885 | 50 |
| highest | Kensington-Chinatown | 18,120 | 773 | 42.7 |
| highest | Moss Park | 21,490 | 836 | 38.9 |
| highest | West Humber-Clairville | 33,300 | 1295 | 38.9 |
| highest | University | 6,435 | 235 | 36.5 |
| highest | Yorkdale-Glen Park | 16,625 | 514 | 30.9 |
| highest | York University Heights | 28,255 | 865 | 30.6 |
| highest | Etobicoke City Centre | 23,600 | 684 | 29 |
| lowest | Humber Bay Shores | 22,605 | 197 | 8.7 |
| lowest | Danforth-East York | 17,065 | 147 | 8.6 |
| lowest | Leaside-Bennington | 16,535 | 140 | 8.5 |
| lowest | Forest Hill North | 12,290 | 103 | 8.4 |
| lowest | Lambton Baby Point | 7,965 | 64 | 8 |
| lowest | Guildwood | 9,680 | 76 | 7.9 |
| lowest | Centennial Scarborough | 13,380 | 105 | 7.8 |
| lowest | Avondale | 13,790 | 105 | 7.6 |
| lowest | Pleasant View | 15,220 | 114 | 7.5 |
| lowest | Steeles | 22,765 | 131 | 5.8 |

_20 rows._
