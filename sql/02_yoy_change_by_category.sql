-- Q2. Year-over-year % change per category. Which category had the biggest single-year jump?
-- Technique: LAG() window over a partition, NULLIF to avoid divide-by-zero.
with yearly as (
    select mci_category, occurrence_year as year, count(*) as incidents
    from incidents
    where occurrence_year between 2014 and 2024   -- 2025 is a partial year
    group by 1, 2
)
select
    mci_category,
    year,
    incidents,
    lag(incidents) over (partition by mci_category order by year)                  as prev_year,
    round(100.0 * (incidents - lag(incidents) over (partition by mci_category order by year))
          / nullif(lag(incidents) over (partition by mci_category order by year), 0), 1) as yoy_pct
from yearly
order by mci_category, year;
