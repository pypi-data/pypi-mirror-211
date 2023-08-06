import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.0.0.1'
PACKAGE_NAME = 'src_ie_tools'
AUTHOR = 'Samson Rock Capital'
AUTHOR_EMAIL = 'src.indexdevs@samsonrock.com'


LICENSE = 'MIT'
DESCRIPTION = 'A higher level of abstraction around API Endpoints.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
      'requests',
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
