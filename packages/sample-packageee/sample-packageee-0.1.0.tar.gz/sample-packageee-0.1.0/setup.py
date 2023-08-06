# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_packageee']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0', 'flake8>=4.0.1,<5.0.0', 'mypy>=0.950,<0.951']

setup_kwargs = {
    'name': 'sample-packageee',
    'version': '0.1.0',
    'description': 'Sample package',
    'long_description': '# Sample package\nTest package',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
