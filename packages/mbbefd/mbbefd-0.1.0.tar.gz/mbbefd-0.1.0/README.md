# Structure
https://samharrison.science/posts/conda-package-fortran-python/

# Release

```bat
cibuildwheel --platform windows
twine upload wheelhouse/*
```