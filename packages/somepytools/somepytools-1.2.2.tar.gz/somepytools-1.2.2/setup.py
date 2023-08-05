# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['somepytools']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['PyYAML>=6.0,<7.0',
         'toml>=0.10.2,<0.11.0',
         'numpy>=1.22.3,<2.0.0',
         'opencv-python-headless>=4.5.5,<5.0.0',
         'torch>=1.11.0,<2.0.0',
         'matplotlib>=3.5.1,<4.0.0']}

setup_kwargs = {
    'name': 'somepytools',
    'version': '1.2.2',
    'description': 'Just some useful Python tools',
    'long_description': "# Some useful tools for Python [in context of Data Science]\n\n[![PyPI](https://img.shields.io/pypi/v/somepytools)](https://pypi.org/project/somepytools/)\n[![Downloads](https://pepy.tech/badge/somepytools)](https://pepy.tech/project/somepytools)\n[![License: Apache](https://img.shields.io/badge/license-Apache%202-blue)](https://github.com/v-goncharenko/somepytools/blob/master/LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nHere I gather functions that are handful in Data Science & Machine Learning\nprojects.\n\nAll functions are described by their docstrings, rendering documentation is next\nstep.\n\n## Installation\n\nIt's [published on PyPI](https://pypi.org/project/somepytools/), so simply\n\n`pip install somepytools`\n\n## Reference\n\nModules inclues:\n\n- extended typing module\n- common read-write operations for configs\n- utils to work with filesystem\n- functions to handle videos in opencv\n- torch utilities (infer and count parameters)\n- even more (e.g. wrapper to convert strings inputs to `pathlib`)\n\nFor now it's better to go through the files and look at contents\n",
    'author': 'Vladilav Goncharenko',
    'author_email': 'vladislav.goncharenko@phystech.edu',
    'maintainer': 'Vladislav Goncharenko',
    'maintainer_email': 'vladislav.goncharenko@phystech.edu',
    'url': 'https://github.com/v-goncharenko/somepytools',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
