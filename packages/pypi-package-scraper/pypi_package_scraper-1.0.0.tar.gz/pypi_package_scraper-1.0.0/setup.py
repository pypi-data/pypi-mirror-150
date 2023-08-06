import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
VERSION = '1.0.0'
PACKAGE_NAME = 'pypi_package_scraper'
AUTHOR = 'DataKund'
AUTHOR_EMAIL = 'datakund@gmail.com'
URL = 'https://github.com/you/your_package'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'A python library to scrape pypi packages data'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"
KEYWORDS='datakund_cloud data scraper pypi'
INSTALL_REQUIRES = [
      'requests','tqdm','datakund_cloud'
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
      packages=find_packages(),
      keywords = KEYWORDS
      )