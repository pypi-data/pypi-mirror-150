# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xtbclient', 'xtbclient.client', 'xtbclient.models']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0',
 'pytest-asyncio>=0.18.3,<0.19.0',
 'pytest-mock>=3.7.0,<4.0.0',
 'websocket-client>=1.3.2,<2.0.0',
 'websockets>=10.3,<11.0']

setup_kwargs = {
    'name': 'xtbclient',
    'version': '0.1.0',
    'description': 'XTB trading platform client',
    'long_description': None,
    'author': 'Cristian Libotean',
    'author_email': 'eblis102@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
