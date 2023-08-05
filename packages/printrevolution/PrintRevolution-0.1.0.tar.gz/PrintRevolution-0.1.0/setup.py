# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printrevolution']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['revolution = revolution:main']}

setup_kwargs = {
    'name': 'printrevolution',
    'version': '0.1.0',
    'description': 'A soothing meditation on politics.',
    'long_description': None,
    'author': 'Sam Lavigne',
    'author_email': 'splavigne@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
