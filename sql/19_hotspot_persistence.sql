-- Q19. Are hotspots persistent? Of the top-20 neighbourhoods in 2014, how many are still top-20 in 2024?
-- Technique: two ranked CTEs, FULL OUTER JOIN, COALESCE to classify.
with top14 as (
    select neighbourhood_id, count(*) as incidents_2014
    from incidents where occurrence_year = 2014 and neighbourhood_id is not null
    group by 1 order by 2 desc limit 20
),
top24 as (
    select neighbourhood_id, count(*) as incidents_2024
    from incidents where occurrence_year = 2024 and neighbourhood_id is not null
    group by 1 order by 2 desc limit 20
)
select
    n.neighbourhood_name,
    top14.incidents_2014,
    top24.incidents_2024,
    case
        when top14.neighbourhood_id is not null and top24.neighbourhood_id is not null then 'persistent hotspot'
        when top14.neighbourhood_id is not null then 'dropped out of top 20'
        else 'new to top 20'
    end as status
from top14
full outer join top24 using (neighbourhood_id)
join neighbourhoods n using (neighbourhood_id)
order by status, coalesce(top24.incidents_2024, 0) desc;
