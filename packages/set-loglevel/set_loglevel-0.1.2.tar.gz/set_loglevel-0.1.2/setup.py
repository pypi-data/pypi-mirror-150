# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['set_loglevel']

package_data = \
{'': ['*']}

install_requires = \
['environs>=9.5.0,<10.0.0', 'logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'set-loglevel',
    'version': '0.1.2',
    'description': 'Return a loglevel (10, 20, etc.) taking ENV LOGLEVEL into account',
    'long_description': '# set-loglevel\n[![pytest](https://github.com/ffreemt/set-loglevel/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/set-loglevel/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/set_loglevel.svg)](https://badge.fury.io/py/set_loglevel)\n\nReturn a loglevel taking ENV LOGLEVEL into account\n\n## Install it\n\n```shell\npip install set-loglevel\n# poetry add set-loglevel\n# git clone https://github.com/ffreemt/set-loglevel && cd set-loglevel\n```\n\n## Use it\n```python\nfrom set_loglevel import set_loglevel\n\nset_loglevel()  # 10/20/etc\n\n# or\nset_loglevel(20, force=True)  # 20\n\n```\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/set-loglevel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
