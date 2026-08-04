# Q20. Before trusting any of the above: what is wrong with the data?

```sql
-- Q20. Before trusting any of the above: what is wrong with the data?
-- Technique: one-row profile using FILTER clauses; the kind of query to run first on any new dataset.
select
    count(*)                                                                    as total_rows,
    count(distinct event_id)                                                    as distinct_events,
    count(*) filter (where neighbourhood_id is null)                            as rows_no_neighbourhood,
    round(100.0 * count(*) filter (where neighbourhood_id is null) / count(*), 2) as pct_no_neighbourhood,
    count(*) filter (where longitude = 0 or latitude = 0 or longitude is null)  as rows_no_coordinates,
    count(*) filter (where occurrence_date < '2014-01-01')                      as occurred_before_2014,
    count(*) filter (where occurrence_date > report_date)                       as occurred_after_report,
    min(occurrence_date)                                                        as earliest_occurrence,
    max(report_date)                                                            as latest_report
from incidents;
```

| total_rows | distinct_events | rows_no_neighbourhood | pct_no_neighbourhood | rows_no_coordinates | occurred_before_2014 | occurred_after_report | earliest_occurrence | latest_report |
|---:|---:|---:|---:|---:|---:|---:|:---|:---|
| 452949 | 394,433 | 7027 | 1.6 | 6680 | 1,720 | 0 | 1964-09-01 | 2025-09-30 |

_1 rows._
