-- Q4. What are the three peak hours for each category?
-- Technique: ROW_NUMBER() to take top-N per group.
with by_hour as (
    select mci_category, occurrence_hour, count(*) as incidents
    from incidents
    where occurrence_year >= 2014
    group by 1, 2
),
ranked as (
    select *, row_number() over (partition by mci_category order by incidents desc) as rn
    from by_hour
)
select mci_category, occurrence_hour, incidents, rn as rank
from ranked
where rn <= 3
order by mci_category, rn;
