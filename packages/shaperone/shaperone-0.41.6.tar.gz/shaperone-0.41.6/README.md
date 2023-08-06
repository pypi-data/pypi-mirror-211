
SHAPerone is a patched fork of [SHAP](https://pypi.org/project/shap)

Patches

### Shaperone 0.41.6 (Shap 0.41)
* Fixed  [issue 2909](https://github.com/slundberg/shap/issues/2909) `NumbaDeprecationWarning: The 'nopython' keyword argument was not 
  supplied to the 'numba.jit' decorator.` This will prevent  a breaking change in `Numba>=0.59.0`
* Fixed missing jit import in `links.py`
* Upgraded github action `actions/checkout@v2, actions/setup-python@v2, codecov/codecov-action@v2` to `v3`. 
  The `v2` actions depend on  depreciated `node 12`, the new `v2` actions have upgraded to `node 16`

### Shaperone 0.41.5 (Shap 0.41)
* Fixed the failing `build_wheels.yml` github action for the OSX target. Upgraded from the no longer existing `macOS-10.15` to `macos-11`.
* Patched [issue 2721](https://github.com/slundberg/shap/issues/2721), [pull 2697](https://github.com/slundberg/shap/pull/2697) with `beeswarmplot` that 
broke compatibility with `matplotlib>3.5.3`
* Removed usage of np.int, np.bool and np.float [pull 1890](https://github.com/slundberg/shap/pull/1890). 
The use of np.int, np.bool and np.float has been depreciated since numpy 1.20.0 and removed in `numpy>=1.24.0`.

## Install

SHAPerone can be installed from [PyPI](https://pypi.org/project/shaperone):

<pre>
pip install shaperone
</pre>
