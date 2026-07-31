# Q15. Per-day rate on weekends vs weekdays, by category. (Normalised: 2 weekend days vs 5 weekdays.)

```sql
-- Q15. Per-day rate on weekends vs weekdays, by category. (Normalised: 2 weekend days vs 5 weekdays.)
-- Technique: CASE bucketing and dividing counts by the number of days in each bucket.
with tagged as (
    select
        mci_category,
        case when occurrence_dow in ('Saturday', 'Sunday') then 'weekend' else 'weekday' end as day_type,
        occurrence_date
    from incidents
    where occurrence_year between 2014 and 2024
)
select
    mci_category,
    day_type,
    count(*) as incidents,
    count(distinct occurrence_date) as days_observed,
    round(count(*) * 1.0 / count(distinct occurrence_date), 1) as incidents_per_day
from tagged
group by 1, 2
order by mci_category, day_type;
```

| mci_category | day_type | incidents | days_observed | incidents_per_day |
|:---|:---|---:|---:|---:|
| Assault | weekday | 154045 | 2,870 | 53.7 |
| Assault | weekend | 69548 | 1,148 | 60.6 |
| Auto Theft | weekday | 51005 | 2,870 | 17.8 |
| Auto Theft | weekend | 17567 | 1,148 | 15.3 |
| Break and Enter | weekday | 56729 | 2,870 | 19.8 |
| Break and Enter | weekend | 20275 | 1,148 | 17.7 |
| Robbery | weekday | 26633 | 2,856 | 9.3 |
| Robbery | weekend | 10406 | 1,145 | 9.1 |
| Theft Over | weekday | 10871 | 2,763 | 3.9 |
| Theft Over | weekend | 3462 | 1,062 | 3.3 |

_10 rows._
