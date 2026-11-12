# Mini Project Report: Flight Operations Dashboard

**Student:** Nedved William Machumu
**Date:** November 2026

## 1. Abstract
This project builds a desktop dashboard that analyses flight operations data. It reads flight records from a CSV file, calculates performance indicators with Pandas, draws charts with Matplotlib and presents everything in a Tkinter window. Operations staff can see punctuality, delays, cancellations and seat utilisation at a glance.

## 2. Problem Statement
Airlines and airports record large amounts of flight data, but raw tables make it hard to spot delay patterns or under-used routes. A simple visual tool is needed to summarise this data and let users filter it.

## 3. Objectives
- Load and clean flight data from a CSV file.
- Compute key performance indicators (KPIs).
- Visualise delays, status and route performance.
- Provide filtering, sorting and export in a desktop interface.

## 4. Technologies Used
| Technology | Purpose |
|------------|---------|
| Python     | Data processing |
| Tkinter    | Desktop dashboard |
| Matplotlib | Graphs and charts |
| Pandas     | Data analysis |
| CSV        | Flight dataset |

## 5. Dataset
`flights.csv` holds 500 synthetic flights across 5 airlines and 10 routes (both directions) for 2026. Fields include flight ID, airline, origin, destination, scheduled departure, departure and arrival delay, status, passengers, capacity, distance and aircraft type. A flight is `Delayed` when its departure delay exceeds 15 minutes; about 4% are `Cancelled`.

## 6. System Design
**Architecture (two layers)**
1. *Data layer:* `load_data()` reads the CSV and derives `route`, `hour`, `month` and `load_factor`; `apply_filters()` narrows the data; `compute_kpis()` returns headline metrics.
2. *UI layer:* the `Dashboard` class (Tkinter) builds the toolbar, KPI cards, a chart tab and a table tab.

**Data flow:** CSV → Pandas DataFrame → filters → KPIs, charts and table.

**Load factor** = passengers ÷ capacity × 100.

## 7. Implementation
- **Toolbar:** airline and status dropdowns, Reload, Export view, Open CSV.
- **KPI cards:** total flights, on-time percentage, cancellations, average delay, average load factor.
- **Charts (Matplotlib embedded via FigureCanvasTkAgg):**
  1. Pie chart of flight status
  2. Horizontal bar chart of average delay by airline
  3. Line chart of flights per departure hour
  4. Bar chart of top routes by load factor
- **Table:** Treeview with click-to-sort column headers.
- **Error handling:** a message box appears if the CSV cannot be read.

## 8. Results
The dashboard updates all KPIs, charts and the table whenever a filter changes. On the sample data roughly half the flights are on time, about 47% are delayed and 4% are cancelled. Delay patterns and busy hours are visible directly in the charts. *(Add screenshots of the running dashboard here.)*

## 9. Limitations
- The dataset is synthetic, not real operational data.
- Only the first 1,000 rows are shown in the table.
- No live data feed or date-range filter.

## 10. Future Scope
- Date-range and route filters.
- Delay prediction with a machine-learning model.
- Live data from an airline or airport API.
- Export of charts as images or PDF reports.

## 11. Conclusion
The project shows how Python, Pandas, Matplotlib and Tkinter can be combined into a useful analytics tool with no web server or database. It can be extended with real data and further analysis.

## 12. How to Run
```bash
pip install -r requirements.txt
python main.py
```
