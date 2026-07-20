# Q1. How has each major crime category trended year over year since 2014?

```sql
-- Q1. How has each major crime category trended year over year since 2014?
-- Technique: conditional aggregation (a manual pivot).
select
    occurrence_year as year,
    count(*) filter (where mci_category = 'Assault')          as assault,
    count(*) filter (where mci_category = 'Auto Theft')       as auto_theft,
    count(*) filter (where mci_category = 'Break and Enter')  as break_and_enter,
    count(*) filter (where mci_category = 'Robbery')          as robbery,
    count(*) filter (where mci_category = 'Theft Over')       as theft_over,
    count(*)                                                  as total
from incidents
where occurrence_year between 2014 and 2025
group by 1
order by 1;
```

| year | assault | auto_theft | break_and_enter | robbery | theft_over | total |
|---:|---:|---:|---:|---:|---:|---:|
| 2014 | 16,884 | 3,640 | 7,216 | 3,757 | 1,015 | 32,512 |
| 2015 | 18,181 | 3,269 | 6,938 | 3,534 | 1,044 | 32,966 |
| 2016 | 19,093 | 3,348 | 6,425 | 3,777 | 1,045 | 33,688 |
| 2017 | 19,721 | 3,647 | 6,932 | 4,097 | 1,188 | 35,585 |
| 2018 | 20,096 | 4,804 | 7,654 | 3,758 | 1,290 | 37,602 |
| 2019 | 21,146 | 5,382 | 8,573 | 3,724 | 1,375 | 40,200 |
| 2020 | 18,503 | 5,810 | 6,963 | 2,863 | 1,213 | 35,352 |
| 2021 | 19,222 | 6,648 | 5,724 | 2,285 | 1,091 | 34,970 |
| 2022 | 21,452 | 9,894 | 6,088 | 2,931 | 1,458 | 41,823 |
| 2023 | 24,385 | 12,520 | 7,644 | 3,138 | 1,745 | 49,432 |
| 2024 | 24,910 | 9,610 | 6,847 | 3,175 | 1,869 | 46,411 |
| 2025 | 17,699 | 5,110 | 4,449 | 2,031 | 1,399 | 30,688 |

_12 rows._
