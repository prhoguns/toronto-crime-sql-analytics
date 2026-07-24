# Q6. Top 15 neighbourhoods by incidents in 2024, and how their rank moved since 2019.

```sql
-- Q6. Top 15 neighbourhoods by incidents in 2024, and how their rank moved since 2019.
-- Technique: RANK() in two CTEs joined together; negative "rank_change" means it got worse.
with r2019 as (
    select neighbourhood_id, count(*) as incidents_2019,
           rank() over (order by count(*) desc) as rank_2019
    from incidents where occurrence_year = 2019 and neighbourhood_id is not null
    group by 1
),
r2024 as (
    select neighbourhood_id, count(*) as incidents_2024,
           rank() over (order by count(*) desc) as rank_2024
    from incidents where occurrence_year = 2024 and neighbourhood_id is not null
    group by 1
)
select
    n.neighbourhood_name,
    r2024.incidents_2024,
    r2024.rank_2024,
    r2019.rank_2019,
    r2019.rank_2019 - r2024.rank_2024 as rank_change
from r2024
join r2019 using (neighbourhood_id)
join neighbourhoods n using (neighbourhood_id)
order by rank_2024
limit 15;
```

| neighbourhood_name | incidents_2024 | rank_2024 | rank_2019 | rank_change |
|:---|---:|---:|---:|---:|
| West Humber-Clairville | 1295 | 1 | 2 | 1 |
| Mimico-Queensway | 1023 | 2 | 26 | 24 |
| Downtown Yonge East | 885 | 3 | 3 | 0 |
| York University Heights | 865 | 4 | 6 | 2 |
| Moss Park | 836 | 5 | 1 | -4 |
| Yonge-Bay Corridor | 794 | 6 | 4 | -2 |
| Kensington-Chinatown | 773 | 7 | 5 | -2 |
| Annex | 767 | 8 | 9 | 1 |
| St Lawrence-East Bayfront-The Islands | 726 | 9 | 17 | 8 |
| Wellington Place | 695 | 10 | 7 | -3 |
| Etobicoke City Centre | 684 | 11 | 21 | 10 |
| Wexford/Maryvale | 671 | 12 | 14 | 2 |
| West Hill | 625 | 13 | 8 | -5 |
| Oakdale-Beverley Heights | 612 | 14 | 12 | -2 |
| Clairlea-Birchmount | 567 | 15 | 16 | 1 |

_15 rows._
