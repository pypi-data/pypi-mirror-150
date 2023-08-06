# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyswot', 'pyswot.vendor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyswot',
    'version': '0.2.2',
    'description': 'Python wrapper for JetBrains/swot',
    'long_description': '# PySwot\n\n[![CI](https://github.com/DIAGNijmegen/rse-pyswot/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/DIAGNijmegen/rse-pyswot/actions/workflows/ci.yml?query=branch%3Amain)\n[![PyPI](https://img.shields.io/pypi/v/pyswot)](https://pypi.org/project/pyswot/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyswot)](https://pypi.org/project/pyswot/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPython wrapper for [JetBrains/swot](https://github.com/JetBrains/swot).\n\n  - Free software: Apache Software License 2.0\n\n## Features\n\nThis library is a wrapper around\n[JetBrains/swot](https://github.com/JetBrains/swot) and provides two\nmethods:\n\n```python\n>>> from pyswot import is_academic\n>>> is_academic("user@ox.ac.uk")\nTrue\n>>> is_academic("user@gmail.com")\nFalse\n```\n\n```python\n>>> from pyswot import find_school_names\n>>> find_school_names("user@ox.ac.uk")\n[\'University of Oxford\']\n>>> find_school_names("user@gmail.com")\n[]\n```\n',
    'author': 'James Meakin',
    'author_email': 'pyswot@jmsmkn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DIAGNijmegen/rse-pyswot',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
