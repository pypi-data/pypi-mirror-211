from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'Helper functions that I use often'
LONG_DESCRIPTION = '''A package that allows me to import functions that I use often.'''
# DataFramePlotter - given a dataframe with multiple variables, plots each variable against time in a tkinter window. Requires pandas, matplotlib, tkinter, and re. The usage is: 
#     import brunospackage as bp
#     plotter = bp.DataFramePlotter(df, nameOfTimeColumn, unit_format)
#     plotter.run()'''

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="brunospackage", 
        version=VERSION,
        author="Bruno Tacchi",
        author_email="bruno_tacchi@hotmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['matplotlib', 'pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        # import pandas as pd
        # import matplotlib.pyplot as plt
        # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        # from matplotlib.figure import Figure
        # import tkinter as tk
        # import re
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)