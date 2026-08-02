-- Q18. The five most common specific offences inside each category, with share of category.
-- Technique: ROW_NUMBER() top-N per partition combined with a windowed percentage.
with counts as (
    select mci_category, offence, count(*) as incidents
    from incidents
    where occurrence_year >= 2014
    group by 1, 2
),
ranked as (
    select
        *,
        row_number() over (partition by mci_category order by incidents desc) as rn,
        round(100.0 * incidents / sum(incidents) over (partition by mci_category), 1) as pct_of_category
    from counts
)
select mci_category, rn as rank, offence, incidents, pct_of_category
from ranked
where rn <= 5
order by mci_category, rn;
