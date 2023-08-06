import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import re


class DataFramePlotter:
    def __init__(self, df, time_column, unit_pattern):
        self.df = df
        self.time_column = time_column
        self.unit_pattern = unit_pattern
        self.columns = [col for col in df.columns if col != time_column]  # exclude time_column from columns to plot
        self.current_column_index = 0

        self.root = tk.Tk()
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_plot)
        self.next_button.pack(side=tk.RIGHT)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_plot)
        self.previous_button.pack(side=tk.RIGHT)

        self.plot_current_column()

    def plot_current_column(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        column_name = self.columns[self.current_column_index]
        ax.plot(self.df[self.time_column], self.df[column_name])

        # Extract units from column name and set y label
        match = re.search(self.unit_pattern, column_name)
        if match:
            ax.set_ylabel(match.group(1))  # Group 1 should be the units

        ax.set_title(column_name)
        self.canvas.draw()

    def next_plot(self):
        self.current_column_index = (self.current_column_index + 1) % len(self.columns)
        self.plot_current_column()

    def previous_plot(self):
        self.current_column_index = (self.current_column_index - 1) % len(self.columns)
        self.plot_current_column()

    def run(self):
        self.root.mainloop()
