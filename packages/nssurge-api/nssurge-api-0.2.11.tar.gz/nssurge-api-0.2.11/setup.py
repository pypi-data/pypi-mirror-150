# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nssurge_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'nssurge-api',
    'version': '0.2.11',
    'description': 'NSSurge HTTP API for Python',
    'long_description': '',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tddschn/nssurge-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
