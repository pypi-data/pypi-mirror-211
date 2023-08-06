#!/usr/bin/env python
import numpy
from Cython.Build import cythonize
from setuptools import Extension, setup

files = [
    "const.c",
    "main.c",
    "halo_integral.c",
    "polevl.c",
    "sici.c",
    "sicif.c",
    "polevlf.c",
    "logf.c",
    "sinf.c",
    "constf.c",
    "mtherr.c",
]
ext_modules = [
    Extension(
        name="PyCosmo.cython.halo_integral",
        ext_modules=cythonize("src/PyCosmo/cython/halo_integral.pyx"),
        sources=["src/PyCosmo/cython/" + file for file in files],
        include_dirs=[numpy.get_include()],
    )
]

setup(
    ext_modules=ext_modules,
)
