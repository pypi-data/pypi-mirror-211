from pathlib import Path
import setuptools
setuptools.setup(
    name="kirapdf",
    version=1.0,
    long_discription=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])





)
