-- Q6. Top 15 neighbourhoods by incidents in 2024, and how their rank moved since 2019.
-- Technique: RANK() in two CTEs joined together; negative "rank_change" means it got worse.
with r2019 as (
    select neighbourhood_id, count(*) as incidents_2019,
           rank() over (order by count(*) desc) as rank_2019
    from incidents where occurrence_year = 2019 and neighbourhood_id is not null
    group by 1
),
r2024 as (
    select neighbourhood_id, count(*) as incidents_2024,
           rank() over (order by count(*) desc) as rank_2024
    from incidents where occurrence_year = 2024 and neighbourhood_id is not null
    group by 1
)
select
    n.neighbourhood_name,
    r2024.incidents_2024,
    r2024.rank_2024,
    r2019.rank_2019,
    r2019.rank_2019 - r2024.rank_2024 as rank_change
from r2024
join r2019 using (neighbourhood_id)
join neighbourhoods n using (neighbourhood_id)
order by rank_2024
limit 15;
