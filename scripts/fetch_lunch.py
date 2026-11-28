"""Fetch upcoming school lunch menus from MealViewer and write lunch.json.

Run by the GitHub Actions workflow in .github/workflows/lunch.yml.
"""
import datetime as dt
import json
import sys
import urllib.request

SCHOOL = "ClarksvilleElementary"
DAYS_AHEAD = 21
SIDE_TYPES = ("VEGETABLE", "FRUIT")  # milk is the same every day, so it is left out


def tidy(name):
    name = " ".join(name.split())
    return name.title().replace("'S ", "'s ").replace("W/", "w/") if name.isupper() else name


def main():
    start = dt.date.today() - dt.timedelta(days=1)
    end = start + dt.timedelta(days=DAYS_AHEAD)
    url = (f"https://api.mealviewer.com/api/v4/school/{SCHOOL}/"
           f"{start:%m-%d-%Y}/{end:%m-%d-%Y}/")
    req = urllib.request.Request(url, headers={"User-Agent": "morning-dashboard"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)

    days = []
    for sched in data.get("menuSchedules", []):
        date = (sched.get("dateInformation") or {}).get("dateFull", "")[:10]
        for block in sched.get("menuBlocks", []):
            if (block.get("blockName") or "").strip().lower() != "lunch":
                continue
            entrees, sides = [], []
            for line in (block.get("cafeteriaLineList") or {}).get("data", []):
                for item in (line.get("foodItemList") or {}).get("data", []):
                    kind = (item.get("item_Type") or "").upper()
                    name = tidy(item.get("item_Name") or "")
                    if not name:
                        continue
                    if "ENTREE" in kind or "MAIN" in kind:
                        bucket = entrees
                    elif any(t in kind for t in SIDE_TYPES):
                        bucket = sides
                    else:
                        continue
                    if name not in bucket:
                        bucket.append(name)
            if entrees or sides:
                days.append({"date": date, "entrees": entrees, "sides": sides})

    if not data.get("menuSchedules"):
        sys.exit("MealViewer returned no menus; keeping the previous lunch.json")

    out = {"school": (data.get("physicalLocation") or {}).get("name", SCHOOL),
           "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "days": sorted(days, key=lambda d: d["date"])}
    with open("lunch.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"Saved {len(days)} lunch days")


if __name__ == "__main__":
    main()
