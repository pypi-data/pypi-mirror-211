import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
import re
import warnings


class DataFramePlotter:
    UNIT_PATTERNS = {
        'hyphen': '-([^-\n]+)$',
        'square_brackets': '\[([^]]+)\]$',
        'comma': ',\s*([^,]+)$',
    }

    def __init__(self, df, time_column, unit_format='hyphen'):
        # Check if df is not a list:
        self.isList = False
        self.has_changed_x = False
        if not isinstance(df, list):
            self.df1 = df
            self.time_column1 = time_column
            self.unit_pattern1 = self.UNIT_PATTERNS.get(unit_format, self.UNIT_PATTERNS['hyphen'])
            self.columns1 = [col for col in df.columns if col != time_column]  # exclude time_column from columns to plot
            self.current_column_index1 = 0
        else:
            self.isList = True
            # If list contains more than two dataframes, raise error
            if len(df) > 2:
                raise ValueError("List of dataframes can only contain 2 dataframes")
            self.df1 = df[0]
            self.df2 = df[1]
            # Check if time_column is a list:
            if isinstance(time_column, list):
                self.time_column1 = time_column[0]
                self.time_column2 = time_column[1]
            else:
                self.time_column1 = time_column
                self.time_column2 = time_column
            # Check if unit_format is a list:
            if isinstance(unit_format, list):
                self.unit_format1 = unit_format[0]
                self.unit_format2 = unit_format[1]
            else:
                self.unit_format1 = unit_format
                self.unit_format2 = unit_format
            self.unit_pattern1 = self.UNIT_PATTERNS.get(self.unit_format1, self.UNIT_PATTERNS['hyphen'])
            self.unit_pattern2 = self.UNIT_PATTERNS.get(self.unit_format2, self.UNIT_PATTERNS['hyphen'])
            self.columns1 = [col for col in self.df1.columns if col != self.time_column1]  # exclude time_column from columns to plot
            self.columns2 = [col for col in self.df2.columns if col != self.time_column2]  # exclude time_column from columns to plot
            self.current_column_index1 = 0
            self.current_column_index2 = 0


        self.root = tk.Tk()
        self.window_width = 900
        self.window_height = 800

        # Get screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate position
        position_top = int(self.screen_height / 2 - self.window_height / 2)
        position_right = int(self.screen_width / 2 - self.window_width / 2)

        # Set the geometry
        self.root.geometry(f"{self.window_width}x{self.window_height}+{position_right}+{position_top}")
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()

        # Create frame containing xlim and ylim entries
        self.axis_frame = tk.Frame(self.root)

        self.button_frame = tk.Frame(self.axis_frame)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_plot)
        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_plot)

        if not self.isList:
            self.next_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.previous_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            self.button_frame.grid(row=4, column=2, columnspan=2, sticky='nsew')

        if self.isList:
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.next_button2 = tk.Button(self.button_frame, text="Next", command=self.next_plot2)
            self.previous_button2 = tk.Button(self.button_frame, text="Previous", command=self.previous_plot2)
            
            self.previous_button.grid(row=0, column=0, columnspan=1, sticky='nsew')
            self.next_button.grid(row=0, column=1, columnspan=1, sticky='nsew')
            self.previous_button2.grid(row=1, column=0, columnspan=1, sticky='nsew')
            self.next_button2.grid(row=1, column=1, columnspan=1, sticky='nsew')
            self.button_frame.grid(row=4, rowspan=2, column=4, columnspan=2, sticky='nsew')

        # Initialize a StringVar with default value as the first column name
        self.column_var = tk.StringVar()
        self.column_var.set(self.columns1[0])

        # Create a dropdown menu with column names
        self.column_menu = tk.OptionMenu(self.axis_frame, self.column_var, *self.columns1, command=self.plot_selected_column)

        if self.isList:
            self.column_menu.grid(row=4, column=2, columnspan=2, sticky='nsew')
            self.column_var2 = tk.StringVar()
            self.column_var2.set(self.columns2[0])

            # Create a dropdown menu with column names
            self.column_menu2 = tk.OptionMenu(self.axis_frame, self.column_var2, *self.columns2, command=self.plot_selected_column2)
            self.column_menu2.grid(row=5, column=2, columnspan=2, sticky='nsew')
            df1_label = tk.Label(self.axis_frame, text='Dataframe #1')
            df1_label.grid(row=4, column=0, columnspan=2, sticky='nsew')
            df2_label = tk.Label(self.axis_frame, text='Dataframe #2')
            df2_label.grid(row=5, column=0, columnspan=2, sticky='nsew')
        else:
            self.column_menu.grid(row=4, column=0, columnspan=2, sticky='nsew')

        self.xmin_label = tk.Label(self.axis_frame, text='xmin')
        self.xmin_entry = tk.Entry(self.axis_frame)
        self.xmax_label = tk.Label(self.axis_frame, text='xmax')
        self.xmax_entry = tk.Entry(self.axis_frame)
        self.xmin_label.grid(row=0, column=0, sticky='nsew')
        self.xmin_entry.grid(row=0, column=1, sticky='nsew')
        self.xmax_label.grid(row=1, column=0, sticky='nsew')
        self.xmax_entry.grid(row=1, column=1, sticky='nsew')

        if not self.isList:
            self.ymin_label = tk.Label(self.axis_frame, text='ymin')
            self.ymin_entry = tk.Entry(self.axis_frame)
            self.ymax_label = tk.Label(self.axis_frame, text='ymax')
            self.ymax_entry = tk.Entry(self.axis_frame)
            # Add labels and entries to grid
            self.ymin_label.grid(row=0, column=2, sticky='nsew')
            self.ymin_entry.grid(row=0, column=3, sticky='nsew')
            self.ymax_label.grid(row=1, column=2, sticky='nsew')
            self.ymax_entry.grid(row=1, column=3, sticky='nsew')
        else:
            self.ymin_label = tk.Label(self.axis_frame, text='ymin1')
            self.ymin_entry = tk.Entry(self.axis_frame)
            self.ymax_label = tk.Label(self.axis_frame, text='ymax1')
            self.ymax_entry = tk.Entry(self.axis_frame)
            # Add labels and entries to grid
            self.ymin_label.grid(row=0, column=2, sticky='nsew')
            self.ymin_entry.grid(row=0, column=3, sticky='nsew')
            self.ymax_label.grid(row=1, column=2, sticky='nsew')
            self.ymax_entry.grid(row=1, column=3, sticky='nsew')

            self.ymin_label2 = tk.Label(self.axis_frame, text='ymin2')
            self.ymin_entry2 = tk.Entry(self.axis_frame)
            self.ymax_label2 = tk.Label(self.axis_frame, text='ymax2')
            self.ymax_entry2 = tk.Entry(self.axis_frame)

            self.ymin_label2.grid(row=0, column=4, sticky='nsew')
            self.ymin_entry2.grid(row=0, column=5, sticky='nsew')
            self.ymax_label2.grid(row=1, column=4, sticky='nsew')
            self.ymax_entry2.grid(row=1, column=5, sticky='nsew')

        self.axis_frame.pack(anchor='center')

        self.xmin_entry.bind("<KeyRelease>", self.update_x)
        self.xmax_entry.bind("<KeyRelease>", self.update_x)
        self.ymin_entry.bind("<KeyRelease>", self.update_plot1)
        self.ymax_entry.bind("<KeyRelease>", self.update_plot1)
        if self.isList:
            self.ymin_entry2.bind("<KeyRelease>", self.update_plot2)
            self.ymax_entry2.bind("<KeyRelease>", self.update_plot2)

        # Connect the callback function to the 'motion_notify_event' event
        self.canvas.mpl_connect('motion_notify_event', self.update_entries_from_toolbar_initial)

        # This should be called after all the necessary attributes are defined.
        self.plot_current_column('df1')
        if self.isList:
            self.plot_current_column('df2')

    def plot_selected_column(self, column_name):
        self.current_column_index1 = self.columns1.index(column_name)
        self.plot_current_column('df1')
        self.update_entries_from_toolbar_1(None)

    def plot_selected_column2(self, column_name):
        self.current_column_index2 = self.columns2.index(column_name)
        self.plot_current_column('df2')
        self.update_entries_from_toolbar_2(None)

    def plot_current_column(self, dataframe_tag):
        if not hasattr(self, 'ax1'):
            self.ax1 = self.fig.add_subplot(111)
        if not hasattr(self, 'ax2'):
            self.ax2 = self.ax1.twinx()
            
        if dataframe_tag == "df1":
            if self.has_changed_x:
                xlim = self.ax1.get_xlim()
            self.ax1.cla()  # clear the ax1

            # Set the title
            column_name_1 = self.columns1[self.current_column_index1]
            # Extract the units and set the label for y-axis
            match = re.search(self.unit_pattern1, column_name_1)
            cleaned_column_name1 = re.sub(self.unit_pattern1, '', column_name_1)
            self.ax1.plot(self.df1[self.time_column1], self.df1[column_name_1], label=cleaned_column_name1)
            if self.has_changed_x:
                self.ax1.set_xlim(xlim)
            # xmin = float(self.xmin_entry.get() if self.xmin_entry.get() != '' else 0)
            # xmax = float(self.xmax_entry.get() if self.xmax_entry.get() != '' else xmin + 1)
            # self.ax1.set_xlim([xmin, xmax])

            if match:
                self.ax1.set_ylabel(match.group(1))

            self.ax1.legend(bbox_to_anchor=(0.1, 1.02, 1., .102), loc='lower left', borderaxespad=0.)
            self.update_entries_from_toolbar_1(None)

        elif dataframe_tag == "df2":
            self.ax2.cla()  # clear the ax2

            column_name_2 = self.columns2[self.current_column_index2]
            # Extract the units and set the label for y-axis
            match = re.search(self.unit_pattern2, column_name_2)
            # Set the title
            cleaned_column_name2 = re.sub(self.unit_pattern2, '', column_name_2)
            self.ax2.plot(self.df2[self.time_column2], self.df2[column_name_2], label=cleaned_column_name2, color='r')

            if match:
                self.ax2.yaxis.tick_right()
                self.ax2.yaxis.set_label_position("right")
                self.ax2.set_ylabel(match.group(1))
                

            self.ax2.legend(bbox_to_anchor=(-0.1, 1.02, 1., .102), loc='lower right', borderaxespad=0.)
            self.update_entries_from_toolbar_2(None)

        else:
            raise ValueError("Invalid dataframe tag. Expected 'df1' or 'df2'.")

        if not self.isList:
            self.ax1.set_xlabel(self.time_column1)
        else:
            self.ax1.set_xlabel(f'{self.time_column1} | {self.time_column2}')
        self.canvas.draw()

    def next_plot(self):
        self.current_column_index1 = (self.current_column_index1 + 1) % len(self.columns1)
        self.plot_current_column('df1')
        self.update_dropdown()

    def next_plot2(self):
        self.current_column_index2 = (self.current_column_index2 + 1) % len(self.columns2)
        self.plot_current_column('df2')
        self.update_dropdown()

    def previous_plot(self):
        self.current_column_index1 = (self.current_column_index1 - 1) % len(self.columns1)
        self.plot_current_column('df1')
        self.update_dropdown()

    def previous_plot2(self):
        self.current_column_index2 = (self.current_column_index2 - 1) % len(self.columns2)
        self.plot_current_column('df2')
        self.update_dropdown()

    def update_dropdown(self):
        if self.isList:
            self.column_var.set(self.columns1[self.current_column_index1])
            self.column_var2.set(self.columns2[self.current_column_index2])
        else:
            self.column_var.set(self.columns1[self.current_column_index1])



    def run(self):
        self.root.mainloop()

    def update_entries_from_toolbar_initial(self, event):
        if not self.isList:
            self.xmin_entry.delete(0, tk.END)
            self.xmax_entry.delete(0, tk.END)
            self.ymin_entry.delete(0, tk.END)
            self.ymax_entry.delete(0, tk.END)
            self.xmin_entry.insert(0, self.ax1.get_xlim()[0])
            self.xmax_entry.insert(0, self.ax1.get_xlim()[1])
            self.ymin_entry.insert(0, self.ax1.get_ylim()[0])
            self.ymax_entry.insert(0, self.ax1.get_ylim()[1])
        else:
            self.xmin_entry.delete(0, tk.END)
            self.xmax_entry.delete(0, tk.END)
            self.ymin_entry.delete(0, tk.END)
            self.ymax_entry.delete(0, tk.END)
            self.ymin_entry2.delete(0, tk.END)
            self.ymax_entry2.delete(0, tk.END)
            self.xmin_entry.insert(0, self.ax1.get_xlim()[0])
            self.xmax_entry.insert(0, self.ax1.get_xlim()[1])
            self.ymin_entry.insert(0, self.ax1.get_ylim()[0])
            self.ymax_entry.insert(0, self.ax1.get_ylim()[1])
            self.ymin_entry2.insert(0, self.ax2.get_ylim()[0])
            self.ymax_entry2.insert(0, self.ax2.get_ylim()[1])

    def update_entries_from_toolbar_1(self, event):
        if not self.isList:
            self.ymin_entry.delete(0, tk.END)
            self.ymax_entry.delete(0, tk.END)
            self.ymin_entry.insert(0, self.ax1.get_ylim()[0])
            self.ymax_entry.insert(0, self.ax1.get_ylim()[1])
        else:
            self.ymin_entry.delete(0, tk.END)
            self.ymax_entry.delete(0, tk.END)
            self.ymin_entry.insert(0, self.ax1.get_ylim()[0])
            self.ymax_entry.insert(0, self.ax1.get_ylim()[1])

    def update_entries_from_toolbar_2(self, event):
        self.ymin_entry2.delete(0, tk.END)
        self.ymax_entry2.delete(0, tk.END)        
        self.ymin_entry2.insert(0, self.ax2.get_ylim()[0])
        self.ymax_entry2.insert(0, self.ax2.get_ylim()[1])

    def update_plot1(self, event):
        try:
            xmin = float(self.xmin_entry.get() if self.xmin_entry.get() != '' else 0)
            xmax = float(self.xmax_entry.get() if self.xmax_entry.get() != '' else xmin + 1)
            ymin = float(self.ymin_entry.get() if self.ymin_entry.get() != '' else 0)
            ymax = float(self.ymax_entry.get() if self.ymax_entry.get() != '' else ymin + 1)
        except ValueError:
            return

        self.ax1.set_xlim([xmin, xmax])
        self.ax1.set_ylim([ymin, ymax])

        self.canvas.draw()

    def update_plot2(self, event):
        try:
            ymin2 = float(self.ymin_entry2.get() if self.ymin_entry2.get() != '' else 0)
            ymax2 = float(self.ymax_entry2.get() if self.ymax_entry2.get() != '' else ymin2 + 1)
        except ValueError:
            return

        self.ax2.set_ylim([ymin2, ymax2])

        self.canvas.draw()

    def update_x(self, event):
        try:
            xmin = float(self.xmin_entry.get() if self.xmin_entry.get() != '' else 0)
            xmax = float(self.xmax_entry.get() if self.xmax_entry.get() != '' else xmin + 1)
        except ValueError:
            return
        self.has_changed_x = True

        self.ax1.set_xlim([xmin, xmax])
        self.ax2.set_xlim([xmin, xmax])

        self.canvas.draw()
