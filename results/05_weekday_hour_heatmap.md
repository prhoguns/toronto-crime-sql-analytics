# Q5. Day-of-week x hour grid for assaults (dashboard heatmap input).

```sql
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
```

| day_of_week | dow_num | occurrence_hour | assaults |
|:---|---:|---:|---:|
| Monday | 1 | 0 | 2,339 |
| Monday | 1 | 1 | 1,049 |
| Monday | 1 | 2 | 978 |
| Monday | 1 | 3 | 753 |
| Monday | 1 | 4 | 513 |
| Monday | 1 | 5 | 407 |
| Monday | 1 | 6 | 447 |
| Monday | 1 | 7 | 688 |
| Monday | 1 | 8 | 1,043 |
| Monday | 1 | 9 | 1,237 |
| Monday | 1 | 10 | 1,288 |
| Monday | 1 | 11 | 1,446 |
| Monday | 1 | 12 | 2,146 |
| Monday | 1 | 13 | 1,500 |
| Monday | 1 | 14 | 1,585 |
| Monday | 1 | 15 | 1,948 |
| Monday | 1 | 16 | 1,837 |
| Monday | 1 | 17 | 1,677 |
| Monday | 1 | 18 | 1,922 |
| Monday | 1 | 19 | 1,778 |
| Monday | 1 | 20 | 1,831 |
| Monday | 1 | 21 | 1,695 |
| Monday | 1 | 22 | 1,565 |
| Monday | 1 | 23 | 1,401 |
| Tuesday | 2 | 0 | 1,991 |
| Tuesday | 2 | 1 | 909 |
| Tuesday | 2 | 2 | 774 |
| Tuesday | 2 | 3 | 549 |
| Tuesday | 2 | 4 | 398 |
| Tuesday | 2 | 5 | 362 |
| Tuesday | 2 | 6 | 421 |
| Tuesday | 2 | 7 | 610 |
| Tuesday | 2 | 8 | 1,064 |
| Tuesday | 2 | 9 | 1,241 |
| Tuesday | 2 | 10 | 1,351 |
| Tuesday | 2 | 11 | 1,457 |
| Tuesday | 2 | 12 | 2,139 |
| Tuesday | 2 | 13 | 1,524 |
| Tuesday | 2 | 14 | 1,657 |
| Tuesday | 2 | 15 | 2,019 |
| Tuesday | 2 | 16 | 1,703 |
| Tuesday | 2 | 17 | 1,851 |
| Tuesday | 2 | 18 | 1,770 |
| Tuesday | 2 | 19 | 1,780 |
| Tuesday | 2 | 20 | 1,850 |
| Tuesday | 2 | 21 | 1,704 |
| Tuesday | 2 | 22 | 1,621 |
| Tuesday | 2 | 23 | 1,406 |
| Wednesday | 3 | 0 | 2,192 |
| Wednesday | 3 | 1 | 953 |
| Wednesday | 3 | 2 | 839 |
| Wednesday | 3 | 3 | 566 |
| Wednesday | 3 | 4 | 426 |
| Wednesday | 3 | 5 | 398 |
| Wednesday | 3 | 6 | 428 |
| Wednesday | 3 | 7 | 692 |
| Wednesday | 3 | 8 | 1,098 |
| Wednesday | 3 | 9 | 1,294 |
| Wednesday | 3 | 10 | 1,439 |
| Wednesday | 3 | 11 | 1,455 |

_168 rows; showing first 60._
