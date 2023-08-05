# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['torch_adapters', 'torch_adapters.adapters']

package_data = \
{'': ['*']}

install_requires = \
['torch>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'torch-adapters',
    'version': '0.0.2',
    'description': '',
    'long_description': '# torch-adapters',
    'author': 'ma2za',
    'author_email': 'mazzapaolo2019@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
