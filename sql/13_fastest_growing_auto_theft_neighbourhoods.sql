-- Q13. Where did auto theft grow fastest between 2019 and 2023 (the peak)? Minimum 50 thefts in 2019 to avoid small-base noise.
-- Technique: conditional aggregation across two years + HAVING on a filtered count.
select
    n.neighbourhood_name,
    count(*) filter (where occurrence_year = 2019) as thefts_2019,
    count(*) filter (where occurrence_year = 2023) as thefts_2023,
    round(100.0 * (count(*) filter (where occurrence_year = 2023) - count(*) filter (where occurrence_year = 2019))
          / count(*) filter (where occurrence_year = 2019), 0) as growth_pct
from incidents i
join neighbourhoods n using (neighbourhood_id)
where mci_category = 'Auto Theft' and occurrence_year in (2019, 2023)
group by 1
having count(*) filter (where occurrence_year = 2019) >= 50
order by growth_pct desc
limit 15;
