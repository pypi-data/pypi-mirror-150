# set-loglevel
[![pytest](https://github.com/ffreemt/set-loglevel/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/set-loglevel/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/set_loglevel.svg)](https://badge.fury.io/py/set_loglevel)

Return a loglevel taking ENV LOGLEVEL into account

## Install it

```shell
pip install set-loglevel
# poetry add set-loglevel
# git clone https://github.com/ffreemt/set-loglevel && cd set-loglevel
```

## Use it
```python
from set_loglevel import set_loglevel

set_loglevel()  # 10/20/etc

# or
set_loglevel(20, force=True)  # 20

```
