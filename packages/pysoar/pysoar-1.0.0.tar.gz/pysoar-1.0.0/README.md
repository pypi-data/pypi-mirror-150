# PySOAR

PySOAR is a Python (3.9+) package for data analysis of translocation events during nanopore sensing. The main features include:
* Baseline correction function.
* Splitting the current into bins and doing a Poisson fit on that data to help the user visually decide on what threshold should be used for this data.
* Finding peaks function based on the threshold chosen.
* Ability to extract features from the events using both CUSUM and ADEPT methods.
* Histogram plots of peak curretn and dwell time data.

# Installation

To install with pip:
'''

pip install --user pysoar

'''

PySOAR utilises the following external libraries:
* [NumPy](https://numpy.org/)
* [SciPy]((https://scipy.org/))
* [ruptures](https://centre-borelli.github.io/ruptures-docs/)
* [matplotlib](https://matplotlib.org/)

# Acknowledgements
Developed by Vladimir Ivanov as part of the MSci final year project while working with the Edel's group at Imperial College London