# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atentry']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'atentry',
    'version': '1.0.0',
    'description': 'Never see `if __name__ == "__main__"` again!',
    'long_description': '# The `@entry` decorator\n\n[![PyPI](https://img.shields.io/pypi/v/atentry)](https://pypi.org/project/atentry/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/atentry)\n\nTired of the traditional python `if __name__ == \'__main__\':` pattern? Try `@entry` instead!\n\n`@entry` is designed to be a simple decorator for declaring main functions in python. In the backend, the same module name check is performed, but it keeps your code a little cleaner.\n\n## Usage\n\n**Simple example:**\n\n```python\nfrom atentry import entry\n\n@entry\ndef main():\n    print("Hello, world!")\n```\n\n**Using a return value:**\n\n```python\nfrom atentry import entry\n\n@entry\ndef main() -> int:\n    print("Hello, world!")\n    return 128 # Program exit code\n```\n\n## Installation\n\nLoading this library in your project is as simple as:\n\n```sh\n# Using Poetry\npoetry add atentry\n\n# Using PiP\npython3 -m pip install atentry\n```\n',
    'author': 'Evan Pratten',
    'author_email': 'ewpratten@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ewpratten/atentry',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
