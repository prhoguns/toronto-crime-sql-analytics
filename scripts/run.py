"""Run every query in sql/ against data/crime.duckdb, write results/<name>.md, and draw the charts.

    python scripts/run.py            # everything
    python scripts/run.py 08 16      # just queries 08 and 16
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

DB = "data/crime.duckdb"
SQL_DIR = Path("sql")
OUT_DIR = Path("results")
CHART_DIR = Path("charts")
MAX_ROWS = 60


NO_SEPARATOR = ("year", "id", "hour", "rank", "num", "month", "rows", "rn")


def fmt_cell(v, col: str = "") -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)) or v is pd.NaT or v is pd.NA:
        return ""
    sep = "" if any(k in col for k in NO_SEPARATOR) else ","
    if isinstance(v, (bool, np.bool_)):
        return str(v)
    if isinstance(v, (int, np.integer)):
        return f"{int(v):{sep}}"
    if isinstance(v, (float, np.floating)):
        return f"{int(v):{sep}}" if float(v).is_integer() else f"{v:{sep}.1f}"
    if isinstance(v, (pd.Timestamp,)):
        return v.strftime("%Y-%m-%d")
    return str(v)


def to_markdown(df: pd.DataFrame) -> str:
    """Own renderer: pandas.to_markdown upcasts every column to float when any column is float."""
    cols = list(df.columns)
    numeric = [pd.api.types.is_numeric_dtype(df[c]) for c in cols]
    head = "| " + " | ".join(cols) + " |"
    sep = "|" + "|".join("---:" if n else ":---" for n in numeric) + "|"
    rows = ["| " + " | ".join(fmt_cell(v, c) for v, c in zip(rec, cols, strict=True)) + " |" for rec in df.itertuples(index=False, name=None)]
    return "\n".join([head, sep, *rows])


def run_query(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    sql = path.read_text()
    df = con.execute(sql).df()
    question = next((line.lstrip("- ").strip() for line in sql.splitlines() if line.startswith("-- Q")), path.stem)
    body = to_markdown(df.head(MAX_ROWS))
    note = f"\n\n_{len(df):,} rows; showing first {MAX_ROWS}._" if len(df) > MAX_ROWS else f"\n\n_{len(df):,} rows._"
    (OUT_DIR / f"{path.stem}.md").write_text(f"# {question}\n\n```sql\n{sql.strip()}\n```\n\n{body}{note}\n")
    print(f"{path.stem}: {len(df):,} rows")


def charts(con: duckdb.DuckDBPyConnection) -> None:
    CHART_DIR.mkdir(exist_ok=True)
    plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False, "axes.spines.right": False})

    # 1. Category trend
    df = con.execute((SQL_DIR / "01_incidents_by_year_and_category.sql").read_text()).df()
    ax = df.set_index("year")[["assault", "auto_theft", "break_and_enter", "robbery", "theft_over"]].plot(figsize=(9, 4.5))
    ax.set_title("Major crime incidents by category, Toronto 2014-2025 (2025 partial)")
    ax.set_ylabel("incidents")
    ax.figure.tight_layout()
    ax.figure.savefig(CHART_DIR / "01_category_trend.png")

    # 2. Auto theft rolling average
    df = con.execute((SQL_DIR / "08_auto_theft_rolling_12m.sql").read_text()).df()
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(df["month"], df["auto_thefts"], width=25, color="#c9d6e3", label="monthly")
    ax.plot(df["month"], df["trailing_12m_avg"], color="#1f4e79", linewidth=2, label="trailing 12-month avg")
    ax.set_title("Auto theft per month with trailing 12-month average")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CHART_DIR / "08_auto_theft_rolling.png")

    # 3. Heatmap
    df = con.execute((SQL_DIR / "05_weekday_hour_heatmap.sql").read_text()).df()
    grid = df.pivot(index="dow_num", columns="occurrence_hour", values="assaults")
    fig, ax = plt.subplots(figsize=(10, 3.6))
    im = ax.imshow(grid, aspect="auto", cmap="YlOrRd")
    ax.set_yticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_xticks(range(0, 24, 2), range(0, 24, 2))
    ax.set_xlabel("hour of day")
    ax.set_title("Assaults by day of week and hour, 2014-2025")
    fig.colorbar(im, ax=ax, label="incidents")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "05_assault_heatmap.png")

    # 4. Rate per 1000, top 10
    df = con.execute((SQL_DIR / "07_crime_rate_per_1000.sql").read_text()).df()
    top = df[df.bucket == "highest"].sort_values("per_1000")
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.barh(top["neighbourhood_name"], top["per_1000"], color="#1f4e79")
    ax.set_xlabel("incidents per 1,000 residents, 2024")
    ax.set_title("Highest crime rate neighbourhoods (2021 census population)")
    fig.tight_layout()
    fig.savefig(CHART_DIR / "07_rate_per_1000.png")
    print("charts written")


def main(argv: list[str]) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    con = duckdb.connect(DB, read_only=True)
    files = sorted(SQL_DIR.glob("*.sql"))
    if argv:
        files = [f for f in files if f.name[:2] in argv]
    for f in files:
        run_query(con, f)
    if not argv:
        charts(con)


if __name__ == "__main__":
    main(sys.argv[1:])
