# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['warehouses', 'warehouses.bigquery']

package_data = \
{'': ['*']}

install_requires = \
['geopandas>=0.10.2,<0.11.0',
 'google-cloud-bigquery>=3.1.0,<4.0.0',
 'pandas-gbq>=0.17.4,<0.18.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'warehouses',
    'version': '0.1.1',
    'description': 'Python library to facilitate read/write of GIS and tabular data between Python and cloud warehouses',
    'long_description': None,
    'author': 'aaronfraint',
    'author_email': 'aaronfraint@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
