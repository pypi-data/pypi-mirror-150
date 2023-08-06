# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bbgo', 'bbgo.data', 'bbgo.enums', 'bbgo.handlers', 'bbgo.utils']

package_data = \
{'': ['*']}

modules = \
['bbgo_pb2', 'bbgo_pb2_grpc']
install_requires = \
['click>=8.0.4,<9.0.0',
 'flake8>=4.0.1,<5.0.0',
 'grpcio-tools>=1.44.0,<2.0.0',
 'grpcio>=1.44.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'bbgo',
    'version': '0.1.9',
    'description': '',
    'long_description': None,
    'author': 'なるみ',
    'author_email': 'weaper@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
