# Q19. Are hotspots persistent? Of the top-20 neighbourhoods in 2014, how many are still top-20 in 2024?

```sql
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
```

| neighbourhood_name | incidents_2014 | incidents_2024 | status |
|:---|---:|---:|:---|
| Black Creek | 353 |  | dropped out of top 20 |
| Kennedy Park | 361 |  | dropped out of top 20 |
| Eglinton East | 325 |  | dropped out of top 20 |
| Mimico-Queensway |  | 1023 | new to top 20 |
| St Lawrence-East Bayfront-The Islands |  | 726 | new to top 20 |
| Yorkdale-Glen Park |  | 514 | new to top 20 |
| West Humber-Clairville | 885 | 1295 | persistent hotspot |
| Downtown Yonge East | 567 | 885 | persistent hotspot |
| York University Heights | 586 | 865 | persistent hotspot |
| Moss Park | 658 | 836 | persistent hotspot |
| Yonge-Bay Corridor | 581 | 794 | persistent hotspot |
| Kensington-Chinatown | 573 | 773 | persistent hotspot |
| Annex | 476 | 767 | persistent hotspot |
| Wellington Place | 562 | 695 | persistent hotspot |
| Etobicoke City Centre | 326 | 684 | persistent hotspot |
| Wexford/Maryvale | 457 | 671 | persistent hotspot |
| West Hill | 530 | 625 | persistent hotspot |
| Oakdale-Beverley Heights | 389 | 612 | persistent hotspot |
| Clairlea-Birchmount | 478 | 567 | persistent hotspot |
| South Riverdale | 388 | 546 | persistent hotspot |
| Glenfield-Jane Heights | 414 | 533 | persistent hotspot |
| Church-Wellesley | 347 | 506 | persistent hotspot |
| Mount Olive-Silverstone-Jamestown | 406 | 497 | persistent hotspot |

_23 rows._
