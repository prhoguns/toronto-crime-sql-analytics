"""Download the two source files from open.toronto.ca into data/."""
from pathlib import Path

import requests

CKAN = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action"
FILES = {
    "major_crime_indicators.csv": ("major-crime-indicators", "major-crime-indicators.csv"),
    "neighbourhood_profiles_2021.xlsx": ("neighbourhood-profiles", "neighbourhood-profiles-2021-158-model"),
}


def resource_url(package: str, name: str) -> str:
    pkg = requests.get(f"{CKAN}/package_show", params={"id": package}, timeout=60).json()["result"]
    return next(r["url"] for r in pkg["resources"] if r["name"] == name)


def main() -> None:
    Path("data").mkdir(exist_ok=True)
    for fname, (pkg, res) in FILES.items():
        dest = Path("data") / fname
        if dest.exists():
            print(f"{fname}: already present")
            continue
        url = resource_url(pkg, res)
        print(f"{fname}: downloading {url}")
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            dest.write_bytes(r.content)
        print(f"{fname}: {dest.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
