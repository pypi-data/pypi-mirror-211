"""
TO CREATE A WHEEL FILE RUN:
-pip install wheel setuptools
-python setup.py bdist_wheel
"""

from Cython.Build import cythonize
from setuptools import find_packages, setup

from cython_setup import ext_modules

if __name__ == "__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        name="autonon",
        version="0.4.0",
        author="Organon Analytics",
        author_email="support@organonanalytics.com",
        description="Organon Automated ML Platform",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitlab.com/organon-os/autonon",
        packages=find_packages(exclude=["organon.tests*"]),
        package_data={
            "organon.afe": [
                "data/*"
            ]
        },
        install_requires=[
            "numpy>=1.20.0",
            "pandas>=1.1.1",
            "paramiko>=2.7.2",
            "psutil>=5.7.2",
            "sortedcontainers>=2.3.0",
            "pycryptodome>=3.9.9",
            "plotly>=4.14.1",
            "matplotlib>=3.3.3",
            "scipy>=1.6.0",
            "cryptography>=3.3.1",
            "joblib>=1.0.1",
            "scikit-learn>=1.1",
            "lightgbm>=3.2.1",
            "python-dateutil>=2.8.2",
            "six>=1.16.0",
            "seaborn>=0.11.2",
            "xgboost>=1.6.1",
            "scikit-optimize>=0.9.0",
            "statsmodels >= 0.13.2",
            "tensorflow>=2.10",
            "defusedxml >= 0.6.0",
            "transformers>=4.26.0",
            "datasets>=2.6.1",
            "keras>=2.10.0",
            "ultralytics>=8.0.59"
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.8',
        ext_modules=cythonize(ext_modules)
    )
