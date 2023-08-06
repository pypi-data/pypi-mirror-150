# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confident', 'confident.loaders']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'confident',
    'version': '0.2.2',
    'description': 'Loading configurations from multiple sources into a data model.',
    'long_description': None,
    'author': 'limonyellow',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
