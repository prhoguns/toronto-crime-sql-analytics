-- Q8. Monthly auto thefts with a trailing 12-month average to smooth seasonality.
-- Technique: window frame ROWS BETWEEN 11 PRECEDING AND CURRENT ROW.
with monthly as (
    select date_trunc('month', occurrence_date)::date as month, count(*) as auto_thefts
    from incidents
    where mci_category = 'Auto Theft' and occurrence_date >= '2014-01-01'
    group by 1
)
select
    month,
    auto_thefts,
    round(avg(auto_thefts) over (order by month rows between 11 preceding and current row), 1) as trailing_12m_avg,
    max(auto_thefts) over () as all_time_peak_month
from monthly
order by month;
