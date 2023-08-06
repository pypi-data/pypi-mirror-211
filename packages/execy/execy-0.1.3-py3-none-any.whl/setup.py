# setup.py

from setuptools import setup, find_packages

setup(
    name="execy",
    version="1.0.1",
    author="hglong16",
    author_email="intihad.vuong@gmail.com",
    description="A package for measuring execution time",
    packages=find_packages("src"),
    package_dir={"execy": "src"},
    python_requires=">=3.6",
    license="MIT",
)
