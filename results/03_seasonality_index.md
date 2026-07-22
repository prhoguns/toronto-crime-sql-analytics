# Q3. Is crime seasonal? Index each calendar month against the annual monthly average (100 = average).

```sql
-- Q3. Is crime seasonal? Index each calendar month against the annual monthly average (100 = average).
-- Technique: two-level aggregation, window AVG over the whole partition.
with monthly as (
    select
        mci_category,
        month(occurrence_date) as month_num,
        strftime(occurrence_date, '%b') as month_abbr,
        count(*) / count(distinct occurrence_year)::double as avg_incidents_per_month
    from incidents
    where occurrence_year between 2014 and 2024
    group by 1, 2, 3
)
select
    mci_category,
    month_num,
    month_abbr,
    round(avg_incidents_per_month) as avg_incidents,
    round(100 * avg_incidents_per_month / avg(avg_incidents_per_month) over (partition by mci_category)) as seasonality_index
from monthly
order by mci_category, month_num;
```

| mci_category | month_num | month_abbr | avg_incidents | seasonality_index |
|:---|---:|:---|---:|---:|
| Assault | 1 | Jan | 1607 | 95 |
| Assault | 2 | Feb | 1439 | 85 |
| Assault | 3 | Mar | 1577 | 93 |
| Assault | 4 | Apr | 1585 | 94 |
| Assault | 5 | May | 1806 | 107 |
| Assault | 6 | Jun | 1822 | 108 |
| Assault | 7 | Jul | 1856 | 110 |
| Assault | 8 | Aug | 1812 | 107 |
| Assault | 9 | Sep | 1771 | 105 |
| Assault | 10 | Oct | 1755 | 104 |
| Assault | 11 | Nov | 1669 | 99 |
| Assault | 12 | Dec | 1629 | 96 |
| Auto Theft | 1 | Jan | 492 | 95 |
| Auto Theft | 2 | Feb | 439 | 84 |
| Auto Theft | 3 | Mar | 513 | 99 |
| Auto Theft | 4 | Apr | 496 | 96 |
| Auto Theft | 5 | May | 521 | 100 |
| Auto Theft | 6 | Jun | 522 | 100 |
| Auto Theft | 7 | Jul | 518 | 100 |
| Auto Theft | 8 | Aug | 528 | 102 |
| Auto Theft | 9 | Sep | 539 | 104 |
| Auto Theft | 10 | Oct | 576 | 111 |
| Auto Theft | 11 | Nov | 573 | 110 |
| Auto Theft | 12 | Dec | 516 | 99 |
| Break and Enter | 1 | Jan | 598 | 102 |
| Break and Enter | 2 | Feb | 517 | 89 |
| Break and Enter | 3 | Mar | 567 | 97 |
| Break and Enter | 4 | Apr | 552 | 95 |
| Break and Enter | 5 | May | 573 | 98 |
| Break and Enter | 6 | Jun | 562 | 96 |
| Break and Enter | 7 | Jul | 589 | 101 |
| Break and Enter | 8 | Aug | 617 | 106 |
| Break and Enter | 9 | Sep | 578 | 99 |
| Break and Enter | 10 | Oct | 618 | 106 |
| Break and Enter | 11 | Nov | 620 | 106 |
| Break and Enter | 12 | Dec | 611 | 105 |
| Robbery | 1 | Jan | 290 | 103 |
| Robbery | 2 | Feb | 262 | 94 |
| Robbery | 3 | Mar | 272 | 97 |
| Robbery | 4 | Apr | 260 | 93 |
| Robbery | 5 | May | 279 | 99 |
| Robbery | 6 | Jun | 266 | 95 |
| Robbery | 7 | Jul | 282 | 101 |
| Robbery | 8 | Aug | 292 | 104 |
| Robbery | 9 | Sep | 287 | 102 |
| Robbery | 10 | Oct | 312 | 111 |
| Robbery | 11 | Nov | 299 | 107 |
| Robbery | 12 | Dec | 265 | 95 |
| Theft Over | 1 | Jan | 95 | 88 |
| Theft Over | 2 | Feb | 91 | 84 |
| Theft Over | 3 | Mar | 98 | 90 |
| Theft Over | 4 | Apr | 101 | 93 |
| Theft Over | 5 | May | 114 | 105 |
| Theft Over | 6 | Jun | 113 | 104 |
| Theft Over | 7 | Jul | 118 | 109 |
| Theft Over | 8 | Aug | 118 | 109 |
| Theft Over | 9 | Sep | 114 | 105 |
| Theft Over | 10 | Oct | 116 | 107 |
| Theft Over | 11 | Nov | 114 | 105 |
| Theft Over | 12 | Dec | 110 | 101 |

_60 rows._
