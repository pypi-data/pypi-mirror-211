from setuptools import Extension, setup
from Cython.Build import cythonize
import numpy

setup(
    name="mbbefd",
    zip_safe=False,
    # packages=['mbbefd'],
    include_dirs=[numpy.get_include()],
    ext_modules=cythonize("mbbefd.pyx", annotate=True),
    # # include_dirs=[numpy.get_include()],
    # ext_modules=cythonize(
    #     # language_level = "3",
    #     annotate=True,
    #     module_list=Extension("mbbefd", ["src/mbbefd.pyx"], include_dirs=[numpy.get_include()]),
    # )
)