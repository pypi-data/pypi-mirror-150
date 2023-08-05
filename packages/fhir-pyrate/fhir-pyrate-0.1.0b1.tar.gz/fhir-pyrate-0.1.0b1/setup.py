# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fhir_pyrate', 'fhir_pyrate.util']

package_data = \
{'': ['*']}

install_requires = \
['SimpleITK>=2.0.2,<3.0.0',
 'dicomweb-client>=0.52.0,<0.53.0',
 'numpy',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas==1.2.0',
 'pydicom>=2.1.2,<3.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'spacy>=3.0.6,<4.0.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'fhir-pyrate',
    'version': '0.1.0b1',
    'description': 'FHIR-PYrate is a package that provides a high-level API to query FHIR Servers for bundles of resources and return the structured information into Pandas DataFrames. It can also be used to filter resources and download DICOM studies and series.',
    'long_description': None,
    'author': 'Giulia Baldini',
    'author_email': 'giulia.baldini@uk-essen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
