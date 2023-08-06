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
    'version': '0.1.1',
    'description': 'Massively parallel cloud computing with popular Python libraries for analytics, processing, and simulation! ',
    'long_description': '# Banyan\n\nBanyan Python is an extension to the Python programming language that seamlessly\nscales existing libraries and code to massive data and parallel cloud computing.\n\n## Getting Started\n\nEnsure you have Python>=3.8 installed. Install Banyan for Python as follows:\n\n`pip install banyan-python`\n\nImport and configure as follows:\n\n```\nimport banyan as bn\n\nbn.configure()\n```\n\nVisit [Banyan Computing](https://www.banyancomputing.com/resources/) for full documentation.\n',
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
