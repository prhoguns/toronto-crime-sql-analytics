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
