# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cli-jam',
    'version': '0.1.0',
    'description': 'A very useful app.',
    'long_description': None,
    'author': 'Chris Webster',
    'author_email': 'chris@dataq.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
