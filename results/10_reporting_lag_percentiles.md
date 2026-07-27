# Q10. How long after a crime is it reported? Percentiles of the lag, by category.

```sql
-- Q10. How long after a crime is it reported? Percentiles of the lag, by category.
-- Technique: QUANTILE_CONT for p50/p90/p99, plus share reported same day.
select
    mci_category,
    count(*) as incidents,
    round(100.0 * count(*) filter (where report_date = occurrence_date) / count(*), 1) as pct_same_day,
    quantile_cont(report_date - occurrence_date, 0.50) as p50_days,
    quantile_cont(report_date - occurrence_date, 0.90) as p90_days,
    quantile_cont(report_date - occurrence_date, 0.99) as p99_days,
    max(report_date - occurrence_date) as max_days
from incidents
where occurrence_year >= 2014
group by 1
order by p90_days desc;
```

| mci_category | incidents | pct_same_day | p50_days | p90_days | p99_days | max_days |
|:---|---:|---:|---:|---:|---:|---:|
| Theft Over | 15732 | 31 | 2 | 53 | 491.7 | 3,517 |
| Assault | 241292 | 76 | 0 | 6 | 756 | 4,231 |
| Break and Enter | 81453 | 62.1 | 0 | 5 | 87 | 2,485 |
| Auto Theft | 73682 | 44.5 | 1 | 3 | 71 | 3,653 |
| Robbery | 39070 | 86.8 | 0 | 1 | 31 | 2,350 |

_5 rows._
