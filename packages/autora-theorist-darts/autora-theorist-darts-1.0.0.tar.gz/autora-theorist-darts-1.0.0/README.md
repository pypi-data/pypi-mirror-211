# AutoRA Differentiable Architecture Search

`autora-theorist-darts` is a Python module for fitting data using differentiable architecture 
search, built on AutoRA.

Website: [https://autoresearch.github.io/autora/](https://autoresearch.github.io/autora/)

## User Guide

You will need:

- `python` 3.8 or greater: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- `graphviz` (optional, required for computation graph visualizations): 
  [https://graphviz.org/download/](https://graphviz.org/download/)

Install DARTS as part of the `autora` package:

```shell
pip install -U "autora[theorist-darts]" --pre
```

> It is recommended to use a `python` environment manager like `virtualenv`.

Check your installation by running:
```shell
python -c "from autora.theorist.darts import DARTSRegressor; DARTSRegressor()"
```
