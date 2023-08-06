# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['listless']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'listless',
    'version': '0.1.2',
    'description': 'generator utils; aka listless',
    'long_description': '<a href="https://github.com/dynamic-graphics-inc/dgpy-libs">\n<img align="right" src="https://github.com/dynamic-graphics-inc/dgpy-libs/blob/main/docs/images/dgpy_banner.svg?raw=true" alt="drawing" height="120" width="300"/>\n</a>\n\n# listless\n\n[![Wheel](https://img.shields.io/pypi/wheel/listless.svg)](https://img.shields.io/pypi/wheel/listless.svg)\n[![Version](https://img.shields.io/pypi/v/listless.svg)](https://img.shields.io/pypi/v/listless.svg)\n[![py_versions](https://img.shields.io/pypi/pyversions/listless.svg)](https://img.shields.io/pypi/pyversions/listless.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n**Install:** `pip install listless` OR `poetry add listless`\n\n**What:** typed & tested python itertools/generators-utils library\n',
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dynamic-graphics-inc/dgpy-libs/tree/main/libs/listless',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
