# Flight Operations Dashboard

A desktop mini project that analyses airline flight operations and shows the results in an interactive dashboard.

| Technology | Purpose |
|------------|---------|
| Python     | Data processing |
| Tkinter    | Desktop dashboard |
| Matplotlib | Graphs and charts |
| Pandas     | Data analysis |
| CSV        | Flight dataset |

## Features
- KPI cards: total flights, on-time %, cancellations, average delay, average load factor
- Four charts: status split, delay by airline, flights per hour, top routes by load factor
- Filter by airline and flight status
- Sortable flight table
- Load another CSV with the same columns, and export the filtered view

## Project structure
```
main.py               # dashboard application
generate_data.py      # optional: regenerates the sample dataset
flights.csv           # 500 sample flights
requirements.txt
Mini_Project_Report.md
```

## Setup
```bash
pip install -r requirements.txt
# Linux only, if Tkinter is missing:
sudo apt install python3-tk
python main.py
```

## CSV columns
`flight_id, airline, origin, destination, scheduled_departure, departure_delay_min, arrival_delay_min, status, passengers, capacity, distance_km, aircraft`

`status` is one of `On Time`, `Delayed` (departure delay > 15 min) or `Cancelled`.

The dataset is synthetic and for learning purposes only.
