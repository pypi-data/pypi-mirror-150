# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memery']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.1.0,<10.0.0',
 'annoy>=1.17.0,<2.0.0',
 'ftfy>=6.1.1,<7.0.0',
 'regex>=2022.4.24,<2023.0.0',
 'streamlit==1.3.1',
 'torch>=1.11.0,<2.0.0',
 'torchvision>=0.12.0,<0.13.0',
 'tqdm>=4.64.0,<5.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['memery = memery.cli:main']}

setup_kwargs = {
    'name': 'memery',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'deepfates',
    'author_email': 'deepfates@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
