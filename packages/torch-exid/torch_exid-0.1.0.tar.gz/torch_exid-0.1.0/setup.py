# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torch_exid']

package_data = \
{'': ['*']}

install_requires = \
['torch>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'torch-exid',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Artem Legotin',
    'author_email': 'hello@artemlegotin.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
