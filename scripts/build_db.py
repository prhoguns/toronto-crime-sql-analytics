"""Build data/crime.duckdb from the raw files: one typed `incidents` table and a `neighbourhoods` table."""
import duckdb
import openpyxl

DB = "data/crime.duckdb"

POP_ROW = "Total - Age groups of the population - 25% sample data"
INCOME_ROW = "Median total income in 2020 ($)"


def neighbourhood_rows() -> list[tuple]:
    ws = openpyxl.load_workbook("data/neighbourhood_profiles_2021.xlsx", read_only=True)["hd2021_census_profile"]
    rows = ws.iter_rows(values_only=True)
    names = next(rows)[1:]
    numbers = next(rows)[1:]
    designation = next(rows)[1:]
    pop = income = None
    for row in rows:
        label = str(row[0]).strip() if row[0] else ""
        if label == POP_ROW:
            pop = row[1:]
        elif label == INCOME_ROW:
            income = row[1:]
        if pop and income:
            break
    return [
        (int(n), str(name), str(d), int(p), int(i) if i else None)
        for n, name, d, p, i in zip(numbers, names, designation, pop, income, strict=False)
        if n is not None
    ]


def main() -> None:
    con = duckdb.connect(DB)
    con.execute("drop table if exists neighbourhoods")
    con.execute(
        "create table neighbourhoods (neighbourhood_id int primary key, neighbourhood_name varchar, "
        "tsns_designation varchar, population_2021 int, median_income_2020 int)"
    )
    con.executemany("insert into neighbourhoods values (?, ?, ?, ?, ?)", neighbourhood_rows())

    con.execute("drop table if exists incidents")
    con.execute(
        """
        create table incidents as
        select
            _id                                   as row_id,
            EVENT_UNIQUE_ID                       as event_id,
            REPORT_DATE::date                     as report_date,
            try_cast(OCC_DATE as date)            as occurrence_date,
            try_cast(OCC_YEAR as int)             as occurrence_year,
            try_cast(OCC_HOUR as int)             as occurrence_hour,
            trim(OCC_DOW)                         as occurrence_dow,
            DIVISION                              as division,
            LOCATION_TYPE                         as location_type,
            PREMISES_TYPE                         as premises_type,
            OFFENCE                               as offence,
            MCI_CATEGORY                          as mci_category,
            try_cast(HOOD_158 as int)             as neighbourhood_id,
            try_cast(LONG_WGS84 as double)        as longitude,
            try_cast(LAT_WGS84 as double)         as latitude
        from read_csv('data/major_crime_indicators.csv', header = true, all_varchar = true)
        """
    )
    n = con.execute("select count(*) from incidents").fetchone()[0]
    h = con.execute("select count(*) from neighbourhoods").fetchone()[0]
    print(f"built {DB}: incidents={n:,} neighbourhoods={h}")


if __name__ == "__main__":
    main()
