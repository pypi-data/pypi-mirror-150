
[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CI with install](https://github.com/fusion-energy/dagmc_bounding_box/actions/workflows/ci_with_install.yml/badge.svg)](https://github.com/fusion-energy/dagmc_bounding_box/actions/workflows/ci_with_install.yml)

[![PyPI](https://img.shields.io/pypi/v/dagmc_bounding_box?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/paramak/)
[![anaconda-publish](https://github.com/fusion-energy/dagmc_bounding_box/actions/workflows/anaconda-publish.yml/badge.svg)](https://github.com/fusion-energy/dagmc_bounding_box/actions/workflows/anaconda-publish.yml)

# Features

Finds the bounding box of a DAGMC geometry file.

The bounding box is a pair of coordinates that define the upper right and lower left corner of the geometry.

This which is particularly useful when assigning a regular mesh tally over the entire DAGMC geometry.

# Installation

Using Pip

```bash
pip install dagmc_bounding_box
```

Using Conda

```bash
conda install -c fusion-energy -c conda-forge dagmc_bounding_box
```

# Usage

Find the bounding box
```python
from dagmc_bounding_box import DagmcBoundingBox
my_corners = DagmcBoundingBox("dagmc.h5m").corners()
print(my_corners)
>>> ((-100, -100, -100), (100, 100, 100))
```

Extend the bounding box
```python
from dagmc_bounding_box import DagmcBoundingBox
my_corners = DagmcBoundingBox("dagmc.h5m").corners(extend=(10, 5, 2)
print(my_corners)
>>> ((-110, -105, -102), (110, 105, 102))
```
