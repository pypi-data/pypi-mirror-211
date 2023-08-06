"""
This file creates extensions for pyx files.
"""
import platform

import numpy
from Cython.Build import cythonize
from setuptools import setup, Extension

os_type_name: str = platform.system()

if "WINDOWS" in os_type_name.upper():
    omp_extra_compile_arg = "/openmp"
    omp_extra_link_arg = "/openmp"
else:
    omp_extra_compile_arg = "-fopenmp"
    omp_extra_link_arg = "-fopenmp"

ext_modules = [
    Extension(
        name='organon.afe.domain.modelling.helper.data_frame_builder_helper',
        sources=[r'./organon/afe/domain/modelling/helper/data_frame_builder_helper.pyx'],
        extra_compile_args=[omp_extra_compile_arg],
        extra_link_args=[omp_extra_link_arg],
        include_dirs=[numpy.get_include()],
        language='c++'
    ),
    Extension(
        name='organon.fl.mathematics.sweep.pyx_files.sweep_helper',
        sources=[r'./organon/fl/mathematics/sweep/pyx_files/sweep_helper.pyx'],
        extra_compile_args=[omp_extra_compile_arg],
        extra_link_args=[omp_extra_link_arg],
        include_dirs=[numpy.get_include()],
        language='c++'
    ),
]

if __name__ == "__main__":
    setup(name="CythonFiles", ext_modules=cythonize(ext_modules))
