# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usrl_colormaps']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usrl-colormaps',
    'version': '0.0.1',
    'description': 'Matolotlib colormaps for the Uppsala Social Robotics Lab.',
    'long_description': None,
    'author': 'Sebastian Wallkötter',
    'author_email': 'sebastian.wallkotter@it.uu.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
