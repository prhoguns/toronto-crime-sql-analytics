# Q4. What are the three peak hours for each category?

```sql
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
```

| mci_category | occurrence_hour | incidents | rank |
|:---|---:|---:|---:|
| Assault | 0 | 16826 | 1 |
| Assault | 12 | 14144 | 2 |
| Assault | 15 | 13362 | 3 |
| Auto Theft | 22 | 6484 | 1 |
| Auto Theft | 21 | 5815 | 2 |
| Auto Theft | 23 | 5762 | 3 |
| Break and Enter | 0 | 6356 | 1 |
| Break and Enter | 3 | 4776 | 2 |
| Break and Enter | 4 | 4739 | 3 |
| Robbery | 20 | 2732 | 1 |
| Robbery | 21 | 2729 | 2 |
| Robbery | 19 | 2512 | 3 |
| Theft Over | 0 | 1599 | 1 |
| Theft Over | 12 | 1491 | 2 |
| Theft Over | 17 | 972 | 3 |

_15 rows._
