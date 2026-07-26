-- Q9. Where does each type of crime happen? Share of incidents by premises type within category.
-- Technique: SUM() OVER (PARTITION BY) to compute percentage of group total.
select
    mci_category,
    premises_type,
    count(*) as incidents,
    round(100.0 * count(*) / sum(count(*)) over (partition by mci_category), 1) as pct_of_category
from incidents
where occurrence_year >= 2020
group by 1, 2
order by mci_category, incidents desc;
