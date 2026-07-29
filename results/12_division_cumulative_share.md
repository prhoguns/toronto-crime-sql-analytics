# Q12. Police divisions ranked by 2024 volume with running cumulative share (Pareto view).

```sql
-- Q12. Police divisions ranked by 2024 volume with running cumulative share (Pareto view).
-- Technique: SUM() OVER (ORDER BY ...) for a running total.
with by_div as (
    select division, count(*) as incidents
    from incidents
    where occurrence_year = 2024 and division <> 'NSA'
    group by 1
)
select
    division,
    incidents,
    round(100.0 * incidents / sum(incidents) over (), 1) as pct_share,
    round(100.0 * sum(incidents) over (order by incidents desc) / sum(incidents) over (), 1) as cumulative_pct
from by_div
order by incidents desc;
```

| division | incidents | pct_share | cumulative_pct |
|:---|---:|---:|---:|
| D22 | 3970 | 8.6 | 8.6 |
| D32 | 3840 | 8.3 | 17 |
| D51 | 3370 | 7.3 | 24.3 |
| D55 | 3294 | 7.2 | 31.4 |
| D31 | 3253 | 7.1 | 38.5 |
| D41 | 3215 | 7 | 45.5 |
| D23 | 3030 | 6.6 | 52.1 |
| D14 | 2986 | 6.5 | 58.6 |
| D43 | 2942 | 6.4 | 65 |
| D42 | 2863 | 6.2 | 71.2 |
| D53 | 2744 | 6 | 77.1 |
| D52 | 2625 | 5.7 | 82.8 |
| D33 | 2431 | 5.3 | 88.1 |
| D12 | 2002 | 4.3 | 92.5 |
| D11 | 1947 | 4.2 | 96.7 |
| D13 | 1521 | 3.3 | 100 |

_16 rows._
