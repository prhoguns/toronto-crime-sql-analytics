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
