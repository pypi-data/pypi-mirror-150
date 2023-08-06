# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mamimo']

package_data = \
{'': ['*']}

install_requires = \
['isort>=5.10.1,<6.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pre-commit>=2.18.1,<3.0.0',
 'scikit-learn>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'mamimo',
    'version': '0.1.0',
    'description': 'A package to compute a marketing mix model.',
    'long_description': None,
    'author': 'Garve',
    'author_email': 'xgarve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
