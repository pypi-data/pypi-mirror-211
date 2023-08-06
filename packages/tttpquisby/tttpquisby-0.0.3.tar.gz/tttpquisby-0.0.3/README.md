**Quisby** is a tool to provide first view into the results from various benchmarks such as linpack, streams, fio etc. It doesn't aim to replace existing data viz tool but rather to provide a simplified view to the data with basic metric to understand the benchmark results from a higher level view. For detailed view, there are other tools such as pbench-dashboard, js-charts etc at hand.

#### Setup
*Prerequisite*: Make sure you have `jinja2` installed before running any `make` command below. 
```
$ pip install Jinja2
```
##### Install
- Install pquisby package locally onto system
```console
$ make local PACKAGE_NAME=pquisby
```

##### Push to Pypi
- Push quisby to pypi
```console
$ make pypi PACKAGE_NAME=pquisby
```

- Push quisby to testpypi
```console
$ make testpypi PACKAGE_NAME=pquisby
```

> Note:  For password-less pypi authentication please create config [example]( https://packaging.python.org/en/latest/specifications/pypirc/#using-another-package-index)