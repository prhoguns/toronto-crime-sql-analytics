"""Build docs/index.html: an interactive Plotly dashboard from the same queries, published on GitHub Pages.

No server, no framework: the data is embedded as JSON and plotly.js is loaded from a CDN.
"""
from __future__ import annotations

import json
from pathlib import Path

import duckdb

DB = "data/crime.duckdb"
OUT = Path("docs/index.html")

con = duckdb.connect(DB, read_only=True)


def q(name: str):
    return con.execute(Path(f"sql/{name}.sql").read_text()).df()


yearly = q("01_incidents_by_year_and_category")
rolling = q("08_auto_theft_rolling_12m")
rates = q("07_crime_rate_per_1000")
heat = q("05_weekday_hour_heatmap")
premises = q("17_break_and_enter_premises_trend")
hours = q("04_peak_hours_by_category")
dq = q("20_data_quality_profile").iloc[0]
top_rates = rates[rates.bucket == "highest"].sort_values("per_1000")
grid = heat.pivot(index="dow_num", columns="occurrence_hour", values="assaults")

data = {
    "yearly": {"year": yearly["year"].tolist(), **{c: yearly[c].tolist() for c in ["assault", "auto_theft", "break_and_enter", "robbery", "theft_over"]}},
    "rolling": {"month": rolling["month"].astype(str).tolist(), "monthly": rolling["auto_thefts"].tolist(), "avg": rolling["trailing_12m_avg"].tolist()},
    "rates": {"name": top_rates["neighbourhood_name"].tolist(), "per_1000": top_rates["per_1000"].tolist(), "pop": top_rates["population_2021"].tolist()},
    "heat": {"z": grid.values.tolist(), "x": [int(c) for c in grid.columns], "y": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]},
    "premises": {"year": premises["year"].tolist(), "house": premises["house"].tolist(), "apartment": premises["apartment"].tolist(), "commercial": premises["commercial"].tolist()},
    "totals": {"rows": int(dq["total_rows"]), "events": int(dq["distinct_events"]), "latest": str(dq["latest_report"])[:10]},
}

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Toronto Crime Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
  :root {{ --ink:#1b2430; --muted:#5b6672; --line:#e3e8ee; --accent:#1f4e79; --bg:#f7f9fb; }}
  * {{ box-sizing:border-box }} body {{ margin:0; font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; color:var(--ink); background:var(--bg) }}
  header {{ background:#fff; border-bottom:1px solid var(--line); padding:20px 24px }}
  h1 {{ margin:0 0 4px; font-size:22px }} header p {{ margin:0; color:var(--muted) }}
  .kpis {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; padding:16px 24px 0 }}
  .kpi {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:12px 16px }}
  .kpi b {{ display:block; font-size:24px; color:var(--accent) }} .kpi span {{ color:var(--muted); font-size:13px }}
  main {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(460px,1fr)); gap:16px; padding:16px 24px 32px }}
  .card {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:8px 8px 0 }}
  .card h2 {{ font-size:15px; margin:8px 12px 0; font-weight:600 }} .card p {{ margin:2px 12px 8px; color:var(--muted); font-size:13px }}
  .plot {{ width:100%; height:340px }}
  footer {{ padding:0 24px 24px; color:var(--muted); font-size:13px }} a {{ color:var(--accent) }}
  @media (max-width:520px) {{ main {{ grid-template-columns:1fr; padding:12px 16px }} .kpis {{ padding:12px 16px 0 }} }}
</style></head>
<body>
<header><h1>Toronto Major Crime Indicators, 2014 – {data['totals']['latest'][:4]}</h1>
<p>Toronto Police Service open data · {data['totals']['rows']:,} offence records across {data['totals']['events']:,} events · latest report {data['totals']['latest']} ·
<a href="https://github.com/prhoguns/toronto-crime-sql-analytics">queries and methodology</a></p></header>
<div class="kpis">
  <div class="kpi"><b>{yearly.loc[yearly.year == 2024, 'total'].iloc[0]:,}</b><span>incidents in 2024</span></div>
  <div class="kpi"><b>{int(yearly.loc[yearly.year == 2023, 'auto_theft'].iloc[0]):,}</b><span>auto thefts at the 2023 peak (3,647 in 2017)</span></div>
  <div class="kpi"><b>{top_rates.iloc[-1]['per_1000']}</b><span>per 1,000 residents, {top_rates.iloc[-1]['neighbourhood_name']} (2024)</span></div>
  <div class="kpi"><b>{int(rolling['trailing_12m_avg'].iloc[-1])}</b><span>auto thefts / month, trailing 12-month avg</span></div>
</div>
<main>
  <div class="card"><h2>Incidents by category and year</h2><p>2025 is a partial year.</p><div id="yearly" class="plot"></div></div>
  <div class="card"><h2>Auto theft per month</h2><p>Bars: monthly count. Line: trailing 12-month average.</p><div id="rolling" class="plot"></div></div>
  <div class="card"><h2>Highest 2024 rate per 1,000 residents</h2><p>2021 census population. Downtown cores have small resident counts and large daytime populations.</p><div id="rates" class="plot"></div></div>
  <div class="card"><h2>Assaults by weekday and hour</h2><p>All years. Midnight and weekend nights dominate.</p><div id="heat" class="plot"></div></div>
  <div class="card"><h2>Break and enter by premises type</h2><p>House break-ins halved 2014–2021 while commercial rose.</p><div id="premises" class="plot"></div></div>
</main>
<footer>Built from <a href="https://open.toronto.ca/dataset/major-crime-indicators/">open.toronto.ca</a> under the Open Government Licence – Toronto. Static page generated by <code>scripts/build_dashboard.py</code>.</footer>
<script>
const D = {json.dumps(data)};
const base = {{ margin:{{l:48,r:16,t:8,b:40}}, paper_bgcolor:'#fff', plot_bgcolor:'#fff', font:{{family:'inherit',size:12}}, legend:{{orientation:'h',y:-0.18}} }};
const cfg = {{ displayModeBar:false, responsive:true }};
const cat = {{assault:'Assault',auto_theft:'Auto theft',break_and_enter:'Break and enter',robbery:'Robbery',theft_over:'Theft over'}};
Plotly.newPlot('yearly', Object.keys(cat).map(k=>({{x:D.yearly.year,y:D.yearly[k],name:cat[k],mode:'lines+markers'}})), {{...base, xaxis:{{dtick:1}}, yaxis:{{title:'incidents'}}}}, cfg);
Plotly.newPlot('rolling', [
  {{x:D.rolling.month,y:D.rolling.monthly,type:'bar',name:'monthly',marker:{{color:'#c9d6e3'}}}},
  {{x:D.rolling.month,y:D.rolling.avg,mode:'lines',name:'trailing 12-mo avg',line:{{color:'#1f4e79',width:2.5}}}}
], {{...base, bargap:0.1}}, cfg);
Plotly.newPlot('rates', [{{x:D.rates.per_1000,y:D.rates.name,type:'bar',orientation:'h',marker:{{color:'#1f4e79'}},text:D.rates.pop.map(p=>'pop '+p.toLocaleString()),textposition:'inside',insidetextanchor:'start',textfont:{{color:'#fff'}}}}],
  {{...base, margin:{{l:190,r:16,t:8,b:40}}, xaxis:{{title:'incidents per 1,000 residents, 2024'}}}}, cfg);
Plotly.newPlot('heat', [{{z:D.heat.z,x:D.heat.x,y:D.heat.y,type:'heatmap',colorscale:'YlOrRd',showscale:false,hovertemplate:'%{{y}} %{{x}}:00 — %{{z}} assaults<extra></extra>'}}], {{...base, xaxis:{{title:'hour of day',dtick:2}}}}, cfg);
Plotly.newPlot('premises', ['house','apartment','commercial'].map(k=>({{x:D.premises.year,y:D.premises[k],name:k,type:'bar'}})), {{...base, barmode:'stack', xaxis:{{dtick:1}}}}, cfg);
</script></body></html>"""
OUT.write_text(html)
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
