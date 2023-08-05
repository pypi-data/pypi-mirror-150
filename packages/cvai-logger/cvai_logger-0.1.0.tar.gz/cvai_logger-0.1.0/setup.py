# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvai_logger']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2022.1,<2023.0']

setup_kwargs = {
    'name': 'cvai-logger',
    'version': '0.1.0',
    'description': 'ClearVision AI logger',
    'long_description': None,
    'author': 'Gautham Reddy',
    'author_email': 'gauthamv93@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
