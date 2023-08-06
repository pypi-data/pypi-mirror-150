# npy-cpp-patches
Read N-Dimensional patches from `.npy` files. This module is built using `C++` and has `Python3` bindings.

## Data Specifications

- Arrays must be saved in `C-contiguous` format, i.e. **NOT** `Fortran-contiguous`.
- First dimension is indexed using `qspace_index`, and therefore is a non-contiguous patch dimension.
- Next dimensions are specified by a patch shape `C++` vector or `Python` tuple. To extract patches of lower dimensionality than that of the data, set the corresponding dimensions to `1`.


## Python Usage

### Install
```pip install cpp-npy-patcher```

### Usage
```python

from npy_patcher import PatcherDouble, PatcherFloat, PatcherInt, PatcherLong



```

## C++ Usage