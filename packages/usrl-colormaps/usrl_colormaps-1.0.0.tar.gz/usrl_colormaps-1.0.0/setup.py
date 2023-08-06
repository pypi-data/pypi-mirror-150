# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['usrl_colormaps']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20,<2.0']

setup_kwargs = {
    'name': 'usrl-colormaps',
    'version': '1.0.0',
    'description': 'Matolotlib colormaps for the Uppsala Social Robotics Lab.',
    'long_description': None,
    'author': 'Sebastian Wallkötter',
    'author_email': 'sebastian.wallkotter@it.uu.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
