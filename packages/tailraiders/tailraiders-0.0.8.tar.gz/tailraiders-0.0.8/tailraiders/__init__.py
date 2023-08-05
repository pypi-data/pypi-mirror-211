"""
Tailraiders
=======================================

The tailraiders package is made to help with general Data Sciency stuff.
"""

# Checking if dependencies are installed, the dependencies
# of my libary are stored in the dependency_module value
dependency_module = ['pandas',
                     'numpy',
                     'matplotlib',
                     'seaborn',
                     'sklearn']

# For-loop to check for modules
for module in dependency_module:
    # Try to import modules
    try:
        __import__(module)
    # Raise an error when it fails, telling them to install the failed module
    except ImportError:
        raise ImportError(f"The required package {module} \
                            was not found. Please install it.")

# Making it so you can, for certain parts, use from tailraiders import _blank_
from tailraiders.boaboa.doc import docstring
from tailraiders.gajalaka.plots import Plot, MeltPlot
from tailraiders.protector.nan import Nan
from tailraiders.protector.prep import Outliers
