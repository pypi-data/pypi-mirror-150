# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['banyan']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.45,<2.0.0',
 'botocore>=1.23.48,<2.0.0',
 'progressbar2>=4.0.0,<5.0.0',
 'progressbar>=2.5,<3.0',
 'pygit2>=1.9.0,<2.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.63.0,<5.0.0']

setup_kwargs = {
    'name': 'banyan-python',
    'version': '0.1.0',
    'description': 'Massively parallel cloud computing with popular Python libraries for analytics, processing, and simulation! ',
    'long_description': None,
    'author': 'Banyan Computing',
    'author_email': 'support@banyancomputing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.banyancomputing.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
