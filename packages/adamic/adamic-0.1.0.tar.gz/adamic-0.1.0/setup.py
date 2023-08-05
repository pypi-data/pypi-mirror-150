import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'adamic'
AUTHOR = 'Ben Moran'
AUTHOR_EMAIL = 'benjamin.moran.287@gmail.com'
URL = 'https://github.com/redsoxfan0219/adamic'

LICENSE = 'MIT License'
DESCRIPTION = 'A package to create data dictionaries, given a Pandas df'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'pandas>=1.1'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )