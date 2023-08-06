# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['d0da']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

setup_kwargs = {
    'name': 'd0da',
    'version': '0.1.0',
    'description': 'Wooting D0DA protocol',
    'long_description': '',
    'author': 'Dick Marinus',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
