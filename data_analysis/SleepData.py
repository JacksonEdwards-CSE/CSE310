"""Analyze the sleep dataset and display the results in a Tkinter GUI."""

import argparse
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import matplotlib
import pandas as pd

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


DATA_FILE = Path(__file__).with_name("dataset_2191_sleep.csv")
GRAPH_FILE = Path(__file__).with_name("sleep_by_danger.png")


def load_data() -> pd.DataFrame:
    """Load the CSV and convert its numeric columns to numbers."""
    sleep_data = pd.read_csv(DATA_FILE, na_values=["?"])
    sleep_data.index.name = "record"

    numeric_columns = [
        "body_weight",
        "brain_weight",
        "max_life_span",
        "gestation_time",
        "predation_index",
        "sleep_exposure_index",
        "danger_index",
        "total_sleep",
    ]
    sleep_data[numeric_columns] = sleep_data[numeric_columns].apply(
        pd.to_numeric, errors="coerce"
    )
    return sleep_data


def average_sleep_by_danger(sleep_data: pd.DataFrame) -> pd.DataFrame:
    """Return average total sleep grouped by danger index."""
    return (
        sleep_data.groupby("danger_index", as_index=False)["total_sleep"]
        .mean()
        .sort_values("danger_index")
    )


def make_average_sleep_figure(sleep_data: pd.DataFrame) -> Figure:
    """Create the average-sleep-by-danger bar chart."""
    chart_data = average_sleep_by_danger(sleep_data)
    figure = Figure(figsize=(8, 5), dpi=100)
    axis = figure.add_subplot(111)
    bars = axis.bar(
        chart_data["danger_index"].astype(str),
        chart_data["total_sleep"],
        color="steelblue",
    )
    axis.set_title("Average Total Sleep by Danger Index")
    axis.set_xlabel("Danger index")
    axis.set_ylabel("Average total sleep (hours)")
    axis.grid(axis="y", alpha=0.3)
    axis.bar_label(bars, fmt="%.2f")
    figure.tight_layout()
    return figure


def make_record_sleep_figure(sleep_data: pd.DataFrame) -> Figure:
    """Create a chart of individual records sorted by total sleep."""
    chart_data = sleep_data.sort_values("total_sleep", ascending=False)
    figure = Figure(figsize=(8, 5), dpi=100)
    axis = figure.add_subplot(111)
    axis.bar(
        chart_data.index.astype(str),
        chart_data["total_sleep"],
        color="darkorange",
    )
    axis.set_title("Total Sleep by Record (Sorted)")
    axis.set_xlabel("Record")
    axis.set_ylabel("Total sleep (hours)")
    axis.tick_params(axis="x", labelrotation=90, labelsize=7)
    axis.grid(axis="y", alpha=0.3)
    figure.tight_layout()
    return figure


def save_average_sleep_graph(sleep_data: pd.DataFrame) -> None:
    """Save the first chart as a PNG for use outside the GUI."""
    figure = make_average_sleep_figure(sleep_data)
    figure.savefig(GRAPH_FILE, dpi=150)
    figure.clear()


class SleepDataApp:
    """Tkinter application containing filters and two graph tabs."""

    def __init__(self, root: tk.Tk, sleep_data: pd.DataFrame) -> None:
        self.root = root
        self.all_data = sleep_data
        self.filtered_data = sleep_data
        self.canvases: list[FigureCanvasTkAgg] = []
        self.figures: list[Figure] = []

        root.title("Sleep Data Analysis")
        root.geometry("950x700")

        self._build_filter_panel()
        self._build_tabs()
        self.refresh_charts()

    def _build_filter_panel(self) -> None:
        filter_frame = ttk.LabelFrame(self.root, text="Filter data")
        filter_frame.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(filter_frame, text="Minimum total sleep (hours):").grid(
            row=0, column=0, padx=(10, 4), pady=10
        )
        self.minimum_sleep = tk.StringVar(value="0")
        ttk.Entry(filter_frame, textvariable=self.minimum_sleep, width=10).grid(
            row=0, column=1, padx=4, pady=10
        )

        ttk.Label(filter_frame, text="Danger index:").grid(
            row=0, column=2, padx=(20, 4), pady=10
        )
        danger_values = ["All"] + [
            str(int(value))
            for value in sorted(self.all_data["danger_index"].dropna().unique())
        ]
        self.danger_index = tk.StringVar(value="All")
        ttk.Combobox(
            filter_frame,
            textvariable=self.danger_index,
            values=danger_values,
            state="readonly",
            width=8,
        ).grid(row=0, column=3, padx=4, pady=10)

        ttk.Button(filter_frame, text="Apply filter", command=self.apply_filters).grid(
            row=0, column=4, padx=(20, 4), pady=10
        )
        ttk.Button(filter_frame, text="Clear", command=self.clear_filters).grid(
            row=0, column=5, padx=4, pady=10
        )

        self.filter_status = ttk.Label(filter_frame, text="")
        self.filter_status.grid(row=1, column=0, columnspan=6, padx=10, pady=(0, 8))

    def _build_tabs(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.average_tab = ttk.Frame(self.notebook)
        self.record_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.average_tab, text="Average by Danger")
        self.notebook.add(self.record_tab, text="Sleep by Record")

    def apply_filters(self) -> None:
        try:
            minimum_sleep = float(self.minimum_sleep.get() or 0)
        except ValueError:
            messagebox.showerror(
                "Invalid filter", "Minimum total sleep must be a number."
            )
            return

        if minimum_sleep < 0:
            messagebox.showerror(
                "Invalid filter", "Minimum total sleep cannot be negative."
            )
            return

        filtered = self.all_data[self.all_data["total_sleep"] >= minimum_sleep]
        if self.danger_index.get() != "All":
            filtered = filtered[
                filtered["danger_index"] == int(self.danger_index.get())
            ]

        self.filtered_data = filtered
        self.refresh_charts()

    def clear_filters(self) -> None:
        self.minimum_sleep.set("0")
        self.danger_index.set("All")
        self.filtered_data = self.all_data
        self.refresh_charts()

    def refresh_charts(self) -> None:
        for canvas in self.canvases:
            canvas.get_tk_widget().destroy()
        for figure in self.figures:
            figure.clear()
        self.canvases.clear()
        self.figures.clear()

        if self.filtered_data.empty:
            self.filter_status.configure(text="No records match the selected filters.")
            return

        self.filter_status.configure(
            text=f"Showing {len(self.filtered_data)} of {len(self.all_data)} records"
        )
        chart_specs = [
            (self.average_tab, make_average_sleep_figure(self.filtered_data)),
            (self.record_tab, make_record_sleep_figure(self.filtered_data)),
        ]
        for tab, figure in chart_specs:
            canvas = FigureCanvasTkAgg(figure, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.canvases.append(canvas)
            self.figures.append(figure)


def print_analysis(sleep_data: pd.DataFrame) -> None:
    """Print the original analysis results to the terminal."""
    most_sleep = sleep_data.sort_values("total_sleep", ascending=False).head(5)
    median_sleep = sleep_data["total_sleep"].median()
    grouped = average_sleep_by_danger(sleep_data).sort_values(
        "total_sleep", ascending=False
    )

    print("Sleep Data Analysis")
    print("=" * 20)
    print(f"Records analyzed: {len(sleep_data)}")
    print(f"Median total sleep: {median_sleep:.2f} hours")
    print(f"Graph saved to: {GRAPH_FILE.name}")
    print(
        f"Filter: {(sleep_data['total_sleep'] > median_sleep).sum()} records have "
        "more than the median amount of total sleep."
    )
    print("\nQuestion 1: Which records have the most total sleep?")
    print(most_sleep[["total_sleep", "danger_index"]].to_string())
    print("\nQuestion 2: What is the average total sleep for each danger index?")
    print(
        grouped.rename(columns={"total_sleep": "average_total_sleep"}).to_string(
            index=False,
            formatters={"average_total_sleep": lambda value: f"{value:.2f}"},
        )
    )


def main(show_gui: bool = True) -> None:
    sleep_data = load_data()
    save_average_sleep_graph(sleep_data)
    print_analysis(sleep_data)

    if show_gui:
        root = tk.Tk()
        SleepDataApp(root, sleep_data)
        root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze the sleep dataset.")
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="print the analysis and save the graph without opening Tkinter",
    )
    arguments = parser.parse_args()
    main(show_gui=not arguments.no_gui)
