# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ImageCompare']

package_data = \
{'': ['*']}

install_requires = \
['imutils>=0.5.4,<0.6.0',
 'numpy>=1.22.3,<2.0.0',
 'opencv-python-headless>=4.5.5,<5.0.0',
 'robotframework>=4',
 'scikit-image>=0.19.2,<0.20.0']

setup_kwargs = {
    'name': 'robotframework-imagecompare',
    'version': '0.1.0',
    'description': 'A Robot Framework Library for image comparisons',
    'long_description': None,
    'author': 'Many Kasiriha',
    'author_email': 'many.kasiriha@dbschenker.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
