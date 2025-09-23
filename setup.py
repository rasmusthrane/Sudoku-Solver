from setuptools import setup, find_packages

setup(
    name="sudoku_solver",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
