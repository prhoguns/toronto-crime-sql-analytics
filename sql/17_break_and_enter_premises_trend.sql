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
