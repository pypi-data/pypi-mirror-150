# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deep_dance', 'deep_dance.client', 'deep_dance.client.commands']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0']

entry_points = \
{'console_scripts': ['deep_dance = deep_dance.client.dance_application:main']}

setup_kwargs = {
    'name': 'deep-dance',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'AeRabelais',
    'author_email': 'pantagruelspendulum@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
