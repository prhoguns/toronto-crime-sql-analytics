# Q18. The five most common specific offences inside each category, with share of category.

```sql
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
```

| mci_category | rank | offence | incidents | pct_of_category |
|:---|---:|:---|---:|---:|
| Assault | 1 | Assault | 165560 | 68.6 |
| Assault | 2 | Assault With Weapon | 41378 | 17.1 |
| Assault | 3 | Assault Bodily Harm | 10361 | 4.3 |
| Assault | 4 | Assault Peace Officer | 7858 | 3.3 |
| Assault | 5 | Assault - Resist/ Prevent Seiz | 3802 | 1.6 |
| Auto Theft | 1 | Theft Of Motor Vehicle | 73682 | 100 |
| Break and Enter | 1 | B&E | 68243 | 83.8 |
| Break and Enter | 2 | B&E W'Intent | 10349 | 12.7 |
| Break and Enter | 3 | Unlawfully In Dwelling-House | 2697 | 3.3 |
| Break and Enter | 4 | B&E Out | 127 | 0.2 |
| Break and Enter | 5 | B&E - To Steal Firearm | 23 | 0 |
| Robbery | 1 | Robbery - Mugging | 9712 | 24.9 |
| Robbery | 2 | Robbery With Weapon | 7563 | 19.4 |
| Robbery | 3 | Robbery - Other | 6582 | 16.8 |
| Robbery | 4 | Robbery - Business | 5927 | 15.2 |
| Robbery | 5 | Robbery - Swarming | 2803 | 7.2 |
| Theft Over | 1 | Theft Over | 8847 | 56.2 |
| Theft Over | 2 | Theft From Motor Vehicle Over | 3790 | 24.1 |
| Theft Over | 3 | Theft From Mail / Bag / Key | 1676 | 10.7 |
| Theft Over | 4 | Theft Over - Shoplifting | 784 | 5 |
| Theft Over | 5 | Theft Over - Distraction | 372 | 2.4 |

_21 rows._
