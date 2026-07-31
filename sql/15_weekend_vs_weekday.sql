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
