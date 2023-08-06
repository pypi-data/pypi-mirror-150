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
    'version': '0.1.1',
    'description': 'Library of Eclectic Experiments by Tenchi',
    'long_description': '# LEET\n\n*Library of Eclectic Experiments by Tenchi*\n\nRandom modules that I made and use in several project and are too small to get their own package. A `util` library of sorts.\n\n---\n\n## Contents\n\n<!-- MarkdownTOC autolink=true -->\n\n- [Logging](#logging)\n    - [Progress bars](#progress-bars)\n    - [Images](#images)\n\n<!-- /MarkdownTOC -->\n\n## Logging\n\nModule that provides a fancy-looking theme for Python loggers.\n\n(TODO: Screenshot)\n\nTo enable, `import leet.logging` from anywhere (maybe the main `__init__.py` of your project). You will then have a global logger `log` function that you can use from anywhere:\n\n```py\nlog.info("Hello")\nlog.warn("World")\n```\n\n### Progress bars\n\nAlso provides a progress bar (from [WoLpH/python-progressbar](https://github.com/WoLpH/python-progressbar)) that fits in the theme:\n\n```py\nfrom time import sleep\nfrom leet.logging import ProgressBar\n\nfor i in ProgressBar(range(10)):\n    sleep(1)\n    log.info("Working on %d..." % i)\n```\n\n### Images\n\nAlso supports outputing images via [imgcat](https://iterm2.com/utilities/imgcat) if using [iTerm2](https://iterm2.com/) (support for other tools pending):\n\n```py\nlog.warn("Image is too big:", extras={"img": "path/to/image.png"})\n```\n',
    'author': 'Hamza Haiken',
    'author_email': 'tenchi@team2xh.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Tenchi2xh/leet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
