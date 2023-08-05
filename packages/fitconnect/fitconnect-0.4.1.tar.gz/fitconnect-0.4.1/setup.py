# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitconnect']

package_data = \
{'': ['*'], 'fitconnect': ['schema/*']}

install_requires = \
['jsonschema>=4.4.0,<5.0.0',
 'jwcrypto>=1.1,<2.0',
 'requests>=2.26.0,<3.0.0',
 'semver>=3.0.0.dev3,<4.0.0',
 'strictyaml>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'fitconnect',
    'version': '0.4.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
