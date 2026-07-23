-- Q5. Day-of-week x hour grid for assaults (dashboard heatmap input).
-- Technique: grouping on two dimensions, ordering weekdays correctly with a CASE.
select
    occurrence_dow as day_of_week,
    case occurrence_dow
        when 'Monday' then 1 when 'Tuesday' then 2 when 'Wednesday' then 3 when 'Thursday' then 4
        when 'Friday' then 5 when 'Saturday' then 6 when 'Sunday' then 7 end as dow_num,
    occurrence_hour,
    count(*) as assaults
from incidents
where mci_category = 'Assault' and occurrence_year >= 2014
group by 1, 2, 3
order by dow_num, occurrence_hour;
