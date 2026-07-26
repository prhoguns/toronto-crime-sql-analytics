# Q9. Where does each type of crime happen? Share of incidents by premises type within category.

```sql
-- Q9. Where does each type of crime happen? Share of incidents by premises type within category.
-- Technique: SUM() OVER (PARTITION BY) to compute percentage of group total.
select
    mci_category,
    premises_type,
    count(*) as incidents,
    round(100.0 * count(*) / sum(count(*)) over (partition by mci_category), 1) as pct_of_category
from incidents
where occurrence_year >= 2020
group by 1, 2
order by mci_category, incidents desc;
```

| mci_category | premises_type | incidents | pct_of_category |
|:---|:---|---:|---:|
| Assault | Apartment | 39687 | 31.5 |
| Assault | Outside | 31265 | 24.8 |
| Assault | Commercial | 19283 | 15.3 |
| Assault | House | 14373 | 11.4 |
| Assault | Other | 10077 | 8 |
| Assault | Transit | 7757 | 6.1 |
| Assault | Educational | 3729 | 3 |
| Auto Theft | Outside | 26023 | 52.5 |
| Auto Theft | House | 16114 | 32.5 |
| Auto Theft | Commercial | 3794 | 7.7 |
| Auto Theft | Apartment | 1728 | 3.5 |
| Auto Theft | Other | 1722 | 3.5 |
| Auto Theft | Transit | 145 | 0.3 |
| Auto Theft | Educational | 66 | 0.1 |
| Break and Enter | Commercial | 15118 | 40.1 |
| Break and Enter | Apartment | 9782 | 25.9 |
| Break and Enter | House | 9616 | 25.5 |
| Break and Enter | Other | 2436 | 6.5 |
| Break and Enter | Educational | 638 | 1.7 |
| Break and Enter | Transit | 76 | 0.2 |
| Break and Enter | Outside | 49 | 0.1 |
| Robbery | Outside | 7009 | 42.7 |
| Robbery | Commercial | 5356 | 32.6 |
| Robbery | Apartment | 1334 | 8.1 |
| Robbery | Other | 929 | 5.7 |
| Robbery | House | 802 | 4.9 |
| Robbery | Transit | 636 | 3.9 |
| Robbery | Educational | 357 | 2.2 |
| Theft Over | Commercial | 2880 | 32.8 |
| Theft Over | Outside | 2501 | 28.5 |
| Theft Over | Apartment | 1599 | 18.2 |
| Theft Over | House | 1191 | 13.6 |
| Theft Over | Other | 466 | 5.3 |
| Theft Over | Educational | 81 | 0.9 |
| Theft Over | Transit | 57 | 0.6 |

_35 rows._
