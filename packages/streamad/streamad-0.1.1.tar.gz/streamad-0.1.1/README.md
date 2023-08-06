# StreamAD

![StreamAD Logo](docs/source/images/logo_htmlwithname.svg)





Online anomaly detection for data stream. Detectors process the univariate or multivariate data one by one to simulte a real-time scene.



[Documentation](https://streamad.readthedocs.io/en/latest/)


<!--- BADGES: START --->

![GitHub](https://img.shields.io/github/license/Fengrui-Liu/StreamAD)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/StreamAD?style=flat)
![Read the Docs](https://img.shields.io/readthedocs/streamad?style=flat)
![PyPI](https://img.shields.io/pypi/v/streamad)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/streamad)
[![Downloads](https://static.pepy.tech/personalized-badge/streamad?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/streamad)
![example workflow](https://github.com/Fengrui-Liu/StreamAD/actions/workflows/testing.yml//badge.svg)
[![codecov](https://codecov.io/gh/Fengrui-Liu/StreamAD/branch/main/graph/badge.svg?token=AQG26L2RA7)](https://codecov.io/gh/Fengrui-Liu/StreamAD)
---



## Installation

The stable version can be installed from PyPI:

```bash
pip install streamad
```

The development version can be installed from GitHub:

```bash
pip install git+https://github.com/Fengrui-Liu/StreamAD
```



## MODELS

### For univariate time series.
- [x] KNN CAD
- [x] SPOT

### For multivariate time series, also compatible with univariate time series.
- [x] xStream