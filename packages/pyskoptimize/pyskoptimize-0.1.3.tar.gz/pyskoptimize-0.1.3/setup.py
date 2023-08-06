# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyskoptimize']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scikit-optimize>=0.9.0,<0.10.0',
 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'pyskoptimize',
    'version': '0.1.3',
    'description': 'A configuration driven approach to facilitating Bayesian Hyperparameter Tuning',
    'long_description': '# PySkOptimize\n\n## Installation\n\n## Developer Contribution\n\nTo install from local development, run the following commands in order:\n\n    1. make init\n    2. make install\n\nTo add any new packages, follow the poetry requirements and add\nunit tests\n\n\n',
    'author': 'ed-turner',
    'author_email': 'edward.turner@pyscale.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.pyscale.net/PySkOptimize/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
