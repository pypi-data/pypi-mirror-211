import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
import re


class DataFramePlotter:
    UNIT_PATTERNS = {
        'hyphen': '-([^-\n]+)$',
        'square_brackets': '\[([^]]+)\]$',
        'comma': ',\s*([^,]+)$',
    }

    def __init__(self, df, time_column, unit_format='hyphen'):
        self.df = df # Initialize data frame
        self.time_column = time_column # Initialize name of time column
        self.unit_pattern = self.UNIT_PATTERNS.get(unit_format, self.UNIT_PATTERNS['hyphen']) # Initialize pattern to find units
        self.columns = [col for col in df.columns if col != time_column]  # exclude time_column from columns to plot
        self.current_column_index = 0

        self.root = tk.Tk()
        self.fig = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_plot)
        self.next_button.pack(side=tk.RIGHT)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_plot)
        self.previous_button.pack(side=tk.RIGHT)

        self.plot_current_column()

        # Create frame containing xlim and ylim entries
        self.axis_frame = tk.Frame(self.root)
        self.xmin_label = tk.Label(self.axis_frame, text='xmin')
        self.xmin_entry = tk.Entry(self.axis_frame)
        self.xmax_label = tk.Label(self.axis_frame, text='xmax')
        self.xmax_entry = tk.Entry(self.axis_frame)
        self.ymin_label = tk.Label(self.axis_frame, text='ymin')
        self.ymin_entry = tk.Entry(self.axis_frame)
        self.ymax_label = tk.Label(self.axis_frame, text='ymax')
        self.ymax_entry = tk.Entry(self.axis_frame)

        self.xmin_entry.bind("<KeyRelease>", self.update_plot)
        self.xmax_entry.bind("<KeyRelease>", self.update_plot)
        self.ymin_entry.bind("<KeyRelease>", self.update_plot)
        self.ymax_entry.bind("<KeyRelease>", self.update_plot)

        self.axis_frame.pack(side=tk.BOTTOM, padx=(200, 200))

        # Connect the callback function to the 'motion_notify_event' event
        self.canvas.mpl_connect('motion_notify_event', self.update_entries_from_toolbar)

    def plot_current_column(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        column_name = self.columns[self.current_column_index]
        ax.plot(self.df[self.time_column], self.df[column_name])

        if self.unit_pattern != None:
            # Extract units from column name and set y label
            match = re.search(self.unit_pattern, column_name)
            if match:
                ax.set_ylabel(match.group(1))  # Group 1 should be the units
            # Remove units from column name
            column_name = re.sub(self.unit_pattern, '', column_name)

        ax.set_title(column_name)
        ax.set_xlabel(self.time_column)
        self.canvas.draw()

    def next_plot(self):
        self.current_column_index = (self.current_column_index + 1) % len(self.columns)
        self.plot_current_column()

    def previous_plot(self):
        self.current_column_index = (self.current_column_index - 1) % len(self.columns)
        self.plot_current_column()

    def run(self):
        self.root.mainloop()

    def update_entries_from_toolbar(self, event):
        self.xmin_entry.delete(0, tk.END)
        self.xmax_entry.delete(0, tk.END)
        self.ymin_entry.delete(0, tk.END)
        self.ymax_entry.delete(0, tk.END)

        self.xmin_entry.insert(0, self.ax.get_xlim()[0])
        self.xmax_entry.insert(0, self.ax.get_xlim()[1])
        self.ymin_entry.insert(0, self.ax.get_ylim()[0])
        self.ymax_entry.insert(0, self.ax.get_ylim()[1])

    def update_plot(self, event):
        xmin = float(self.xmin_entry.get() if self.xmin_entry.get() != '' else 0)
        xmax = float(self.xmax_entry.get() if self.xmax_entry.get() != '' else xmin + 1)
        ymin = float(self.ymin_entry.get() if self.ymin_entry.get() != '' else 0)
        ymax = float(self.ymax_entry.get() if self.ymax_entry.get() != '' else ymin + 1)
        self.ax.set_xlim(xmin, xmax)
        self.ax.set_ylim(ymin, ymax)
        self.fig.tight_layout()
        self.canvas.draw()
