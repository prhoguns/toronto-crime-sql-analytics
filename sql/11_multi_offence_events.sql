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
