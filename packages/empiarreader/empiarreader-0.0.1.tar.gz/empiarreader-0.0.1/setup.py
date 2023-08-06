# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['empiarreader']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'intake-xarray>=0.6.1,<0.7.0',
 'intake>=0.6.5,<0.7.0',
 'matplotlib>=3.6.1,<4.0.0',
 'mrcfile>=1.4.3,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-image>=0.19.3,<0.20.0',
 'setuptools>=67.7.2,<68.0.0',
 'starfile>=0.4.11,<0.5.0',
 'xarray>=2022.9.0,<2023.0.0']

entry_points = \
{'intake.drivers': ['empiar = empiarreader:EmpiarCatalog',
                    'mrc = empiarreader:MrcSource',
                    'star = empiarreader:StarSource']}

setup_kwargs = {
    'name': 'empiarreader',
    'version': '0.0.1',
    'description': '',
    'long_description': 'None',
    'author': 'mooniean',
    'author_email': 'bcostagomes@turing.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
