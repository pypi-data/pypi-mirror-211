"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages

# Read the version without importing any dependencies
version = {}
with open("hvc/version.py") as f:
    exec(f.read(), version)

setup(
    name="hvc",  # use torch-hd on PyPi to install hvc, hvc is too similar according to PyPi
    version=version["__version__"],
    description="HVC is a Python library for Hyperdimensional Vector Computing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/people-art/hvc",
    license="MIT",
    install_requires=[
        "torch>=1.9.0",
        "scipy",
        "pandas",
        "numpy",
        "requests",
        "tqdm",
        "openpyxl",
    ],
    packages=find_packages(exclude=["docs", "hvc.tests", "examples"]),
    python_requires=">=3.6, <4",
    project_urls={
        "Source": "https://github.com/people-art/hvc",
        "Documentation": "https://hvc.readthedocs.io",
    },
)
