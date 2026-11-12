"""
Flight Operations Dashboard
Python + Pandas (analysis) + Matplotlib (charts) + Tkinter (desktop UI) + CSV (data)
Run:  python main.py
"""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flights.csv")
ALL = "All"


# ----------------------------------------------------------------- data layer
def load_data(path=DATA_FILE):
    """Read the CSV and add derived columns."""
    df = pd.read_csv(path, parse_dates=["scheduled_departure"])
    df["route"] = df["origin"] + "-" + df["destination"]
    df["hour"] = df["scheduled_departure"].dt.hour
    df["month"] = df["scheduled_departure"].dt.month
    df["load_factor"] = (df["passengers"] / df["capacity"] * 100).round(1)
    return df


def apply_filters(df, airline=ALL, status=ALL):
    if airline != ALL:
        df = df[df["airline"] == airline]
    if status != ALL:
        df = df[df["status"] == status]
    return df


def compute_kpis(df):
    """Headline numbers shown on the dashboard cards."""
    total = len(df)
    if total == 0:
        return {"Total Flights": 0, "On-Time %": "0%", "Cancelled": 0,
                "Avg Delay (min)": 0, "Avg Load Factor": "0%"}
    flown = df[df["status"] != "Cancelled"]
    return {
        "Total Flights": total,
        "On-Time %": f"{(df['status'] == 'On Time').mean() * 100:.1f}%",
        "Cancelled": int((df["status"] == "Cancelled").sum()),
        "Avg Delay (min)": round(flown["departure_delay_min"].mean(), 1) if len(flown) else 0,
        "Avg Load Factor": f"{flown['load_factor'].mean():.1f}%" if len(flown) else "0%",
    }


# ------------------------------------------------------------------- UI layer
class Dashboard(tk.Tk):
    COLORS = {"On Time": "#2e9e5b", "Delayed": "#e0a030", "Cancelled": "#c94040"}

    def __init__(self):
        super().__init__()
        self.title("Flight Operations Dashboard")
        self.geometry("1200x780")
        self.minsize(1000, 650)
        self.df = pd.DataFrame()
        self.view = pd.DataFrame()
        self.airline_var = tk.StringVar(value=ALL)
        self.status_var = tk.StringVar(value=ALL)
        self._build_toolbar()
        self._build_kpis()
        self._build_tabs()
        self.reload()

    # ---- layout
    def _build_toolbar(self):
        bar = ttk.Frame(self, padding=8)
        bar.pack(fill="x")
        ttk.Label(bar, text="Airline:").pack(side="left")
        self.airline_cb = ttk.Combobox(bar, textvariable=self.airline_var,
                                       state="readonly", width=14)
        self.airline_cb.pack(side="left", padx=(4, 12))
        ttk.Label(bar, text="Status:").pack(side="left")
        self.status_cb = ttk.Combobox(bar, textvariable=self.status_var, state="readonly",
                                      width=12, values=[ALL, "On Time", "Delayed", "Cancelled"])
        self.status_cb.pack(side="left", padx=4)
        self.airline_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh())
        self.status_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh())
        ttk.Button(bar, text="Open CSV...", command=self.open_csv).pack(side="right", padx=4)
        ttk.Button(bar, text="Export view", command=self.export_view).pack(side="right", padx=4)
        ttk.Button(bar, text="Reload", command=self.reload).pack(side="right", padx=4)

    def _build_kpis(self):
        self.kpi_frame = ttk.Frame(self, padding=(8, 0))
        self.kpi_frame.pack(fill="x")
        self.kpi_labels = {}
        for i, name in enumerate(["Total Flights", "On-Time %", "Cancelled",
                                  "Avg Delay (min)", "Avg Load Factor"]):
            card = tk.Frame(self.kpi_frame, bg="#f2f4f8", bd=1, relief="solid", padx=14, pady=8)
            card.grid(row=0, column=i, padx=4, pady=6, sticky="nsew")
            self.kpi_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=name, bg="#f2f4f8", fg="#555", font=("Segoe UI", 9)).pack()
            val = tk.Label(card, text="-", bg="#f2f4f8", fg="#1a2b4c",
                           font=("Segoe UI", 18, "bold"))
            val.pack()
            self.kpi_labels[name] = val

    def _build_tabs(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)
        chart_tab, table_tab = ttk.Frame(nb), ttk.Frame(nb)
        nb.add(chart_tab, text="  Charts  ")
        nb.add(table_tab, text="  Flight Table  ")

        self.fig = Figure(figsize=(11, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_tab)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        cols = ["flight_id", "airline", "route", "scheduled_departure", "status",
                "departure_delay_min", "passengers", "capacity", "load_factor"]
        self.tree = ttk.Treeview(table_tab, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title(),
                              command=lambda col=c: self.sort_table(col))
            self.tree.column(c, width=110, anchor="center")
        sb = ttk.Scrollbar(table_tab, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self._sort_desc = False

    # ---- actions
    def reload(self):
        try:
            self.df = load_data(self._path if hasattr(self, "_path") else DATA_FILE)
        except Exception as exc:
            messagebox.showerror("Load error", f"Could not read data:\n{exc}")
            return
        self.airline_cb["values"] = [ALL] + sorted(self.df["airline"].unique())
        self.refresh()

    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self._path = path
            self.reload()

    def export_view(self):
        if self.view.empty:
            messagebox.showinfo("Export", "Nothing to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV files", "*.csv")])
        if path:
            self.view.to_csv(path, index=False)
            messagebox.showinfo("Export", f"Saved {len(self.view)} rows.")

    def sort_table(self, col):
        self._sort_desc = not self._sort_desc
        self.view = self.view.sort_values(col, ascending=not self._sort_desc)
        self.fill_table()

    def refresh(self):
        self.view = apply_filters(self.df, self.airline_var.get(), self.status_var.get())
        for name, value in compute_kpis(self.view).items():
            self.kpi_labels[name].config(text=str(value))
        self.draw_charts()
        self.fill_table()

    def fill_table(self):
        self.tree.delete(*self.tree.get_children())
        for _, r in self.view.head(1000).iterrows():
            self.tree.insert("", "end", values=(
                r.flight_id, r.airline, r.route, r.scheduled_departure.strftime("%Y-%m-%d %H:%M"),
                r.status, r.departure_delay_min, r.passengers, r.capacity, r.load_factor))

    # ---- charts
    def draw_charts(self):
        self.fig.clear()
        df = self.view
        if df.empty:
            self.fig.text(0.5, 0.5, "No data for this filter", ha="center", fontsize=14)
            self.canvas.draw()
            return
        ax1, ax2, ax3, ax4 = self.fig.subplots(2, 2).flatten()

        counts = df["status"].value_counts()
        ax1.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90,
                colors=[self.COLORS[s] for s in counts.index])
        ax1.set_title("Flight Status")

        flown = df[df["status"] != "Cancelled"]
        delay = flown.groupby("airline")["departure_delay_min"].mean().sort_values()
        ax2.barh(delay.index, delay.values, color="#3b6fd4")
        ax2.set_title("Avg Departure Delay by Airline (min)")

        by_hour = df.groupby("hour").size()
        ax3.plot(by_hour.index, by_hour.values, marker="o", color="#8a4fc4")
        ax3.set_title("Flights by Departure Hour")
        ax3.set_xlabel("Hour of day")
        ax3.grid(alpha=0.3)

        lf = flown.groupby("route")["load_factor"].mean().sort_values(ascending=False).head(8)
        ax4.bar(lf.index, lf.values, color="#2e9e9e")
        ax4.set_title("Top Routes by Load Factor (%)")
        ax4.tick_params(axis="x", rotation=45, labelsize=8)

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        raise SystemExit("flights.csv not found. Run: python generate_data.py")
    Dashboard().mainloop()
