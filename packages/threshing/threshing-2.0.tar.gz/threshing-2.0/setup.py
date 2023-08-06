import setuptools
from pathlib import Path

setuptools.setup(
    name='threshing',
    version=2.0,
    long_description=Path('README.md').read_text(),
    pakages= setuptools.find_packages(exclude=['tests','date'])

)