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
