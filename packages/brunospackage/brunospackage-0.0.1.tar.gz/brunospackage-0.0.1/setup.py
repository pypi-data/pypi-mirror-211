from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

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
        install_requires=['matplotlib', 'tkinter', 'pandas', 're'], # add any additional packages that 
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