# Q11. One police event can carry several offence rows. How common is that, and what does it mean for "counting crimes"?

```sql
-- Q11. One police event can carry several offence rows. How common is that, and what does it mean for "counting crimes"?
-- Technique: aggregate to event grain first, then aggregate the aggregate.
with per_event as (
    select event_id, count(*) as offence_rows, count(distinct mci_category) as categories
    from incidents
    where occurrence_year >= 2014
    group by 1
)
select
    offence_rows,
    count(*) as events,
    round(100.0 * count(*) / sum(count(*)) over (), 2) as pct_of_events,
    sum(offence_rows) as rows_contributed
from per_event
group by 1
order by 1;
```

| offence_rows | events | pct_of_events | rows_contributed |
|---:|---:|---:|---:|
| 1 | 347,895 | 88.5 | 347895 |
| 2 | 36,073 | 9.2 | 72146 |
| 3 | 6,635 | 1.7 | 19905 |
| 4 | 1,626 | 0.4 | 6504 |
| 5 | 489 | 0.1 | 2445 |
| 6 | 159 | 0.0 | 954 |
| 7 | 76 | 0.0 | 532 |
| 8 | 41 | 0.0 | 328 |
| 9 | 11 | 0 | 99 |
| 10 | 15 | 0 | 150 |
| 11 | 6 | 0 | 66 |
| 12 | 2 | 0 | 24 |
| 13 | 1 | 0 | 13 |
| 14 | 2 | 0 | 28 |
| 15 | 1 | 0 | 15 |
| 16 | 1 | 0 | 16 |
| 20 | 1 | 0 | 20 |
| 21 | 2 | 0 | 42 |
| 23 | 1 | 0 | 23 |
| 24 | 1 | 0 | 24 |

_20 rows._
