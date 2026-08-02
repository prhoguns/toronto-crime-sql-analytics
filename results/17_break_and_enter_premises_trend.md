# Q17. Break and enters: is the shift toward commercial vs residential premises real?

```sql
-- Q17. Break and enters: is the shift toward commercial vs residential premises real?
-- Technique: conditional aggregation + share, year by year.
select
    occurrence_year as year,
    count(*) as break_and_enters,
    count(*) filter (where premises_type = 'House')       as house,
    count(*) filter (where premises_type = 'Apartment')   as apartment,
    count(*) filter (where premises_type = 'Commercial')  as commercial,
    round(100.0 * count(*) filter (where premises_type = 'Commercial') / count(*), 1) as pct_commercial
from incidents
where mci_category = 'Break and Enter' and occurrence_year between 2014 and 2024
group by 1
order by 1;
```

| year | break_and_enters | house | apartment | commercial | pct_commercial |
|---:|---:|---:|---:|---:|---:|
| 2014 | 7,216 | 2,947 | 1,881 | 1,928 | 26.7 |
| 2015 | 6,938 | 2,646 | 2,004 | 1,938 | 27.9 |
| 2016 | 6,425 | 2,500 | 1,591 | 1,924 | 29.9 |
| 2017 | 6,932 | 2,580 | 1,829 | 2,142 | 30.9 |
| 2018 | 7,654 | 2,524 | 2,028 | 2,581 | 33.7 |
| 2019 | 8,573 | 2,196 | 2,452 | 3,357 | 39.2 |
| 2020 | 6,963 | 1,587 | 1,858 | 2,899 | 41.6 |
| 2021 | 5,724 | 1,166 | 1,630 | 2,426 | 42.4 |
| 2022 | 6,088 | 1,339 | 1,668 | 2,570 | 42.2 |
| 2023 | 7,644 | 2,113 | 1,796 | 3,103 | 40.6 |
| 2024 | 6,847 | 2,121 | 1,619 | 2,546 | 37.2 |

_11 rows._
