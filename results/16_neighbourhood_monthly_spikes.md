# Q16. Anomaly detection in SQL: months where a neighbourhood's incidents were > 3 standard deviations above its own mean.

```sql
-- Q16. Anomaly detection in SQL: months where a neighbourhood's incidents were > 3 standard deviations above its own mean.
-- Technique: per-partition AVG and STDDEV windows to compute a z-score.
with monthly as (
    select neighbourhood_id, date_trunc('month', occurrence_date)::date as month, count(*) as incidents
    from incidents
    where occurrence_year between 2014 and 2025 and neighbourhood_id is not null
    group by 1, 2
),
scored as (
    select
        *,
        avg(incidents) over (partition by neighbourhood_id) as mean_incidents,
        stddev_samp(incidents) over (partition by neighbourhood_id) as sd_incidents
    from monthly
)
select
    n.neighbourhood_name,
    s.month,
    s.incidents,
    round(s.mean_incidents, 1) as neighbourhood_mean,
    round((s.incidents - s.mean_incidents) / nullif(s.sd_incidents, 0), 2) as z_score
from scored s
join neighbourhoods n using (neighbourhood_id)
where (s.incidents - s.mean_incidents) / nullif(s.sd_incidents, 0) > 3
order by z_score desc
limit 20;
```

| neighbourhood_name | month | incidents | neighbourhood_mean | z_score |
|:---|:---|---:|---:|---:|
| Beechborough-Greenbrook | 2024-09-01 | 36 | 9.4 | 5.8 |
| Corso Italia-Davenport | 2023-08-01 | 44 | 14.9 | 5.0 |
| Edenbridge-Humber Valley | 2023-10-01 | 40 | 10.8 | 5.0 |
| Lambton Baby Point | 2022-12-01 | 20 | 5 | 5.0 |
| Highland Creek | 2023-12-01 | 33 | 10.1 | 4.7 |
| Etobicoke City Centre | 2023-08-01 | 104 | 38.1 | 4.6 |
| Bridle Path-Sunnybrook-York Mills | 2023-05-01 | 35 | 9.9 | 4.6 |
| Steeles | 2019-10-01 | 30 | 11 | 4.5 |
| Humber Heights-Westmount | 2024-07-01 | 22 | 7.4 | 4.4 |
| Forest Hill South | 2023-05-01 | 32 | 9.2 | 4.3 |
| Fort York-Liberty Village | 2024-08-01 | 49 | 17.6 | 4.2 |
| Bendale-Glen Andrew | 2023-06-01 | 63 | 27.2 | 4.2 |
| Tam O'Shanter-Sullivan | 2023-07-01 | 47 | 20.2 | 4.2 |
| Long Branch | 2022-06-01 | 30 | 11.3 | 4.2 |
| Markland Wood | 2024-11-01 | 22 | 7.1 | 4.1 |
| Broadview North | 2024-04-01 | 24 | 8.1 | 4.1 |
| Forest Hill South | 2023-08-01 | 31 | 9.2 | 4.1 |
| Lansing-Westgate | 2023-11-01 | 40 | 14.9 | 4.0 |
| Bridle Path-Sunnybrook-York Mills | 2023-10-01 | 32 | 9.9 | 4.0 |
| Leaside-Bennington | 2021-05-01 | 32 | 11 | 4.0 |

_20 rows._
