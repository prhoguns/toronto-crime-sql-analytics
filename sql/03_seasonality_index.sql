-- Q3. Is crime seasonal? Index each calendar month against the annual monthly average (100 = average).
-- Technique: two-level aggregation, window AVG over the whole partition.
with monthly as (
    select
        mci_category,
        month(occurrence_date) as month_num,
        strftime(occurrence_date, '%b') as month_abbr,
        count(*) / count(distinct occurrence_year)::double as avg_incidents_per_month
    from incidents
    where occurrence_year between 2014 and 2024
    group by 1, 2, 3
)
select
    mci_category,
    month_num,
    month_abbr,
    round(avg_incidents_per_month) as avg_incidents,
    round(100 * avg_incidents_per_month / avg(avg_incidents_per_month) over (partition by mci_category)) as seasonality_index
from monthly
order by mci_category, month_num;
