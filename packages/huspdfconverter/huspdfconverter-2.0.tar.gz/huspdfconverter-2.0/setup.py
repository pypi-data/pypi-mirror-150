import setuptools
from pathlib import Path

setuptools.setup(
    name='huspdfconverter',
    version=2.0,
    long_description=Path('README.md').read_text(),
    pakages= setuptools.find_packages('huspdfconverter'),
    package_dir={'': 'huspdfconverter'},
     install_requires=[
      ]

)