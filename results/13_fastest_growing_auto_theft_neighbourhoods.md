# Q13. Where did auto theft grow fastest between 2019 and 2023 (the peak)? Minimum 50 thefts in 2019 to avoid small-base noise.

```sql
-- Q13. Where did auto theft grow fastest between 2019 and 2023 (the peak)? Minimum 50 thefts in 2019 to avoid small-base noise.
-- Technique: conditional aggregation across two years + HAVING on a filtered count.
select
    n.neighbourhood_name,
    count(*) filter (where occurrence_year = 2019) as thefts_2019,
    count(*) filter (where occurrence_year = 2023) as thefts_2023,
    round(100.0 * (count(*) filter (where occurrence_year = 2023) - count(*) filter (where occurrence_year = 2019))
          / count(*) filter (where occurrence_year = 2019), 0) as growth_pct
from incidents i
join neighbourhoods n using (neighbourhood_id)
where mci_category = 'Auto Theft' and occurrence_year in (2019, 2023)
group by 1
having count(*) filter (where occurrence_year = 2019) >= 50
order by growth_pct desc
limit 15;
```

| neighbourhood_name | thefts_2019 | thefts_2023 | growth_pct |
|:---|---:|---:|---:|
| Bedford Park-Nortown | 63 | 235 | 273 |
| Milliken | 85 | 316 | 272 |
| Newtonbrook West | 61 | 220 | 261 |
| Yorkdale-Glen Park | 63 | 206 | 227 |
| Islington | 57 | 172 | 202 |
| Morningside Heights | 55 | 158 | 187 |
| Etobicoke City Centre | 117 | 301 | 157 |
| Agincourt South-Malvern West | 56 | 130 | 132 |
| Wexford/Maryvale | 98 | 215 | 119 |
| Humbermede | 67 | 125 | 87 |
| Oakdale-Beverley Heights | 90 | 166 | 84 |
| York University Heights | 148 | 267 | 80 |
| Clairlea-Birchmount | 70 | 122 | 74 |
| West Humber-Clairville | 490 | 835 | 70 |
| Dorset Park | 62 | 103 | 66 |

_15 rows._
