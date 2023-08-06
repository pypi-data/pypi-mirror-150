# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atentry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'atentry',
    'version': '0.1.0',
    'description': 'Never see `if __name__ == "__main__"` again!',
    'long_description': None,
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
