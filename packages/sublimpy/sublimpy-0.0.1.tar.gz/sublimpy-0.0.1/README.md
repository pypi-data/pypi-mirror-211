# sublimpy
Tools for working with data from the Sublimation of Snow project.

Check out test.ipynb to see some functionality. 

Contains the following modules:
sublimpy.utils
* Utilities for downloading, cleaning, and otherwise working with SoS data.

sublimpy.variables
* Convenience functions for calculating additional variables from SoS measurements.
* E.g. surface temperatures, virtual potential temperatures, turbulent kinetic energy

sublimpy.tidy
* Convenience functions for creating a tidy dataframe dataset from SoS NetCDF datasets.
* Tidy dataframes have "height", "tower", and "measurement" columns which are parsed from the variables provided in the original SoS datasets.

sublimpy.gradients
* Classes to calculate wind and temperature gradients and Richardson numbers from SoS measurements.
* Multiple methods are available, including fitting log-linear and log-polynomial curves, and simple central-differencing.

This package is published exclusively to pip. It can be installed 
```
pip install sublimpy
```

It is published to pypi like so:
```
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```