# Q2. Year-over-year % change per category. Which category had the biggest single-year jump?

```sql
-- Q2. Year-over-year % change per category. Which category had the biggest single-year jump?
-- Technique: LAG() window over a partition, NULLIF to avoid divide-by-zero.
with yearly as (
    select mci_category, occurrence_year as year, count(*) as incidents
    from incidents
    where occurrence_year between 2014 and 2024   -- 2025 is a partial year
    group by 1, 2
)
select
    mci_category,
    year,
    incidents,
    lag(incidents) over (partition by mci_category order by year)                  as prev_year,
    round(100.0 * (incidents - lag(incidents) over (partition by mci_category order by year))
          / nullif(lag(incidents) over (partition by mci_category order by year), 0), 1) as yoy_pct
from yearly
order by mci_category, year;
```

| mci_category | year | incidents | prev_year | yoy_pct |
|:---|---:|---:|---:|---:|
| Assault | 2014 | 16884 |  |  |
| Assault | 2015 | 18181 | 16884 | 7.7 |
| Assault | 2016 | 19093 | 18181 | 5 |
| Assault | 2017 | 19721 | 19093 | 3.3 |
| Assault | 2018 | 20096 | 19721 | 1.9 |
| Assault | 2019 | 21146 | 20096 | 5.2 |
| Assault | 2020 | 18503 | 21146 | -12.5 |
| Assault | 2021 | 19222 | 18503 | 3.9 |
| Assault | 2022 | 21452 | 19222 | 11.6 |
| Assault | 2023 | 24385 | 21452 | 13.7 |
| Assault | 2024 | 24910 | 24385 | 2.2 |
| Auto Theft | 2014 | 3640 |  |  |
| Auto Theft | 2015 | 3269 | 3640 | -10.2 |
| Auto Theft | 2016 | 3348 | 3269 | 2.4 |
| Auto Theft | 2017 | 3647 | 3348 | 8.9 |
| Auto Theft | 2018 | 4804 | 3647 | 31.7 |
| Auto Theft | 2019 | 5382 | 4804 | 12 |
| Auto Theft | 2020 | 5810 | 5382 | 8 |
| Auto Theft | 2021 | 6648 | 5810 | 14.4 |
| Auto Theft | 2022 | 9894 | 6648 | 48.8 |
| Auto Theft | 2023 | 12520 | 9894 | 26.5 |
| Auto Theft | 2024 | 9610 | 12520 | -23.2 |
| Break and Enter | 2014 | 7216 |  |  |
| Break and Enter | 2015 | 6938 | 7216 | -3.9 |
| Break and Enter | 2016 | 6425 | 6938 | -7.4 |
| Break and Enter | 2017 | 6932 | 6425 | 7.9 |
| Break and Enter | 2018 | 7654 | 6932 | 10.4 |
| Break and Enter | 2019 | 8573 | 7654 | 12 |
| Break and Enter | 2020 | 6963 | 8573 | -18.8 |
| Break and Enter | 2021 | 5724 | 6963 | -17.8 |
| Break and Enter | 2022 | 6088 | 5724 | 6.4 |
| Break and Enter | 2023 | 7644 | 6088 | 25.6 |
| Break and Enter | 2024 | 6847 | 7644 | -10.4 |
| Robbery | 2014 | 3757 |  |  |
| Robbery | 2015 | 3534 | 3757 | -5.9 |
| Robbery | 2016 | 3777 | 3534 | 6.9 |
| Robbery | 2017 | 4097 | 3777 | 8.5 |
| Robbery | 2018 | 3758 | 4097 | -8.3 |
| Robbery | 2019 | 3724 | 3758 | -0.9 |
| Robbery | 2020 | 2863 | 3724 | -23.1 |
| Robbery | 2021 | 2285 | 2863 | -20.2 |
| Robbery | 2022 | 2931 | 2285 | 28.3 |
| Robbery | 2023 | 3138 | 2931 | 7.1 |
| Robbery | 2024 | 3175 | 3138 | 1.2 |
| Theft Over | 2014 | 1015 |  |  |
| Theft Over | 2015 | 1044 | 1015 | 2.9 |
| Theft Over | 2016 | 1045 | 1044 | 0.1 |
| Theft Over | 2017 | 1188 | 1045 | 13.7 |
| Theft Over | 2018 | 1290 | 1188 | 8.6 |
| Theft Over | 2019 | 1375 | 1290 | 6.6 |
| Theft Over | 2020 | 1213 | 1375 | -11.8 |
| Theft Over | 2021 | 1091 | 1213 | -10.1 |
| Theft Over | 2022 | 1458 | 1091 | 33.6 |
| Theft Over | 2023 | 1745 | 1458 | 19.7 |
| Theft Over | 2024 | 1869 | 1745 | 7.1 |

_55 rows._
