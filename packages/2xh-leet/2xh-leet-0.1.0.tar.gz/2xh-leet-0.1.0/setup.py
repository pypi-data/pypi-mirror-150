# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leet']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0', 'progressbar2>=4.0.0,<5.0.0', 'sty>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': '2xh-leet',
    'version': '0.1.0',
    'description': 'Library of Eclectic Experiments by Tenchi',
    'long_description': None,
    'author': 'Hamza Haiken',
    'author_email': 'tenchi@team2xh.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
