"""Generates the sample flights.csv dataset (run once, optional)."""
import csv, random
from datetime import datetime, timedelta

random.seed(42)
AIRLINES = {"IndiGo": "A320", "Air India": "B787", "SpiceJet": "B737",
            "Vistara": "A320", "Akasa Air": "B737"}
ROUTES = [("DEL", "BOM", 1150), ("DEL", "BLR", 1740), ("BOM", "BLR", 840),
          ("DEL", "CCU", 1305), ("BOM", "HYD", 620), ("BLR", "MAA", 290),
          ("DEL", "IXC", 245), ("BOM", "GOI", 440), ("CCU", "BLR", 1560),
          ("HYD", "DEL", 1260)]
CAP = {"A320": 180, "B787": 256, "B737": 189}

rows, start = [], datetime(2026, 1, 1)
for i in range(1, 501):
    airline, ac = random.choice(list(AIRLINES.items()))
    o, d, km = random.choice(ROUTES)
    if random.random() < 0.5:
        o, d = d, o
    dep = start + timedelta(days=random.randint(0, 303), hours=random.randint(5, 23),
                            minutes=random.choice([0, 10, 20, 30, 40, 50]))
    r = random.random()
    if r < 0.04:
        status, dd, ad, pax = "Cancelled", 0, 0, 0
    else:
        base = random.choice([0, 0, 0, 5, 10, 25, 45, 90, 150])
        dd = max(0, int(random.gauss(base, 8)))
        ad = max(0, dd + random.randint(-10, 15))
        status = "Delayed" if dd > 15 else "On Time"
        pax = int(CAP[ac] * random.uniform(0.55, 1.0))
    rows.append([f"FL{1000+i}", airline, o, d, dep.strftime("%Y-%m-%d %H:%M"),
                 dd, ad, status, pax, CAP[ac], km, ac])

with open("flights.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["flight_id", "airline", "origin", "destination", "scheduled_departure",
                "departure_delay_min", "arrival_delay_min", "status", "passengers",
                "capacity", "distance_km", "aircraft"])
    w.writerows(rows)
print("flights.csv created with", len(rows), "rows")
