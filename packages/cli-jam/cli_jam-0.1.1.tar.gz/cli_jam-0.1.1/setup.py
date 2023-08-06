# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['app']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['useful = app.useful_app:main']}

setup_kwargs = {
    'name': 'cli-jam',
    'version': '0.1.1',
    'description': 'A very useful app.',
    'long_description': None,
    'author': 'Chris Webster',
    'author_email': 'chris@dataq.co.za',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
