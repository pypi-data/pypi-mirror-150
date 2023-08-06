# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c2']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['c2 = c2.main:main']}

setup_kwargs = {
    'name': 'c2',
    'version': '0.1.7',
    'description': 'No more commenting your code: Use the GPT3-based CodeCommenter',
    'long_description': None,
    'author': 'Standard Data, Inc.',
    'author_email': 'contact@standarddata.ai',
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
