"""Build a tiny synthetic data/crime.duckdb so every query can be smoke-tested in CI without the 135 MB download."""
import duckdb

con = duckdb.connect("data/crime.duckdb")
con.execute("drop table if exists neighbourhoods")
con.execute(
    "create table neighbourhoods (neighbourhood_id int, neighbourhood_name varchar, tsns_designation varchar, "
    "population_2021 int, median_income_2020 int)"
)
con.execute(
    "insert into neighbourhoods values (1,'A','Neighbourhood Improvement Area',10000,40000),"
    "(2,'B','Not an NIA or Emerging Neighbourhood',20000,50000)"
)
con.execute("drop table if exists incidents")
con.execute(
    """
    create table incidents as
    select
        i as row_id,
        'GO-' || i as event_id,
        ('2014-01-01'::date + (i * 7)::int) as report_date,
        ('2014-01-01'::date + (i * 7)::int) as occurrence_date,
        year('2014-01-01'::date + (i * 7)::int) as occurrence_year,
        (i * 5) % 24 as occurrence_hour,
        ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][1 + i % 7] as occurrence_dow,
        'D' || (10 + i % 5) as division,
        'x' as location_type,
        ['House','Apartment','Commercial'][1 + i % 3] as premises_type,
        'Offence ' || (i % 9) as offence,
        ['Assault','Auto Theft','Break and Enter','Robbery','Theft Over'][1 + i % 5] as mci_category,
        1 + i % 2 as neighbourhood_id,
        -79.4 as longitude,
        43.7 as latitude
    from range(600) t(i)
    """
)
print("fixture built")
